import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class SchemaFilesTest(unittest.TestCase):
    def test_user_schema_exists(self):
        path = os.path.join(BASE_DIR, 'user_service', 'schema', 'schema.graphql')
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
            self.assertIn('type User', content)

    def test_task_schema_exists(self):
        path = os.path.join(BASE_DIR, 'task_service', 'schema', 'schema.graphql')
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
            self.assertIn('type Task', content)


if __name__ == '__main__':
    unittest.main()
