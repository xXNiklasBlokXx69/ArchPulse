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
    # Test successful individual command exit code
    def test_cpu_success_exit_code(self):
        with patch("sys.argv", ["main.py", "cpu"]), \
             patch("main.print_cpu_usage"), \
             patch("sys.stdout", new_callable=StringIO):

            result = main()

        self.assertEqual(result, 0)

    # Test failed individual command exit code
    def test_cpu_failed_exit_code(self):
        with patch("sys.argv", ["main.py", "cpu"]), \
             patch("main.print_cpu_usage", side_effect=OSError("CPU unavailable")), \
             patch("sys.stdout", new_callable=StringIO), \
             patch("sys.stderr", new_callable=StringIO) as mock_stderr:

            result = main()

        self.assertEqual(result, 1)
        self.assertIn("CPU unavailable", mock_stderr.getvalue())

    # Test other individual command exit codes
    def test_other_commands_success_exit_codes(self):
        commands = {
            "memory": "print_meminfo",
            "disk": "print_disk_usage",
            "uptime": "print_uptime"
        }

        for command, function in commands.items():
            with self.subTest(command=command):
                with patch("sys.argv", ["main.py", command]), \
                     patch(f"main.{function}"), \
                     patch("sys.stdout", new_callable=StringIO):

                    result = main()

                self.assertEqual(result, 0)

    def test_other_commands_failed_exit_codes(self):
        commands = {
            "memory": "print_meminfo",
            "disk": "print_disk_usage",
            "uptime": "print_uptime"
        }

        for command, function in commands.items():
            with self.subTest(command=command):
                with patch("sys.argv", ["main.py", command]), \
                     patch(f"main.{function}", side_effect=ValueError("Invalid data")), \
                     patch("sys.stdout", new_callable=StringIO), \
                     patch("sys.stderr", new_callable=StringIO):

                    result = main()

                self.assertEqual(result, 1)

    # Test successful full scan
    def test_scan_success_exit_code(self):
        with patch("sys.argv", ["main.py", "scan"]), \
             patch("main.print_cpu_usage"), \
             patch("main.print_meminfo"), \
             patch("main.print_disk_usage"), \
             patch("main.print_uptime"), \
             patch("sys.stdout", new_callable=StringIO):

            result = main()

        self.assertEqual(result, 0)

    # Test scan failure while continuing other diagnostics
    def test_scan_failed_exit_code(self):
        with patch("sys.argv", ["main.py", "scan"]), \
             patch("main.print_cpu_usage", side_effect=OSError("CPU unavailable")) as mock_cpu, \
             patch("main.print_meminfo") as mock_memory, \
             patch("main.print_disk_usage") as mock_disk, \
             patch("main.print_uptime") as mock_uptime, \
             patch("sys.stdout", new_callable=StringIO), \
             patch("sys.stderr", new_callable=StringIO):

            result = main()

        self.assertEqual(result, 1)
        mock_cpu.assert_called_once()
        mock_memory.assert_called_once()
        mock_disk.assert_called_once()
        mock_uptime.assert_called_once()

    # Test successful JSON report
    def test_report_success_exit_code(self):
        with patch("sys.argv", ["main.py", "report", "--output", "test.json"]), \
             patch("main.collect_system_info", return_value={"cpu": {}}) as mock_collect, \
             patch("main.save_report") as mock_save, \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:

            result = main()

        self.assertEqual(result, 0)
        mock_collect.assert_called_once()
        mock_save.assert_called_once_with({"cpu": {}}, "test.json")
        self.assertIn("Report saved to test.json", mock_stdout.getvalue())

    # Test failed JSON report
    def test_report_failed_exit_code(self):
        with patch("sys.argv", ["main.py", "report"]), \
             patch("main.collect_system_info", return_value={"cpu": {}}), \
             patch("main.save_report", side_effect=OSError("Permission denied")), \
             patch("sys.stdout", new_callable=StringIO), \
             patch("sys.stderr", new_callable=StringIO) as mock_stderr:

            result = main()

        self.assertEqual(result, 1)
        self.assertIn("Permission denied", mock_stderr.getvalue())

    # Test report collection failure
    def test_report_collection_failed_exit_code(self):
        with patch("sys.argv", ["main.py", "report"]), \
             patch("main.collect_system_info", side_effect=ValueError("Invalid system data")), \
             patch("main.save_report") as mock_save, \
             patch("sys.stdout", new_callable=StringIO), \
             patch("sys.stderr", new_callable=StringIO):

            result = main()

        self.assertEqual(result, 1)
        mock_save.assert_not_called()

    # Test invalid JSON serialization error
    def test_report_type_error_exit_code(self):
        with patch("sys.argv", ["main.py", "report"]), \
             patch("main.collect_system_info", return_value={"cpu": {}}), \
             patch("main.save_report", side_effect=TypeError("Not JSON serializable")), \
             patch("sys.stdout", new_callable=StringIO), \
             patch("sys.stderr", new_callable=StringIO):

            result = main()

        self.assertEqual(result, 1)

if __name__ == "__main__":
    unittest.main()