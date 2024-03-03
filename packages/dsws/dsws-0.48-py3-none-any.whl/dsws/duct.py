"""
Data Science Work Space - Duct

Duct provides a single class object that is intended to consolidate
all analytical source data connection patterns.
'duct' was deliberately chosen to consolidate the collection of connection
components, but avoid names like pipe, connection, stream to avoid naming
confusion as well as to not limit the types of work space components included

"""

from pyspark.sql import DataFrame as Sdf
from pandas import DataFrame as Pdf
from pyspark.sql import types as T
from delta import DeltaTable
from pyspark.sql import SparkSession

from IPython.core.magic import register_cell_magic
from abc import ABC, abstractmethod
from pyspark.sql import DataFrame
from pyspark.sql.readwriter import DataFrameReader, DataFrameWriter
import pathlib
import re
import subprocess
import inspect
import pandas as pd
from typing import Callable

import ipywidgets as widgets
from bamboolib.plugins import LoaderPlugin, DF_NEW, Text


class Displayer:

    __display: Callable[[object], None]
    __displayHTML: Callable[[object], None]

    def __init__(self, display_fn=None, displayHTML_fn=None):
        self._display = display_fn
        self._displayHTML = displayHTML_fn

    @property
    def _display(self):
        return self.__display

    @_display.setter
    def _display(self, value):
        if callable(value):
            self.__display = value
        else:
            from IPython.display import display

            def d(display_input: object):
                display(display_input)
                return None

            self.__display: Callable[[], None] = d

    @_display.deleter
    def _display(self):
        _display = None

    @property
    def _displayHTML(self):
        return self.__displayHTML

    @_displayHTML.setter
    def _displayHTML(self, value):
        if callable(value):
            self.__displayHTML = value
        else:
            from IPython.core.display import HTML
            from IPython.display import display

            def dh(displayHTML_input: object):
                display(HTML(displayHTML_input))
                return None

            self.__displayHTML: Callable[[], None] = dh

    @_displayHTML.deleter
    def _displayHTML(self):
        self._displayHTML = None


class Alias:
    """Class used within CommandLineInterface to handle dynamic alias"""

    def __init__(self, alias, command, url, picker):
        self.alias = alias
        self._command = command
        self._url = url
        self._picker = picker

    def set_default(self):
        with open(self._picker, "w") as f:
            f.write("clear\n")
            f.write(self.alias + "\n")


class CommandLineInterface:
    """Optional Class to create one or more aliases for workspace connector"""

    def __init__(self, startup_file: str, aliases: [{}] = None):
        """Init will add aliases terminal startup
        startup_file is where all aliases will be set.
        Each alias will be a dict:
        startup_file
        [{"alias": <name of the alias to be used in terminal>,
          "command": <string of command to be used in alias>,}, ...]
        """
        self._startup_file = pathlib.Path(startup_file)
        self._picker = self._startup_file.parent.joinpath('.picker')
        self.aliases = aliases
        with open(self._startup_file, 'r') as f:
            startup_txt = f.read()
        for a in list(aliases):
            if len(re.findall(f"alias {a['alias']}=", startup_txt)) == 0:
                with open(self._startup_file, "a") as f:
                    f.write(f"alias {a['alias']}='{a['command']}'\n")
            setattr(self, str(a['alias']).replace('-', '_'),
                    Alias(alias=a['alias'],
                          command=a['command'],
                          url=None,
                          picker=self._picker))

        # add startup command to run picker
        subprocess.run(["touch", self._picker])
        with open(self._startup_file, "a") as f:
            f.write(f"source {self._picker}\n")

    def unset_default(self):
        with open(self._picker, "w") as f:
            f.write('')


class SparkJDBC(Displayer):
    """Spark JDBC Class provides three methods and one property to read workspace data directly into spark:
        jdbc_reader: DataFrameReader with all authentication and configs applied
        jdbc_table(table: str): DataFrame of workspace table read using spark jdbc
        jdbc_qry(): Dataframe of query run against workspace (uses pushdown where applicable)
        jdbc_writer(src: DataFrame, tgt: str):
    """

    _reader: DataFrameReader = None

    def __init__(self, kwargs: dict, handle=None,
                 display_fn=None, displayHTML_fn=None):
        super().__init__(display_fn, displayHTML_fn)
        self._kwargs = kwargs
        self._handle = handle
        self._register_magic()

    @property
    def reader(self) -> DataFrameReader:
        if not self._reader:
            from pyspark.sql import SparkSession
            self._reader = SparkSession.builder.getOrCreate().read.format("jdbc").options(**self._kwargs)
        return self._reader

    def table(self, table: str) -> DataFrame:
        return self.reader.option("dbtable", table).load()

    def qry(self, sql: str) -> DataFrame:
        return self.reader.option("query", sql).load()

    def writer(self, src: DataFrame, tgt: str) -> DataFrameWriter:
        return src.write.format('jdbc') \
            .options(**self._kwargs) \
            .option("dbtable", tgt)

    def _register_magic(self):
        @register_cell_magic(self._handle + '_spark')
        def spark_jdbc_qry_magic(line=None, cell=''):
            if not line:
                print('Line commands are not evaluated.')
            self._display(self.qry(sql=cell))

        del spark_jdbc_qry_magic


