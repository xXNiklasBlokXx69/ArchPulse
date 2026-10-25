import unittest
from unittest.mock import mock_open, patch
from src.disk import get_disk_usage

from collections import namedtuple

DiskUsage = namedtuple("DiskUsage", ["total", "used", "free", "percent"])


class TestDisk(unittest.TestCase):
    def test_get_disk_usage(self):
        #Arrange
        fake_usage = DiskUsage(
            total=100 * 1024**3,
            used=40 * 1024**3,
            free=60 * 1024**3,
            percent=40.0
        ) 
        #Act
        with patch("psutil.disk_usage", return_value=fake_usage):
            total, used, free, disk_utilization = get_disk_usage()
        #Assert
        self.assertAlmostEqual(total, 100.0, places=2)
        self.assertAlmostEqual(used, 40.0, places=2)
        self.assertAlmostEqual(free, 60.0, places=2)
        self.assertAlmostEqual(disk_utilization, 40.0, places=2)

    def test_get_disk_usage_empty_disk(self):
        #Arrange
        fake_usage = DiskUsage(
            total=100 * 1024**3,
            used=0,
            free=100 * 1024**3,
            percent=0.0
        ) 
        #Act
        with patch("psutil.disk_usage", return_value=fake_usage):
            total, used, free, disk_utilization = get_disk_usage()
        #Assert
        self.assertEqual(total, 100.0)
        self.assertEqual(used, 0.0)
        self.assertEqual(free, 100.0)
        self.assertEqual(disk_utilization, 0.0)

    def test_get_disk_usage_full_disk(self):
        #Arrange
        fake_usage = DiskUsage(
            total=100 * 1024**3,
            used=100 * 1024**3,
            free=0,
            percent=100.0
        ) 
        #Act
        with patch("psutil.disk_usage", return_value=fake_usage):
            total, used, free, disk_utilization = get_disk_usage()
        #Assert
        self.assertEqual(total, 100.0)
        self.assertEqual(used, 100.0)
        self.assertEqual(free, 0.0)
        self.assertEqual(disk_utilization, 100.0)

    def test_get_disk_usage_information_refreshes(self):
        first_usage = DiskUsage(
        total=100 * 1024**3,
        used=40 * 1024**3,
        free=60 * 1024**3,
        percent=40.0
        )

        second_usage = DiskUsage(
            total=100 * 1024**3,
            used=70 * 1024**3,
            free=30 * 1024**3,
            percent=70.0
        )
        with patch("psutil.disk_usage", side_effect=[first_usage, second_usage]) as mock_disk:
            result1 = get_disk_usage()
            result2  = get_disk_usage()

            self.assertEqual(result1, (100.0, 40.0, 60.0, 40.0))
            self.assertEqual(result2, (100.0, 70.0, 30.0, 70.0))
            self.assertEqual(mock_disk.call_count, 2)
            mock_disk.assert_any_call("/")


if __name__ == "__main__":
    unittest.main()