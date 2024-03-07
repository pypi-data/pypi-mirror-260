import os
import unittest

from yangsuite.paths import set_base_path
from ysrestconf.restconf import ParseRestconf


class TestAnsiblePlaybook(unittest.TestCase):
    """Test AnsiblePlaybook class for generating URL, body, and content"""
    @classmethod
    def setUpClass(cls):
        cls.testdir = os.path.join(os.path.dirname(__file__), 'data')
        cls.openapi_dir = os.path.join(cls.testdir, 'openapi')
        cls.playbooks_dir = os.path.join(cls.testdir, 'playbooks')
        cls.user = 'testrest'
        cls.proxyhost = 'localhost:8480'
        cls.devicename = 'CSR1K-7'

        set_base_path(cls.testdir)
        cls.filename = 'testscript.yaml'
        cls.task_name = 'testtask'
        cls.msg_name = 'testmsg'
        cls.xpath_value = 15
        cls.openapi_doc = {}

    def test_pagination(self):
        """Test pagination of paths."""

        mock_head = {'pageCount': 3}
        mock_paths = dict((i, i+1) for i in range(51))
        ParseRestconf.paths_per_page = 50
        ParseRestconf.cached_head['test_user'] = mock_head
        ParseRestconf.cached_paths['test_user'] = mock_paths

        # Page 0 -> 50 of 51 paths
        head = ParseRestconf.get_header(user='test_user', page=0)
        self.assertEqual(len(head['paths']), 50)

        # Page 1 -> 1 of 51 paths
        head = ParseRestconf.get_header(user='test_user', page=1)
        self.assertEqual(len(head['paths']), 1)

        mock_head = {'pageCount': 3}
        mock_paths = dict((i, i+1) for i in range(3))
        ParseRestconf.paths_per_page = 50
        ParseRestconf.cached_head['test_user'] = mock_head
        ParseRestconf.cached_paths['test_user'] = mock_paths

        # Page 0 -> 3 of 3 paths
        head = ParseRestconf.get_header(user='test_user', page=0)
        self.assertEqual(len(head['paths']), 3)
