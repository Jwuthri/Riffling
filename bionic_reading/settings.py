import os
from enum import Enum


SIMPLE_SPLITTER = "([\t\] \n-.!?;:(){}'/[])"


class OutputFormat(Enum):
    PYTHON = "python"
    TEXT = "text"
    HTML = "html"


class StopWordsBehavior(Enum):
    STRIKETHROUGH = "strikethrough"
    HIGHLIGHT = "highlight"
    REMOVE = "remove"
    IGNORE = "ignore"
    BOLD = "bold"


class RareBehavior(Enum):
    HIGHLIGHT = "highlight"
    UNDERLINE = "underline"
    BOLD = "bold"


class Format(Enum):
    STRIKETHROUGH = "strikethrough"
    HIGHLIGHT = "highlight"
    UNDERLINE = "underline"
    BOLD = "bold"


# ROOT PATH
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PROJECT_PATH)

# DATA PATH
DATASET_PATH = os.path.join(PROJECT_ROOT, "data")
ASSETS_DATA_PATH = os.path.join(DATASET_PATH, "assets_data")

# ASSETS PATH
VERY_LIGHT_STOPWORDS_PATH = os.path.join(ASSETS_DATA_PATH, "VERY_LIGHT_STOPWORDS.json")
LIGHT_STOPWORDS_PATH = os.path.join(ASSETS_DATA_PATH, "LIGHT_STOPWORDS.json")
NORMAL_STOPWORDS_PATH = os.path.join(ASSETS_DATA_PATH, "NORMAL_STOPWORDS.json")
STRONG_STOPWORDS_PATH = os.path.join(ASSETS_DATA_PATH, "STRONG_STOPWORDS.json")
