import re
import string
import pandas as pd

from typing import List, Tuple
from sklearn.feature_extraction.text import CountVectorizer

from bionic_reading.data import stopwords_set
from bionic_reading.settings import RareBehavior, Format, Colors
from bionic_reading.utils.file_utils import string_contains_digit, strike_string
from bionic_reading.settings import SIMPLE_SPLITTER, OutputFormat, StopWordsBehavior


class BionicReading:
    """Read faster with your brain, not your eyes."""

    def __init__(
        self,
        fixation: float = 0.6,
        saccades: float = 0.75,
        opacity: float = 0.75,
        stopwords: float = 0.25,
        stopwords_behavior: str = StopWordsBehavior.STRIKETHROUGH.value,
        output_format: str = OutputFormat.HTML.value,
        rare_words_behavior: str = RareBehavior.UNDERLINE.value,
        rare_words_max_freq: int = 5,
        highlight_color: str = Colors.RED.value
    ):
        """
        Inits BionicReading

        :param fixation: Fixation you define the expression of the letter combinations
        :type fixation: float
        :param saccades: Saccades you define the visual jumps from fixation to fixation
        :type saccades: float
        :param opacity: Opacity you define the visibility of your fixation
        :type opacity: float
        :param stopwords: Determine whether the list of stopwords is long or not
        :type stopwords: float
        :param stopwords_behavior: Change the way the stopwords are handled (remove, ignore, keep)
        :type stopwords_behavior: str
        :param output_format: The format of the output (html, python)
        :type output_format: str
        :param rare_words_behavior: Change the way the rare words are handled (highlight, underline)
        :type rare_words_behavior: str
        :param rare_words_max_freq: Max frequency word to be considered as rare
        :type rare_words_max_freq: int
        :param highlight_color: Color that highlight the text
        :type highlight_color: str
        """
        self.fixation = fixation
        self.saccades = saccades
        self.opacity = opacity
        self.stopwords = stopwords
        self.output_format = output_format
        self.stopwords_behavior = stopwords_behavior
        self.rare_words_behavior = rare_words_behavior
        self.rare_words_max_freq = rare_words_max_freq
        self.highlight_color = highlight_color
        self.non_tokens = string.punctuation + " \n\t"

    @property
    def fixation(self):
        """
        It returns the fixation of the object.
        :return: The fixation is being returned.
        """
        return self._fixation

    @fixation.setter
    def fixation(self, value: float):
        """
        This function takes a float value and checks that it is between 0 and 1. If it is, it sets the value of the fixation
        attribute to the value passed in

        :param value: the value of the parameter
        :type value: float
        """
        assert isinstance(value, float), "please use a fixation float type"
        assert 0 <= value <= 1, "please enter a fixation value between 0 and 1"
        self._fixation = value

    @fixation.deleter
    def fixation(self):
        """
        It deletes the fixation attribute of the object.
        """
        del self._fixation

    @property
    def saccades(self):
        """
        This function returns the saccades of the current trial
        :return: The saccades are being returned.
        """
        return self._saccades

    @saccades.setter
    def saccades(self, value: float):
        """
        This function takes a float value between 0 and 1 and assigns it to the saccades attribute

        :param value: the value of the parameter
        :type value: float
        """
        assert isinstance(value, float), "please use a saccades float type"
        assert 0 <= value <= 1, "please enter a saccades value between 0 and 1"
        self._saccades = value

    @saccades.deleter
    def saccades(self):
        """
        It deletes the attribute `_saccades` from the object `self`
        """
        del self._saccades

    @property
    def opacity(self):
        """
        It returns the opacity of the object.
        :return: The opacity of the object.
        """
        return self._opacity

    @opacity.setter
    def opacity(self, value: float):
        """
        This function takes in a float value and checks if it is between 0 and 1. If it is, it sets the opacity to that
        value

        :param value: The value of the parameter
        :type value: float
        """
        assert isinstance(value, float), "please use a opacity float type"
        assert 0 <= value <= 1, "please enter an opacity value between 0 and 1"
        self._opacity = value

    @opacity.deleter
    def opacity(self):
        """
        It deletes the opacity attribute of the object.
        """
        del self._opacity

    @property
    def stopwords_behavior(self):
        """
        This function returns the stopwords behavior of the tokenizer
        :return: The stopwords_behavior is being returned.
        """
        return self._stopwords_behavior

    @stopwords_behavior.setter
    def stopwords_behavior(self, value: str):
        """
        The function takes in a string value and checks to see if it's a valid stopwords_behavior. If it is, it sets the
        stopwords_behavior to that value

        :param value: the value to be checked
        :type value: str
        """
        possible_values = [behavior.value.lower() for behavior in StopWordsBehavior]
        assert isinstance(value, str), "please use a stopwords_behavior str type"
        assert value in possible_values, f"please enter a stopwords_behavior within {possible_values}"
        self._stopwords_behavior = value

    @stopwords_behavior.deleter
    def stopwords_behavior(self):
        """
        It deletes the stopwords_behavior attribute from the object
        """
        del self._stopwords_behavior

    @property
    def stopwords(self):
        """
        The function stopwords() returns the stopwords of the object
        :return: The stopwords are being returned.
        """
        return self._stopwords

    @stopwords.setter
    def stopwords(self, value: float):
        """
        If the value is less than or equal to 1/4, then the stopwords set is very light. If the value is less than or equal
        to 1/2, then the stopwords set is light. If the value is less than or equal to 3/4, then the stopwords set is
        normal. Otherwise, the stopwords set is strong

        :param value: the value of the stopwords parameter
        :type value: float
        """
        assert isinstance(value, float), "please use a stopwords float type"
        assert 0 <= value <= 1, "please enter a stopwords value between 0 and 1"
        self._stopwords = (
            stopwords_set.VERY_LIGHT_STOPWORDS_SET
            if value <= 1 / 4
            else stopwords_set.LIGHT_STOPWORDS_SET
            if value <= 1 / 2
            else stopwords_set.NORMAL_STOPWORDS_SET
            if value <= 3 / 4
            else stopwords_set.STRONG_STOPWORDS_SET
        )

    @stopwords.deleter
    def stopwords(self):
        """
        It deletes the stopwords attribute of the object
        """
        del self._stopwords

    @property
    def output_format(self):
        """
        It returns the output format of the object
        :return: The output format of the file.
        """
        return self._output_format

    @output_format.setter
    def output_format(self, value: str):
        """
        The function takes in a string value and checks if it is a valid output format. If it is, it sets the output format
        to that value

        :param value: the value that the parameter will be set to
        :type value: str
        """
        possible_values = [output.value.lower() for output in OutputFormat]
        assert isinstance(value, str), "please use a output_format str type"
        assert value in possible_values, f"please enter a output_format within {possible_values}"
        self._output_format = value

    @output_format.deleter
    def output_format(self):
        """
        It deletes the output format attribute from the object
        """
        del self._output_format

    @property
    def rare_words_behavior(self):
        """
        This function returns the value of the private variable _rare_words_behavior
        :return: The rare_words_behavior is being returned.
        """
        return self._rare_words_behavior

    @rare_words_behavior.setter
    def rare_words_behavior(self, value: str):
        """
        The function takes in a string value and checks if it is a valid string and if it is a valid string, it sets the
        value of the rare_words_behavior attribute to the value of the string

        :param value: the value to be replaced
        :type value: str
        """
        possible_values = [behavior.value.lower() for behavior in RareBehavior]
        assert isinstance(value, str), "please use a rare_words_behavior str type"
        assert value in possible_values, f"please enter a rare_words_behavior within {possible_values}"
        self._rare_words_behavior = value

    @rare_words_behavior.deleter
    def rare_words_behavior(self):
        """
        It deletes the rare_words_behavior attribute from the object.
        """
        del self._rare_words_behavior

    @property
    def rare_words_max_freq(self):
        """
        This function returns the maximum frequency of a rare word
        :return: The rare_words_max_freq is being returned.
        """
        return self._rare_words_max_freq

    @rare_words_max_freq.setter
    def rare_words_max_freq(self, value: int):
        """
        This function takes in a value and checks if it is an integer. If it is, it sets the value of the
        rare_words_max_freq variable to the value that was passed in

        :param value: The value of the parameter
        :type value: int
        """
        assert isinstance(value, int), "please use a rare_words_max_freq int type"
        self._rare_words_max_freq = value

    @rare_words_max_freq.deleter
    def rare_words_max_freq(self):
        """
        It deletes the rare_words_max_freq attribute from the object.
        """
        del self._rare_words_max_freq

    @property
    def highlight_color(self):
        """
        It returns the highlight color of the object.
        :return: The highlight color.
        """
        return self._highlight_color

    @highlight_color.setter
    def highlight_color(self, value):
        """
        `highlight_color` is a function that takes in a `self` and a `value` argument. It then creates a list of possible
        values that can be passed into the function. It then asserts that the value passed into the function is in the list
        of possible values. It then asserts that the value passed into the function is a string. It then sets the
        `_highlight_color` attribute to the value passed into the function

        :param value: the value of the parameter
        """
        possible_values = [color.value.lower() for color in Colors]
        assert value in possible_values, f"please enter a highlight_color within {possible_values}"
        assert isinstance(value, str), "please use a highlight_color str type"
        self._highlight_color = value

    @highlight_color.deleter
    def highlight_color(self):
        """
        It deletes the attribute _highlight_color from the object self.
        """
        del self._highlight_color

    def get_rare_words(self, text: str) -> List[str]:
        """
        Takes a string of text, and returns a list of words that appear more than a certain number of times in the text

        :param text: The text to be analyzed
        :type text: str
        :return: A list of uncommon words
        """
        vectorizer = CountVectorizer(stop_words=stopwords_set.STRONG_STOPWORDS_SET)
        transformed = vectorizer.fit_transform([text])
        data = pd.DataFrame(transformed.toarray(), columns=vectorizer.get_feature_names_out()).T
        data.columns = ["freq"]
        uncommon_words = data[data["freq"] <= self.rare_words_max_freq].index.tolist()
        uncommon_words = [word for word in uncommon_words if not string_contains_digit(word)]

        return uncommon_words

    @staticmethod
    def split_text_to_words(text: str) -> List[str]:
        """
        It splits a string into a list of words

        :param text: The text to split into words
        :type text: str
        :return: A list of strings
        """
        tokens = re.split(SIMPLE_SPLITTER, text)

        return [token for token in tokens if len(token) > 0]

    def opacity_highlight(self, token: str, highlight_format: str = Format.BOLD.value) -> str:
        """
        If the output format is HTML, then return the HTML tag for the given format. Otherwise, return the ANSI escape code
        for the given format

        :param token: The token to be highlighted
        :type token: str
        :param highlight_format: This is the format that you want to highlight the token with
        :type highlight_format: str
        :return: A string with the token in the specified format.
        """
        if self.output_format == OutputFormat.HTML.value:
            if highlight_format == Format.HIGHLIGHT.value:
                return f"<mark>{token}</mark>"
            elif highlight_format == Format.UNDERLINE.value:
                return f"<u>{token}</u>"
            elif highlight_format == Format.STRIKETHROUGH.value:
                return f"<s>{token}</s>"
            else:
                return f"<b>{token}</b>"
        else:
            if highlight_format == Format.HIGHLIGHT.value:
                return f"\033[93m{token}\033[0m"
            elif highlight_format == Format.UNDERLINE.value:
                return f"\033[4m{token}\033[0m"
            elif highlight_format == Format.STRIKETHROUGH.value:
                return strike_string(token)
            else:
                return f"\033[1m{token}\033[0m"

    def fixation_highlight(self, token: str) -> Tuple[str, str]:
        """
        It takes a string and returns a tuple of two strings. The first string is the part of the string that should be
        highlighted, and the second string is the part of the string that should not be highlighted

        :param token: the string to be highlighted
        :type token: str
        :return: The first return value is the part of the token that has been read, and the second return value is the
        part of the token that has not been read.
        """
        if len(token) <= 2:
            return token[0], token[1:]
        last_char_index = round(self.fixation * len(token))

        return token[:last_char_index], token[last_char_index:]

    def saccades_highlight(self) -> int:
        """
        If the saccades are less than 1/3, return 3, else if the saccades are less than 2/3, return 2, else return 1
        :return: an integer value.
        """
        return 3 if self.saccades < 1 / 3 else 2 if self.saccades < 2 / 3 else 1

    def stopwords_highlight(self, token: str) -> str:
        """
        If the stopwords behavior is set to remove, return an empty string, otherwise return the token

        :param token: The token to highlight
        :type token: str
        """
        if self.stopwords_behavior == StopWordsBehavior.REMOVE.value:
            return ""
        elif self.stopwords_behavior == StopWordsBehavior.STRIKETHROUGH.value:
            return self.opacity_highlight(token, self.stopwords_behavior)
        else:
            return token

    def rare_words_highlight(self, token: str) -> str:
        """
        If the token is a rare word, then return the token with the opacity set to the value of the rare_words_behavior
        attribute

        :param token: the token to highlight
        :type token: str
        :return: The opacity_highlight function is being returned.
        """
        return self.opacity_highlight(token, self.rare_words_behavior)

    def highlight_tokens(self, tokens: List[str], uncommon_words: List[str]) -> List[str]:
        """
        The function takes a list of tokens and an output format, and returns a list of tokens with the tokens that are
        highlighted

        :param tokens: a list of tokens to highlight
        :type tokens: List[str]
        :param uncommon_words: List of all uncommon words
        :type uncommon_words: List[str]
        :return: A list of tokens with the tokens that are highlighted.
        """
        index = 0
        highlighted_tokens = []
        for token in tokens:
            if token not in self.non_tokens:
                index += 1
                if token.isdigit():
                    pass
                elif token.lower() in uncommon_words:
                    token = self.rare_words_highlight(token)
                elif token in self.stopwords and self.stopwords_behavior not in (
                    StopWordsBehavior.HIGHLIGHT.value,
                    StopWordsBehavior.BOLD.value,
                ):
                    token = self.stopwords_highlight(token)
                    index -= 1
                elif index % self.saccades_highlight() == 0 or index == 1:
                    (
                        token_to_highlight,
                        token_not_to_highlight,
                    ) = self.fixation_highlight(token)
                    if token in self.stopwords:
                        token_to_highlight = self.opacity_highlight(token_to_highlight, self.stopwords_behavior)
                    else:
                        token_to_highlight = self.opacity_highlight(token_to_highlight)
                    token = token_to_highlight + token_not_to_highlight
            highlighted_tokens.append(token)

        return highlighted_tokens

    @staticmethod
    def tokens_to_text(tokens: List[str]) -> str:
        """
        It takes a list of tokens and returns a string

        :param tokens: A list of tokens
        :type tokens: List[str]
        :return: A string of the tokens joined together.
        """
        return "".join(tokens)

    def to_output_format(self, text: str) -> str:
        """
        If the output format is HTML, then add the HTML tags to the highlighted text

        :param text: The text to be highlighted
        :type text: str
        :return: The highlighted text.
        """
        output = text
        if self.output_format == OutputFormat.HTML.value:
            style = "b {font-weight: %d} " % (self.opacity * 1000)
            style += "mark {color: %s} " % self.highlight_color
            output = f"<!DOCTYPE html><html><head><style>{style}</style></head><body><p>{text}</p></body></html>"

        return output

    def read_faster(
        self,
        text: str,
    ) -> str:
        """
        The function takes a string of text, splits it into a list of words, highlights the words, and then returns the
        highlighted text

        :param text: the text you want to read faster
        :type text: str
        :return: The highlighted text
        """
        tokens = self.split_text_to_words(text)
        uncommon_words = self.get_rare_words(text)
        highlighted_tokens = self.highlight_tokens(tokens, uncommon_words)
        highlighted_text = self.tokens_to_text(highlighted_tokens)

        return self.to_output_format(highlighted_text)


