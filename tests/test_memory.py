import unittest
from unittest.mock import mock_open, patch
from src.memory import read_meminfo


class TestMemory(unittest.TestCase):

    def test_read_meminfo_valid(self):
        # Arrange
        fake_meminfo = """MemTotal:       8388608 kB
MemAvailable:   4194304 kB
"""

        # Act
        with patch("builtins.open", mock_open(read_data=fake_meminfo)):
            total, available = read_meminfo()

        # Assert
        self.assertEqual(total, 8.0)
        self.assertEqual(available, 4.0)

    def test_read_meminfo_missing_values(self):
        # Arrange
        fake_meminfo = """MemTotal:       8388608 kB"""

        # Act & Assert
        with patch("builtins.open", mock_open(read_data=fake_meminfo)):
            with self.assertRaises(ValueError):
                read_meminfo()

    def test_read_invalid_memory(self):
        # Arrange
        fake_meminfo = """MemTotal:       unknown kB
MemAvailable:   0 kB"""

        # Act & Assert
        with patch("builtins.open", mock_open(read_data=fake_meminfo)):
            with self.assertRaises(ValueError):
                read_meminfo()


if __name__ == "__main__":
    unittest.main()