import unittest
from cerebrium.datatypes import Hardware as HardwareOption
from cerebrium.constants import MAX_GPU_COUNT, MIN_CPU, MIN_MEMORY


class TestHardwareOption(unittest.TestCase):
    def setUp(self):
        self.hardware_option = HardwareOption(
            name="Test",
            VRAM=8,
            gpu_model="Test Model",
            max_memory=128.0,
            max_cpu=36,
            max_gpu_count=MAX_GPU_COUNT,
        )

    def test_validate_cpu_exceeds_max(self):
        message = self.hardware_option.validate(cpu=40, memory=128.0, gpu_count=1)
        self.assertIn("CPU must be at most", message)

    def test_validate_cpu_below_min(self):
        message = self.hardware_option.validate(cpu=0, memory=128.0, gpu_count=1)
        self.assertIn("CPU must be at least", message)

    def test_validate_memory_exceeds_max(self):
        message = self.hardware_option.validate(cpu=36, memory=130.0, gpu_count=1)
        self.assertIn("Memory must be at most", message)

    def test_validate_memory_below_min(self):
        message = self.hardware_option.validate(cpu=36, memory=1.0, gpu_count=1)
        self.assertIn("Memory must be at least", message)

    def test_validate_gpu_count_exceeds_max(self):
        message = self.hardware_option.validate(cpu=36, memory=128.0, gpu_count=10)
        self.assertIn("Number of GPUs must be at most", message)

    def test_validate_gpu_count_below_min(self):
        message = self.hardware_option.validate(cpu=36, memory=128.0, gpu_count=0)
        self.assertIn("Number of GPUs must be at least", message)


if __name__ == "__main__":
    unittest.main()
