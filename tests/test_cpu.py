import unittest
from src.cpu import calculate_cpu_usage, get_cpu_usage
from unittest.mock import patch


class TestCPU(unittest.TestCase):

    def test_cpu_partially_busy(self):
        # Arrange
        first = [100, 0, 50, 850, 0, 0, 0, 0, 0, 0]
        second = [130, 0, 70, 950, 0, 0, 0, 0, 0, 0]

        result = calculate_cpu_usage(first, second)
        self.assertAlmostEqual(result, 33.33, places=2)

    def test_cpu_completely_idle(self):
        # Arrange
        first = [100, 0, 50, 850, 0, 0, 0, 0, 0, 0]
        second = [100, 0, 50, 950, 0, 0, 0, 0, 0, 0]

        result = calculate_cpu_usage(first, second)
        self.assertEqual(result, 0.0)

    def test_cpu_completely_busy(self):
        # Arrange
        first =  [100, 0, 50, 850, 0, 0, 0, 0, 0, 0]
        second = [160, 0, 90, 850, 0, 0, 0, 0, 0, 0]

        result = calculate_cpu_usage(first, second)
        self.assertEqual(result, 100.0)

    def test_cpu_no_elapsed_time(self):
        # Arrange
        first =  [100, 0, 50, 850, 0, 0, 0, 0, 0, 0]
        second = [100, 0, 50, 850, 0, 0, 0, 0, 0, 0]

        result = calculate_cpu_usage(first, second)
        self.assertEqual(result, 0.0)

    def test_cpu_test_io_wait(self):
        # Arrange
        first =  [100, 0, 50, 850, 0, 0, 0, 0, 0, 0]
        second = [150, 0, 50, 850, 50, 0, 0, 0, 0, 0]

        result = calculate_cpu_usage(first, second)
        self.assertAlmostEqual(result, 50, places=2)

    def test_get_cpu_usage(self):
        # Arrange
        first = [100, 0, 50, 850, 0, 0, 0, 0, 0, 0]
        second = [130, 0, 70, 950, 0, 0, 0, 0, 0, 0]

        # Act
        with patch("src.cpu.read_cpu_times", side_effect=[first, second]) as mock_read:
            with patch("src.cpu.time.sleep") as mock_sleep:
                result = get_cpu_usage()

        # Assert
        self.assertAlmostEqual(result, 33.33, places=2)
        self.assertEqual(mock_read.call_count, 2)
        mock_sleep.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()