import unittest
from unittest.mock import Mock, patch
from io import StringIO

from main import main, run_diagnostics


class TestCLI(unittest.TestCase):

    def test_run_diagnostics_success(self):
        # Arrange
        mock_function = Mock()

        # Act
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            run_diagnostics("CPU Usage", mock_function)

        # Assert
        mock_function.assert_called_once()
        self.assertEqual(mock_stdout.getvalue(), "")

    def test_run_diagnostics_os_error(self):
        # Arrange
        mock_function = Mock(side_effect=OSError("File not found"))

        # Act
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            run_diagnostics("Memory Info", mock_function)

        # Assert
        mock_function.assert_called_once()
        self.assertIn(
            "[ERROR] Memory Info: File not found",
            mock_stderr.getvalue()
        )

    def test_run_diagnostics_value_error(self):
        # Arrange
        mock_function = Mock(side_effect=ValueError("Invalid data"))

        # Act
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            run_diagnostics("CPU Usage", mock_function)

        # Assert
        mock_function.assert_called_once()
        self.assertIn(
            "[ERROR] CPU Usage: Invalid data",
            mock_stderr.getvalue()
        )

    def test_run_diagnostics_index_error(self):
        # Arrange
        mock_function = Mock(side_effect=IndexError("Missing value"))

        # Act
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            run_diagnostics("Uptime", mock_function)

        # Assert
        mock_function.assert_called_once()
        self.assertIn(
            "[ERROR] Uptime: Missing value",
            mock_stderr.getvalue()
        )

    def test_run_diagnostics_unexpected_error(self):
        # Arrange
        mock_function = Mock(side_effect=TypeError("Unexpected bug"))

        # Act & Assert
        with self.assertRaises(TypeError):
            run_diagnostics("CPU Usage", mock_function)

        mock_function.assert_called_once()

    def test_default_scan(self):
        # Arrange
        with patch("sys.argv", ["main.py"]):
            with patch("main.print_cpu_usage") as mock_cpu, \
                 patch("main.print_meminfo") as mock_memory, \
                 patch("main.print_disk_usage") as mock_disk, \
                 patch("main.print_uptime") as mock_uptime, \
                 patch("sys.stdout", new_callable=StringIO):

                # Act
                main()

                # Assert
                mock_cpu.assert_called_once()
                mock_memory.assert_called_once()
                mock_disk.assert_called_once()
                mock_uptime.assert_called_once()

    def test_scan_command(self):
        # Arrange
        with patch("sys.argv", ["main.py", "scan"]):
            with patch("main.print_cpu_usage") as mock_cpu, \
                 patch("main.print_meminfo") as mock_memory, \
                 patch("main.print_disk_usage") as mock_disk, \
                 patch("main.print_uptime") as mock_uptime, \
                 patch("sys.stdout", new_callable=StringIO):

                # Act
                main()

                # Assert
                mock_cpu.assert_called_once()
                mock_memory.assert_called_once()
                mock_disk.assert_called_once()
                mock_uptime.assert_called_once()

    def test_cpu_command(self):
        # Arrange
        with patch("sys.argv", ["main.py", "cpu"]):
            with patch("main.print_cpu_usage") as mock_cpu, \
                 patch("main.print_meminfo") as mock_memory, \
                 patch("main.print_disk_usage") as mock_disk, \
                 patch("main.print_uptime") as mock_uptime, \
                 patch("sys.stdout", new_callable=StringIO):

                # Act
                main()

                # Assert
                mock_cpu.assert_called_once()
                mock_memory.assert_not_called()
                mock_disk.assert_not_called()
                mock_uptime.assert_not_called()

    def test_memory_command(self):
        # Arrange
        with patch("sys.argv", ["main.py", "memory"]):
            with patch("main.print_cpu_usage") as mock_cpu, \
                 patch("main.print_meminfo") as mock_memory, \
                 patch("main.print_disk_usage") as mock_disk, \
                 patch("main.print_uptime") as mock_uptime, \
                 patch("sys.stdout", new_callable=StringIO):

                # Act
                main()

                # Assert
                mock_memory.assert_called_once()
                mock_cpu.assert_not_called()
                mock_disk.assert_not_called()
                mock_uptime.assert_not_called()

    def test_disk_command(self):
        # Arrange
        with patch("sys.argv", ["main.py", "disk"]):
            with patch("main.print_cpu_usage") as mock_cpu, \
                 patch("main.print_meminfo") as mock_memory, \
                 patch("main.print_disk_usage") as mock_disk, \
                 patch("main.print_uptime") as mock_uptime, \
                 patch("sys.stdout", new_callable=StringIO):

                # Act
                main()

                # Assert
                mock_disk.assert_called_once()
                mock_cpu.assert_not_called()
                mock_memory.assert_not_called()
                mock_uptime.assert_not_called()

    def test_uptime_command(self):
        # Arrange
        with patch("sys.argv", ["main.py", "uptime"]):
            with patch("main.print_cpu_usage") as mock_cpu, \
                 patch("main.print_meminfo") as mock_memory, \
                 patch("main.print_disk_usage") as mock_disk, \
                 patch("main.print_uptime") as mock_uptime, \
                 patch("sys.stdout", new_callable=StringIO):

                # Act
                main()

                # Assert
                mock_uptime.assert_called_once()
                mock_cpu.assert_not_called()
                mock_memory.assert_not_called()
                mock_disk.assert_not_called()

    def test_invalid_command(self):
        # Arrange
        with patch("sys.argv", ["main.py", "invalid"]):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:

                # Act & Assert
                with self.assertRaises(SystemExit) as context:
                    main()

        self.assertEqual(context.exception.code, 2)
        self.assertIn("invalid choice", mock_stderr.getvalue())

    def test_scan_continues_after_error(self):
        # Arrange
        with patch("sys.argv", ["main.py", "scan"]):
            with patch(
                "main.print_cpu_usage",
                side_effect=OSError("CPU unavailable")
            ) as mock_cpu, \
                 patch("main.print_meminfo") as mock_memory, \
                 patch("main.print_disk_usage") as mock_disk, \
                 patch("main.print_uptime") as mock_uptime, \
                 patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                 patch("sys.stderr", new_callable=StringIO) as mock_stderr:

                # Act
                main()

                # Assert
                mock_cpu.assert_called_once()
                mock_memory.assert_called_once()
                mock_disk.assert_called_once()
                mock_uptime.assert_called_once()

                self.assertIn(
                    "[ERROR] CPU Usage: CPU unavailable",
                    mock_stderr.getvalue()
                )

                self.assertIn(
                    "ArchPulse - System Health",
                    mock_stdout.getvalue()
                )


if __name__ == "__main__":
    unittest.main()