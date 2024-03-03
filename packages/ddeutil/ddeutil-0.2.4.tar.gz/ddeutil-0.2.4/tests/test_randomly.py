import logging
import unittest
from unittest import mock

import ddeutil.core.base.hash as _hash


class RandomTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format="%(asctime)s %(module)s %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )

    def setUp(self) -> None:
        self.patcher = mock.patch("random.choices", return_value="AA145WQ2")
        self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_random_string(self):
        self.assertEqual(_hash.random_str(), "AA145WQ2")