class BambooLoader(LoaderPlugin):
    """Optional Class addition to Workspace that provides methods to interface with bamboolib
    This class requires prior knowledge of what variable name will be assigned to the instantiated workspace.
    This can not be determined dynamically, therefore the bamboolib generated code will not be accurate unless the
    class_variable_name provided at instantiation matches the user variable name assignment.
    """

    def __init__(self, handle, bamboo_ws_name, **kwargs):
        self._handle = handle if handle else bamboo_ws_name
        self._bamboo_ws_name = bamboo_ws_name
        self.name = f"{self._handle} Table Loader"
        self.new_df_name_placeholder = f"{self._handle}_df"
        super().__init__(**kwargs)
        self.database = Text(description=f"{self._handle} Database",
                             value="",
                             placeholder=None,
                             width="xl",
                             **kwargs)
        self.table = Text(description=f"{self._handle} Table",
                          value="",
                          placeholder=None,
                          width="xl",
                          **kwargs)

    def render(self):
        self.set_title(f"Load {self._handle} Table Data")
        self.set_content(
            widgets.HTML("Load WS Data"),
            self.database,
            self.table,
            self.new_df_name_group,
            self.execute_button,
        )

    def get_code(self):
        return f"""
        {DF_NEW} = {self._bamboo_ws_name}.qry("SELECT * FROM {'.'.join([self.database.value, self.table.value])}")
        """


class Migrate:
    _qry: Callable[[str], Pdf]
    _jdbc_spark_table: Callable[[str], Sdf]
    _catalog: str = None
    _database: str = None
    __spark: SparkSession = None

    def __init__(self,
                 qry: Callable[[str], Pdf],
                 jdbc_spark_table: Callable[[str], Sdf]):
        self._qry = qry
        self._jdbc_spark_table = jdbc_spark_table

    @property
    def catalog(self):
        return self._catalog

    @property
    def database(self):
        return self._database

    def config(self,
               catalog: str,
               database: str):
        self._catalog = catalog
        self._database = database

    @property
    def _spark(self):
        if self.__spark is None:
            from pyspark.sql import SparkSession
            self.__spark = SparkSession.builder.getOrCreate()
        return self.__spark

    def _cat_wh_tbl_name(self, tbl_name):
        if self.catalog is None:
            return '.'.join([self.database, tbl_name])
        else:
            return '.'.join([self.catalog, self.database, tbl_name])

    def get_source_tables(self):
        return list(self._qry("SELECT name FROM SYSOBJECTS WHERE xtype = 'U'")['name'])

    def _get_source_table_schema(self, tbl_name):
        sql = f"select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{tbl_name}'"
        return self._qry(sql)

    @staticmethod
    def field_mapper(row):
        # Returns tuple of name, type, nullable, comment
        if row.DATA_TYPE == 'bit':
            return row.COLUMN_NAME, T.BooleanType(), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE == 'tinyint':
            return row.COLUMN_NAME, T.ByteType(), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE == 'smallint':
            return row.COLUMN_NAME, T.ShortType(), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE == 'int':
            return row.COLUMN_NAME, T.IntegerType(), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE == 'bigint':
            return row.COLUMN_NAME, T.LongType(), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE in ['float', 'real']:
            return row.COLUMN_NAME, T.FloatType(), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE == 'double':
            return row.COLUMN_NAME, T.DoubleType(), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE in ['numeric', 'decimal', 'money', 'smallmoney']:
            return row.COLUMN_NAME, T.DecimalType(row.NUMERIC_PRECISION,
                                                  row.NUMERIC_SCALE), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE == 'date':
            return row.COLUMN_NAME, T.DateType(), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE in ['datetime', 'smalldatetime', 'timestamp']:
            return row.COLUMN_NAME, T.TimestampType(), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE in ['binary', 'varbinary', 'image']:
            return row.COLUMN_NAME, T.BinaryType(), row.IS_NULLABLE == 'YES', ''
        elif row.DATA_TYPE in ['varchar', 'nvarchar', 'char', 'nchar', 'text', 'ntext', 'time']:
            return row.COLUMN_NAME, T.StringType(), row.IS_NULLABLE == 'YES', ''
        else:
            return row.COLUMN_NAME, T.StringType(), row.IS_NULLABLE == 'YES', ''

    def create_target_table(self, tbl_name):
        dt = DeltaTable.createIfNotExists(self._spark).tableName(self._cat_wh_tbl_name(tbl_name))
        delta_field_list = [self.field_mapper(r) for i, r in self._get_source_table_schema(tbl_name).iterrows()]
        for c in delta_field_list:
            dt.addColumn(*c[:-1], comment=c[-1])
        dt.execute()

    def run_table_migrate(self, tbl_name):
        self.create_target_table(tbl_name)
        self._jdbc_spark_table(tbl_name).write.mode("overwrite") \
            .saveAsTable(self._cat_wh_tbl_name(tbl_name))


