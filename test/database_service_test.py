import os
import unittest
from application.metrics_model import Metrics
from application.database_service import select_fields, select_group_by_fields


class DatabaseServiceTest(unittest.TestCase):
    def test_select_fields(self):
        fields = "cpi,impressions"
        res = select_fields(fields)
        self.assertIn(Metrics.cpi, res)
        self.assertIn(Metrics.impressions, res)

    def test_select_fields_empty_field(self):
        fields = None
        res = select_fields(fields)
        self.assertEqual(res[0], Metrics.impressions)
        self.assertEqual(res[1], Metrics.clicks)
        self.assertEqual(res[2], Metrics.installs)
        self.assertEqual(res[3], Metrics.spend)
        self.assertEqual(res[4], Metrics.revenue)

    def test_select_fields_unknown(self):

        try:
            res = select_fields('unknown')
            self.fail('shall fail')
        except ValueError as e:
            self.assertEqual(e.args[0], "Cannot select the fields unknown")

    def test_select_groupby_fields(self):
        fields = "date,os"
        res = select_group_by_fields(fields)
        self.assertIn(Metrics.date, res)
        self.assertIn(Metrics.os, res)

    def test_select_fields_groupby_empty_field(self):
        fields = None
        res = select_group_by_fields(fields)
        self.assertEqual(res, None)

    def test_select_fields_groupby_unknown(self):
        try:
            res = select_group_by_fields('unknown')
            self.fail('shall fail')
        except ValueError as e:
            self.assertEqual(e.args[0], "Cannot group by with the fields unknown")


if __name__ == "__main__":
    unittest.main()
