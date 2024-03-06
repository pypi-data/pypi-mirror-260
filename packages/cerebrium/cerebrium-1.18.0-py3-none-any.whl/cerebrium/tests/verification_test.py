import unittest

from cerebrium import datatypes
from cerebrium.verification import *


class TestVerification(unittest.TestCase):
    def test_validate_name(self):
        assert validate_name("") == "No name provided.\n"
        assert validate_name("abc123-") == ""

    def test_validate_python_version(self):
        assert validate_python_version("") == ""
        assert validate_python_version("3.9") == ""
        assert (
            validate_python_version("1.0")
            == "Python version must be one of ['3.8', '3.9', '3.10', '3.11']\n"
        )

    def test_validate_gpu_selection(self):
        assert validate_gpu_selection("") == ""
        assert (
            validate_gpu_selection("CPU")
            == "Hardware must be one of:['GPU', 'TURING_4000', 'TURING_5000', 'AMPERE_A4000', 'AMPERE_A5000', 'AMPERE_A6000', 'AMPERE_A100', 'AMPERE_A100_40GB']\n"
        )
        assert (
            validate_gpu_selection("INVALID")
            == "Hardware must be one of:['GPU', 'TURING_4000', 'TURING_5000', 'AMPERE_A4000', 'AMPERE_A5000', 'AMPERE_A6000', 'AMPERE_A100', 'AMPERE_A100_40GB']\n"
        )

    def test_validate_cooldown(self):
        assert validate_cooldown(None) == ""
        assert (
            validate_cooldown(-1)
            == "Cooldown must be a non-negative number of seconds.\n"
        )
        assert validate_cooldown(0) == ""

    def test_validate_min_replicas(self):
        assert validate_min_replicas(None) == ""
        assert (
            validate_min_replicas(-1)
            == "Minimum number of replicas must be a non-negative integer.\n"
        )
        assert validate_min_replicas(0) == ""

    def test_validate_max_replicas(self):
        assert validate_max_replicas(None, 0) == ""
        assert (
            validate_max_replicas(0, 1)
            == "Maximum number of replicas must be a non-negative integer greater than 0.\nMaximum number of replicas must be greater than or equal to minimum number of replicas.\n"
        )
        assert (
            validate_max_replicas(1, 2)
            == "Maximum number of replicas must be greater than or equal to minimum number of replicas.\n"
        )
        assert validate_max_replicas(2, 1) == ""


if __name__ == "__main__":
    unittest.main()
