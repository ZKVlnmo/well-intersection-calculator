import unittest
from src.trajectoryProcessor import TrajectoryProcessor
from test.parser import parse
import numpy as np


class TestTrajectoryProcessor(unittest.TestCase):


    def test_calculate_intersections(self):
        """
        Проверяет корректность вычисления пересечений траектории с поверхностью.
        """
        data = parse("test_data/Copy of P50_J14_Toppr.irap")
        data["trajectories"] = [[]]  # Создаём пустой список траекторий

        for i in range(-5000, 1000, 100):
            data["trajectories"][0].append([(61352 + 79330) / 2, (299628 + 322815) / 2, i])

        processor = TrajectoryProcessor()
        answer = processor.calculate_intersections(data)
        print(answer)
        self.assertEqual(answer, [[(np.float64(70341.0), np.float64(311221.5), np.float64(-2520.26934412866))]])


if __name__ == "__main__":
    unittest.main()
