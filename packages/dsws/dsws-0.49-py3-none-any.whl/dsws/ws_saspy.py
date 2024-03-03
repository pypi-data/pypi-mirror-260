import subprocess
import sys
from .duct import Workspace
from IPython.core.magic import register_line_magic, register_cell_magic
from databricks_genai_inference import Completion
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter


class WS_saspy(Workspace):
    """
    Workspace class from the SASPy library

    Similar for other DSWS classes, the following class properties and methods are
    provided:
      - SASsession (property): a SASsession from configurations kwargs
      - run(run_cmd): executes a run command
      - qry: precesses a proc sql query, the return type is dependent upon r_type requested:
        - df (default): pandas dataframe
        - disp: pretty html form of pandas dataframe
        - log: text output of query
        - df_log: tuple of df and text log

    Configuring a Saspy class is typically done through `dsws.duct`, but can also be
        evaluated as:
        ```python
        from dsws.ws_saspy import Saspy
        kwargs = {'url':  spark.conf.get("spark.sas_url"),
                  'user': spark.conf.get("spark.sas_user"),
                  'pw':   spark.conf.get("spark.sas_pwd"),
                  'context': 'SAS Job Execution compute context',
                  'convert_completion_endpoint': 'completion.model.endpoint'}
        sas = Saspy(kwargs)
        ```
        SAS Sessions can time out, be aware that this happens, you will get a notice in terminal when
        it does happen and variables set in previous sessions will no longer be set."""

    _configured = False
    _session = None

    def _configure(self):
        """
        _configure will go through the library install and configuration
        once complete it will set self._configured
        """
        # Install saspy
        subprocess.check_call([sys.executable, "-m", "pip", "install", "saspy"])

        # assign path variable to our eventual personal config
        import saspy
        sascfg_personal_path = saspy.__file__.replace('__init__.py', 'sascfg_personal.py')

        # write config file
        sascfg_personal = f'SAS_config_names = [\'{self._handle}\']\n{self._handle}={str(self._kwargs)}'
        with open(sascfg_personal_path, 'w') as f:
            f.write(sascfg_personal)

    @property
    def session(self):
        """session property"""
        if not self._session:
            if not self._configured:
                self._configure()
            import saspy
            self._session = saspy.SASsession(results='HTML', context='SAS Job Execution compute context')
        return self._session

    def _register_magic(self):
        @register_cell_magic(self._handle)
        def submit_magic(line='', cell=''):
            """Executes cell text as if run in SAS environment. Add log|lst to magic prompt to change logging output"""
            args = [a.lower() for a in line.split(' ')]
            show_lst = False if 'log' in args and 'lst' not in args else True
            show_log: bool = True if 'log' in args else False
            c = self.session.submit(cell)
            if show_log:
                print(c['LOG'])
            if show_lst:
                try:
                    self._displayHTML(c['LST'])
                except NameError as err:
                    print('Global displayHTML function does not exist:' + str(err))
                    from IPython.core.display import HTML
                    from IPython.display import display
                    display(HTML(c['LST']))
            else:
                return None
        del submit_magic

        @register_line_magic(self._handle + '_file')
        def submit_file_magic(line=''):
            """Executes single file sas script in remote SAS environment"""
            args = [a.lower() for a in line.split(' ')]
            show_lst = False if 'log' in args and 'lst' not in args else True
            show_log = True if 'log' in args else False
            with open(args[0], 'r') as f:
                c = self.session.submit(f.read())
            if show_log:
                print(c['LOG'])
            if show_lst:
                try:
                    self._displayHTML(c['LST'])
                except NameError as err:
                    print('Global displayHTML function does not exist:' + str(err))
                    from IPython.core.display import HTML
                    from IPython.display import display
                    display(HTML(c['LST']))
            else:
                return None
        del submit_file_magic

        @register_cell_magic(self._handle + '_sql')
        def qry_magic(line='', cell=''):
            """Executes sql provided as PROC SQL and returns results"""
            if line != '':
                print('Line commands are not evaluated.')
            try:
                self._display(self.qry(sql=cell))
            except NameError as err:
                print('Global display function does not exist:' + str(err))
                from IPython.display import display as disp
                disp(self.qry(sql=cell))
        del qry_magic

        self.registered_magics = [f'%%{self._handle}',
                                  f'%{self._handle}_file',
                                  f'%%{self._handle}_sql']

        if self._convert_tool:
            @register_cell_magic(self._handle + '_convert')
            def convert_magic(line='', cell=''):
                """Executes sql provided as PROC SQL and returns results"""
                convert_tool = {"model": "DEMO_gpt_35_turbo_instruct_completions",
                                "prompt": 'Respond with only python code. ' +
                                          'Rewrite the following SAS code as python:\n{cell}',
                                "max_tokens": 1024}
                convert_tool.update(self._convert_tool)
                code = Completion.create(
                    model=convert_tool['model'],
                    prompt=convert_tool['prompt'].format(cell=cell),
                    max_tokens=convert_tool['max_tokens']).__getattribute__('text')[0]
                highlighted_code = highlight(code, PythonLexer(), TerminalFormatter())
                print(highlighted_code)

            self.registered_magics.append(f'%{self._handle}_convert')
            del convert_magic


    def qry(self, sql):
        # Create Pandas Dataframe from SAS SQL Statement
        self.session.submit(f"PROC SQL; CREATE TABLE WORK.qry_temp_dataset AS ({sql.replace(';','')});")
        return self.session.sasdata('qry_temp_dataset', libref='WORK', results='Pandas').to_df()
