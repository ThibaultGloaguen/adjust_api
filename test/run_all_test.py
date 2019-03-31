import unittest
from test.api_metric_test import ApiMetricTestCase
from test.database_service_test import DatabaseServiceTest
import sys

if __name__ == '__main__':

    api = unittest.TestLoader().loadTestsFromTestCase(ApiMetricTestCase)
    db_service = unittest.TestLoader().loadTestsFromTestCase(DatabaseServiceTest)
    all_tests = unittest.TestSuite([api, db_service])
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    if result.wasSuccessful():
        sys.exit(0)
    sys.exit(-1)
