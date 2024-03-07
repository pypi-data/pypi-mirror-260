import logging
import logging.config
import inspect
from pathlib import Path
import shutil
# from pathlib import Path

# Default values
## Paths
# DEFAULT_LOG_FOLDER:Path = Path('logs')
# DEFAULT_LOG_FILE:Path = Path('logs.txt')
# DEFAULT_LOG_CONF_FILE:Path = Path('ragtime_logging.json')
# FOLDER_EXPE:Path = Path('expe')
# FOLDER_AUTO_EVALS:Path = FOLDER_EXPE / Path('AutoEvals')
# FOLDER_HUMAN_EVALS:Path = FOLDER_EXPE / Path('HumanEvals')
# FOLDER_FACTS:Path = FOLDER_EXPE / Path('Facts')
# FOLDER_ANSWERS:Path = FOLDER_EXPE / Path('Answers')
# FOLDER_QUESTIONS:Path = FOLDER_EXPE / Path('Questions')
# FOLDER_RES:Path = Path('..') / '..' / 'res'
# FOLDER_SST_TEMPLATES:Path = FOLDER_RES  / 'spreadsheet_templates'
# FOLDER_HTML_TEMPLATES:Path = FOLDER_RES  / 'html_templates'

# # # HTML
# DEFAULT_HTML_RENDERING:dict[str,bool] = {"show_answers": True, "show_chunks": True, "show_facts": True, "show_evals": True}
# DEFAULT_HTML_TEMPLATE:Path = FOLDER_HTML_TEMPLATES / 'basic_template.jinja'

# # # Spreadheet
# DEFAULT_SPREADSHEET_TEMPLATE:Path = FOLDER_SST_TEMPLATES / 'basic_template.xlsx'
# DEFAULT_WORKSHEET:str = "Expe"
# DEFAULT_HEADER_SIZE:int = 2
# DEFAULT_QUESTION_COL:int = 2
# DEFAULT_FACTS_COL:int = 4
# DEFAULT_ANSWERS_COL:int = 9
# DEFAULT_HUMAN_EVAL_COL:int = 15

# # # LLMs
# DEFAULT_LITELLM_RETRIES:int = 3
# DEFAULT_LITELLM_TEMP:int = 0

# Logging - class to add msg
class RagtimeLogger(logging.LoggerAdapter):
    prefix:str = ""
    def process(self, msg, kwargs):
        return f'{self.prefix + " " if self.prefix else ""}{msg}', kwargs

# Logging - create the logs in the folder of the calling script (not ragtime)
# log_path:Path = Path(sys.argv[0]).parent / DEFAULT_LOG_FOLDER
# with open(log_path / DEFAULT_LOG_CONF_FILE, mode='r', encoding='utf-8') as f:
#     log_conf:dict = json.load(f)

# Change the output file with the correct folder
# log_conf['handlers']['file']['filename'] = str(log_path / DEFAULT_LOG_FILE)
# logging.config.dictConfig(log_conf)
logger:RagtimeLogger = None
# logger = RagtimeLogger(logging.getLogger("ragtime_logger"))

class RagtimeException(Exception):
    pass

def format_exc(msg: str) -> str:
    """Format the message for Exceptions - adds the call stack among other"""
    inspect_stack = inspect.stack()
    class_name:str = inspect_stack[1][0].f_locals["self"].__class__.__name__
    return f'[{class_name}.{inspect.stack()[1][3]}()] {msg}'

def div0(num:float, denom:float) -> float:
    return float(num/denom) if denom else 0.0

def init_project(path:Path = Path('.')):
    shutil.copytree(Path('..')/'base_folder', path)