class Workspace(Displayer, ABC):
    """
    Workspace - base class for all three workspace types:
       - client (remote client session)
       - session (locally instantiated session)
       - connection (open connection to a long-lived service)
    """
    _kwargs: dict = {}
    _handle = None
    _commandLineInterface: CommandLineInterface = None
    _sparkJDBC: SparkJDBC = None
    _convert_tool: {} = None
    registered_magics = []

    def __init__(self, kwargs: {}, handle: str = None,
                 spark_jdbc: {} = None, cli_aliases: {} = None,
                 convert_tool: {} = None,
                 bamboo_loader=False, parent_name='', migrate_tools=False,
                 display_fn=None, displayHTML_fn=None):
        """
        kwargs are a dict of all necessary configurations for
        command, if provided, is the commandline used for terminal sessions
        """
        super().__init__(display_fn, displayHTML_fn)
        self._kwargs = kwargs
        self._handle = handle
        if spark_jdbc:
            self.spark_jdbc = SparkJDBC(spark_jdbc, handle)
        if cli_aliases:
            self.cli = CommandLineInterface(startup_file=cli_aliases['startup_file'],
                                            aliases=cli_aliases['aliases'])
        if convert_tool:
            self.convert_tool = convert_tool
        if bamboo_loader:
            self.bambooLoader = BambooLoader(self._handle, '.'.join([parent_name, self._handle]))
        if migrate_tools:
            pass
        self._register_magic()

    @property
    def handle(self):
        return self._handle

    @abstractmethod
    def _register_magic(self):
        """ Base code to register cell magics"""
        pass


class Duct(Displayer):
    """
    Duct - A single entry class for all workspaces to be configured within.

    In addition to just being a container class, duct provides a way to display all configured functionality
    via the show_workspaces() method. This is important because it will not only list all available magics
    and aliases, but it provides a hyperlink to a web-terminal which will a common interactive pattern for users.

    During instantiation the workspaces are defined as well as
    magics are created according to dsws conventions:
     - An un-argumented magic launches a cli session
     - An argumented magic accepts sql and returns
     a display of results. Intended for very concise
     iterations or summary results.
    """

    _ws: {str: Workspace} = {}
    _name: str

    def __init__(self, display_fn=None, displayHTML_fn=None, name='duct'):
        super().__init__(display_fn, displayHTML_fn)
        self._name = name

    @property
    def ws(self):
        return self._ws

    def show_interoperability(self):
        interop = []
        for ws_name, ws in self.ws.items():
            all_members = [m for m in inspect.getmembers(ws) if m[0][:1] != '_']
            # Get ws members
            ws_members = [m for m in all_members if m[0] not in ['cli', 'spark_jdbc', 'bambooLoader']]
            interop.extend([(ws_name, 'ipython', '.'.join([self._name, ws_name, m[0]])) for m in ws_members])
            # Get cli aliases
            for cli in [m[1] for m in all_members if m[0] == 'cli']:
                for a in list(cli.aliases):
                    interop.append((ws_name, 'Terminal', '$> ' + a['alias']))
            # Get magics
            interop.extend([(ws_name, 'ipython magic', magic) for magic in ws.registered_magics])
            # Get bamboo
            if 'bambooLoader' in [m[0] for m in all_members]:
                interop.append((ws_name, 'bamboolib', '.'.join([self._name, ws_name, 'bambooLoader'])))
            # Get spark_jdbc
            if 'spark_jdbc' in [m[0] for m in all_members]:
                interop.append((ws_name, 'bamboolib', "?" + '.'.join([self._name, ws_name, 'spark_jdbc'])))
        interop_ds = pd.DataFrame(interop, columns=['Workspace', 'Interface', 'Code'])
        interop_html = interop_ds.to_html(index=False)
        html = interop_html.replace('text-align: right', 'text-align: left')
        html = html.replace('<td>', '<td style="text-align: left;">')
        html = html.replace('\\n', '<br>')
        self._displayHTML(html)

    def add_ws(self,
               WS: type[Workspace],
               kwargs: {} = None,
               handle: str = '',
               spark_jdbc: {} = None,
               cli_aliases: {} = None,
               convert_tool: {} = None,
               bamboo_loader: bool = False,
               migrate_tools: bool = False):
        self._ws.update({handle: WS(kwargs=kwargs,
                                    handle=handle,
                                    spark_jdbc=spark_jdbc,
                                    cli_aliases=cli_aliases,
                                    convert_tool=convert_tool,
                                    bamboo_loader=bamboo_loader,
                                    parent_name=self._name,
                                    migrate_tools=migrate_tools,
                                    display_fn=self._display,
                                    displayHTML_fn=self._displayHTML)})
        setattr(self.__class__, handle, property(lambda p_self: p_self.ws[f'{handle}']))
