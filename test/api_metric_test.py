import os
import unittest
from application import create_app


class ApiMetricTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.app.root_path + '/../metrics.db'
        self.client = self.app.test_client

    def test_get_metrics(self):
        rv = self.client().get('/metrics')
        self.assertEqual(rv.status_code, 200)



if __name__ == "__main__":
    unittest.main()
