import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def _has_export_command(path):
    if not os.path.isfile(path):
        return False
    with open(path) as f:
        content = f.read()
    return 'strawberry export-schema' in content


class DockerfileTest(unittest.TestCase):
    def test_user_service_dockerfile_has_export(self):
        path = os.path.join(BASE_DIR, 'user_service', 'Dockerfile')
        self.assertTrue(_has_export_command(path))

    def test_task_service_dockerfile_has_export(self):
        path = os.path.join(BASE_DIR, 'task_service', 'Dockerfile')
        self.assertTrue(_has_export_command(path))


if __name__ == '__main__':
    unittest.main()
