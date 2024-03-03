import datetime
import unittest

import ddeutil.core.dtutils as dtutils


class DtutilsTestCase(unittest.TestCase):
    def test_get_date(self):
        self.assertEqual(
            datetime.datetime.now(tz=dtutils.LOCAL_TZ).date(),
            dtutils.get_date("date"),
        )
