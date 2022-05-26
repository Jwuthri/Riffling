import unittest

from bionic_reading.features.bionic_reading import BionicReading


class TestBionicReading(unittest.TestCase):
    def test_html_correct(self):
        text = "We are happy if as many people as possible can use the advantage of Bionic Reading."
        expected_output = "<!DOCTYPE html><html><head><style>b {font-weight: 700} mark {color: red;} </style></head><body><p><b>W</b>e <b>ar</b>e <u>happy</u> <b>i</b>f <s>as</s> <b>ma</b>ny <u>people</u> <s>as</s> <b>possi</b>ble <b>ca</b>n <b>us</b>e <s>the</s> <u>advantage</u> <s>of</s> <u>Bionic</u> <u>Reading</u>.</p></body></html>"
        self.assertTrue(
            BionicReading(fixation=0.6, saccades=0.75, opacity=0.7, output_format="html").read_faster(text=text)
            == expected_output
        )

    def test_python_correct(self):
        text = "We are happy if as many people as possible can use the advantage of Bionic Reading."
        expected_output = "\x1b[1mW\x1b[0me \x1b[1mar\x1b[0me \x1b[4mhappy\x1b[0m \x1b[1mi\x1b[0mf a̶s̶ \x1b[1mma\x1b[0mny \x1b[4mpeople\x1b[0m a̶s̶ \x1b[1mpossi\x1b[0mble \x1b[1mca\x1b[0mn \x1b[1mus\x1b[0me t̶h̶e̶ \x1b[4madvantage\x1b[0m o̶f̶ \x1b[4mBionic\x1b[0m \x1b[4mReading\x1b[0m."
        self.assertTrue(
            BionicReading(fixation=0.6, saccades=0.75, opacity=0.7, output_format="python").read_faster(text=text)
            == expected_output
        )

    def test_html_incorrect(self):
        text = "We are happy if as many people as possible can use the advantage of Bionic Reading."
        expected_output = "<!DOCTYPE html><html><head><style>b {font-weight: 700} mark {color: red;} </style></head><body><p><b>W</b>e <b>ar</b>e <b>hap</b>py <b>i</b>f <b>a</b>s <b>ma</b>ny <b>peop</b>le <b>a</b>s <b>possi</b>ble <b>ca</b>n <b>us</b>e <s>the</s> <b>advan</b>tage <s>of</s> <b>Bion</b>ic <b>Read</b>ing.</p></body></html>"
        self.assertFalse(
            BionicReading(fixation=0.6, saccades=0.75, opacity=0.7, output_format="python").read_faster(text=text)
            == expected_output
        )

    def test_python_incorrect(self):
        text = "We are happy if as many people as possible can use the advantage of Bionic Reading."
        expected_output = "\x1b[1mW\x1b[0me \x1b[1mar\x1b[0me \x1b[1mhap\x1b[0mpy \x1b[1mi\x1b[0mf \x1b[1ma\x1b[0ms \x1b[1mma\x1b[0mny \x1b[1mpeop\x1b[0mle \x1b[1ma\x1b[0ms \x1b[1mpossi\x1b[0mble \x1b[1mca\x1b[0mn \x1b[1mus\x1b[0me t̶h̶e̶ \x1b[1madvan\x1b[0mtage o̶f̶ \x1b[1mBion\x1b[0mic \x1b[1mRead\x1b[0ming."
        self.assertFalse(
            BionicReading(fixation=0.6, saccades=0.75, opacity=0.7, output_format="html").read_faster(text=text)
            == expected_output
        )