if __name__ == "__main__":
    _text = """
    transduction problems such as language modeling and machine translation [35, 2, 5]. Numerous
efforts have since continued to push the boundaries of recurrent language models and encoder-decoder
architectures [38, 24, 15].
Recurrent models typically factor computation along the symbol positions of the input and output
sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden
states ht, as a function of the previous hidden state ht−1 and the input for position t. This inherently
sequential nature precludes parallelization within training examples, which becomes critical at longer
sequence lengths, as memory constraints limit batching across examples. Recent work has achieved
significant improvements in computational efficiency through factorization tricks [21] and conditional
computation [32], while also improving model performance in case of the latter. The fundamental
constraint of sequential computation, however, remains.
Attention mechanisms have become an integral part of compelling sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in
the input or output sequences [2, 19]. In all but a few cases [27], however, such attention mechanisms
are used in conjunction with a recurrent network.
In this work we propose the Transformer, a model architecture eschewing recurrence and instead
relying entirely on an attention mechanism to draw global dependencies between input and output.
The Transformer allows for significantly more parallelization and can reach a new state of the art in
translation quality after being trained for as little as twelve hours on eight P100 GPUs.
2 Background
The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU
[16], ByteNet [18] and ConvS2S [9], all of which use convolutional neural networks as basic building
block, computing hidden representations in parallel for all input and output positions. In these models,
the number of operations required to relate signals from two arbitrary input or output positions grows
in the distance between positions, linearly for ConvS2S and logarithmically for ByteNet. This makes
it more difficult to learn dependencies between distant positions [12]. In the Transformer this is
reduced to a constant number of operations, albeit at the cost of reduced effective resolution due
to averaging attention-weighted positions, an effect we counteract with Multi-Head Attention as
described in section 3.2.
Self-attention, sometimes called intra-attention is an attention mechanism relating different positions
of a single sequence in order to compute a representation of the sequence. Self-attention has been
used successfully in a variety of tasks including reading comprehension, abstractive summarization,
textual entailment and learning task-independent sentence representations [4, 27, 28, 22].
End-to-end memory networks are based on a recurrent attention mechanism instead of sequencealigned recurrence and have been shown to perform well on simple-language question answering and
language modeling tasks [34].
To the best of our knowledge, however, the Transformer is the first transduction model relying
entirely on self-attention to compute representations of its input and output without using sequencealigned RNNs or convolution. In the following sections, we will describe the Transformer, motivate
self-attention and discuss its advantages over models such as [17, 18] and [9].
3 Model Architecture
Most competitive neural sequence transduction models have an encoder-decoder structure [5, 2, 35].
Here, the encoder maps an input sequence of symbol representations (x1, ..., xn) to a sequence
of continuous representations z = (z1, ..., zn). Given z, the decoder then generates an output
sequence (y1, ..., ym) of symbols one element at a time. At each step the model is auto-regressive
[10], consuming the previously generated symbols as additional input when generating the next.
The Transformer follows this overall architecture using stacked self-attention and point-wise, fully
connected layers for both the encoder and decoder, shown in the left and right halves of Figure 1,
respectively.
    """
    _ = BionicReading(
        fixation=0.6,
        saccades=0.75,
        opacity=0.7,
        output_format="python",
        rare_words_behavior=RareBehavior.HIGHLIGHT.value,
        rare_words_max_freq=1,
    ).read_faster(text=_text)
    print(_text)
    print("*" * 20)
    print(_)
