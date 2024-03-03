import unittest
from dekgen.utils.yaml import yaml
from dekgen.utils.yaml.tags import tmpl_data_final
from dektools.output import pprint


class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_yaml(self):
        pprint(tmpl_data_final(yaml.load('./res/test.yaml')))
