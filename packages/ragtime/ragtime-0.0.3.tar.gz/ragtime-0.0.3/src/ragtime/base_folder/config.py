import logging
from pathlib import Path

from ragtime import RagtimeLogger
# This config file is used to setup : logging, default Expe folders, default Templates

####################
# LOGGING
# You can choose the file where the logs are written in "log_conf" dict, key "handlers"/"file"/"filename" - default is "logs/logs.txt"
# You can otherwise change everything you need as detailed in https://docs.python.org/3/library/logging.config.html

log_conf:dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s %(levelname)-4s %(filename)s %(funcName)s l.%(lineno)s] %(message)s"
            }
        },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream" : "ext://sys.stdout"
        },
        "file": {
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/logs.txt",
            "maxBytes": 1000000
        }
    },
    "loggers": {
        "ragtime_logger": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
            }
    }
}

####################
# DEFAULT FOLDERS
FOLDER_EXPE:Path = Path('expe')
FOLDER_AUTO_EVALS:Path = FOLDER_EXPE / Path('AutoEvals')
FOLDER_HUMAN_EVALS:Path = FOLDER_EXPE / Path('HumanEvals')
FOLDER_FACTS:Path = FOLDER_EXPE / Path('Facts')
FOLDER_ANSWERS:Path = FOLDER_EXPE / Path('Answers')
FOLDER_QUESTIONS:Path = FOLDER_EXPE / Path('Questions')
FOLDER_TEMPLATES:Path = Path('./res')
FOLDER_SST_TEMPLATES:Path = FOLDER_TEMPLATES  / 'spreadsheet_templates'
FOLDER_HTML_TEMPLATES:Path = FOLDER_TEMPLATES  / 'html_templates'

####################
# HTML TEMPLATES
DEFAULT_HTML_RENDERING:dict[str,bool] = {"show_answers": True, "show_chunks": True, "show_facts": True, "show_evals": True}
DEFAULT_HTML_TEMPLATE:Path = FOLDER_HTML_TEMPLATES / 'basic_template.jinja'

#######################
# SPREADSHEET TEMPLATES
DEFAULT_SPREADSHEET_TEMPLATE:Path = FOLDER_SST_TEMPLATES / 'basic_template.xlsx'
DEFAULT_WORKSHEET:str = "Expe"
DEFAULT_HEADER_SIZE:int = 2
DEFAULT_QUESTION_COL:int = 2
DEFAULT_FACTS_COL:int = 4
DEFAULT_ANSWERS_COL:int = 9
DEFAULT_HUMAN_EVAL_COL:int = 15

#######################
# LLMs
DEFAULT_LITELLM_RETRIES:int = 3
DEFAULT_LITELLM_TEMP:int = 0


### DON'T REMOVE THOSE 2 LINES
logging.config.dictConfig(log_conf)
logger = RagtimeLogger(logging.getLogger("ragtime_logger"))
### END DON'T REMOVE
