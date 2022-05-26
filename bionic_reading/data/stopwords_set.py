from bionic_reading.settings import VERY_LIGHT_STOPWORDS_PATH, LIGHT_STOPWORDS_PATH
from bionic_reading.settings import STRONG_STOPWORDS_PATH, NORMAL_STOPWORDS_PATH
from bionic_reading.utils.json_utils import read_text_file


VERY_LIGHT_STOPWORDS_SET = read_text_file(VERY_LIGHT_STOPWORDS_PATH, to_object=True)
LIGHT_STOPWORDS_SET = read_text_file(LIGHT_STOPWORDS_PATH, to_object=True)
NORMAL_STOPWORDS_SET = read_text_file(NORMAL_STOPWORDS_PATH, to_object=True)
STRONG_STOPWORDS_SET = read_text_file(STRONG_STOPWORDS_PATH, to_object=True)
