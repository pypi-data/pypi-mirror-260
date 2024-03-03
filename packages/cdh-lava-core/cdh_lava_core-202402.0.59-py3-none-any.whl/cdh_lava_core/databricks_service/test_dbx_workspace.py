import unittest
from unittest.mock import MagicMock
from cdh_lava_core.databricks_service.dbx_workspace import DbxWorkspaceClient


class TestDbxWorkspaceClient(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.workspace_client = DbxWorkspaceClient(self.client)

    def test_ls(self):
        path = "/path/to/workspace"
        expected_result = [
            {"name": "notebook1", "object_type": "NOTEBOOK"},
            {"name": "directory1", "object_type": "DIRECTORY"},
        ]
        self.client.execute_get_json.return_value = {"objects": expected_result}

        result = self.workspace_client.ls(path)

        self.assertEqual(result, expected_result)
        self.client.execute_get_json.assert_called_once_with(
            f"{self.client.endpoint}/api/2.0/workspace/list?path={path}",
            expected=[200, 404],
        )

    def test_mkdirs(self):
        path = "/path/to/new/directory"
        expected_result = {"path": path}
        self.client.execute_post_json.return_value = expected_result

        result = self.workspace_client.mkdirs(path)

        self.assertEqual(result, expected_result)
        self.client.execute_post_json.assert_called_once_with(
            f"{self.client.endpoint}/api/2.0/workspace/mkdirs", {"path": path}
        )

    def test_delete_path(self):
        path = "/path/to/delete"
        expected_result = {"path": path}
        self.client.execute_post_json.return_value = expected_result

        result = self.workspace_client.delete_path(path)

        self.assertEqual(result, expected_result)
        self.client.execute_post_json.assert_called_once_with(
            f"{self.client.endpoint}/api/2.0/workspace/delete",
            {"path": path, "recursive": True},
            expected=[200, 404],
        )

    # Add more test cases for other methods...


if __name__ == "__main__":
    unittest.main()
