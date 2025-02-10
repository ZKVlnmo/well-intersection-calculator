import unittest
import math
from src.spatial_geometry import best_fit_plane_three_points, best_fit_plane, line_plane_intersection, \
    line_from_two_points


class TestBestFitPlaneThreePoints(unittest.TestCase):
    """
    Тесты для функции, вычисляющей коэффициенты плоскости, проходящей через три точки.
    """

    def test_plane_from_three_points(self):
        """
        Тест для вычисления плоскости через три точки, образующие прямой угол.

        Проверяет, что для точек, образующих прямой угол, плоскость будет иметь правильные коэффициенты.
        """
        points = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
        result = best_fit_plane_three_points(points)
        self.assertEqual(result, (0, 0, 1, 0))

    def test_non_collinear_points(self):
        """
        Тест для вычисления плоскости через три неколлинеарные точки.

        Проверяет, что для неколлинеарных точек правильно вычисляются коэффициенты плоскости.
        """
        points = [(0, 0, 0), (1, 1, 1), (2, 0, 1)]
        result = best_fit_plane_three_points(points)
        self.assertAlmostEqual(result[0], 1, places=2)

    def test_parallel_points(self):
        """
        Тест для вычисления плоскости через три точки, лежащие на одной прямой.

        Проверяет, что для точек, лежащих на одной прямой, функция возвращает ошибочный результат (плоскость не существует).
        """
        points = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
        result = best_fit_plane_three_points(points)
        self.assertEqual(result, (0, 0, 0, 0))


class TestBestFitPlane(unittest.TestCase):
    """
    Тесты для функции, вычисляющей коэффициенты плоскости, наилучшим образом аппроксимирующей заданные точки.
    """

    def test_four_points_with_valid_z(self):
        """
        Тест для четырех точек с корректными значениями z.

        Проверяет, что функция работает корректно при наличии четырех точек с определенными координатами z.
        """
        points = [(0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 3, 3)]
        result = best_fit_plane(points)
        self.assertIsNotNone(result)

    def test_four_points_with_one_none_z(self):
        """
        Тест для четырех точек, одна из которых имеет значение z = None.

        Проверяет, что функция корректно обрабатывает случаи с отсутствующим значением z в одной точке.
        """
        points = [(0, 0, 0), (1, 1, None), (2, 2, 2), (3, 3, 3)]
        result = best_fit_plane(points)
        self.assertIsNotNone(result)

    def test_four_points_with_multiple_none_z(self):
        """
        Тест для четырех точек, две из которых имеют значение z = None.

        Проверяет, что функция возвращает None, если несколько точек имеют значение z = None.
        """
        points = [(0, 0, None), (1, 1, None), (2, 2, 2), (3, 3, 3)]
        result = best_fit_plane(points)
        self.assertIsNone(result)


class TestLinePlaneIntersection(unittest.TestCase):
    """
    Тесты для функции нахождения точки пересечения прямой и плоскости.
    """

    def test_intersection(self):
        """
        Тест для нахождения точки пересечения прямой и плоскости.

        Проверяет, что прямая пересекает плоскость и вычисляется правильная точка пересечения.
        """
        plane = (1, -1, 1, 0)
        line_point = (0, 0, 0)
        line_dir = (1, 1, 1)
        result = line_plane_intersection(plane, line_point, line_dir)
        self.assertEqual(result, (0, 0, 0))

    def test_parallel_line(self):
        """
        Тест для случая, когда прямая параллельна плоскости.

        Проверяет, что функция правильно возвращает None, если прямая параллельна плоскости и не пересекает ее.
        """
        plane = (0, 0, 1, 1)
        line_point = (0, 0, 0)
        line_dir = (1, 1, 0)
        result = line_plane_intersection(plane, line_point, line_dir)
        self.assertIsNone(result)


class TestLineFromTwoPoints(unittest.TestCase):
    """
    Тесты для функции создания прямой по двум точкам.
    """

    def test_standard_line(self):
        """
        Тест для стандартной прямой.

        Проверяет, что функция правильно вычисляет направление прямой по двум точкам.
        """
        p1 = (0, 0, 0)
        p2 = (1, 1, 1)
        result = line_from_two_points(p1, p2)
        self.assertEqual(result, ((0, 0, 0), (1, 1, 1)))

    def test_vertical_line(self):
        """
        Тест для вертикальной прямой.

        Проверяет, что функция правильно вычисляет направление вертикальной прямой.
        """
        p1 = (0, 0, 0)
        p2 = (0, 1, 0)
        result = line_from_two_points(p1, p2)
        self.assertEqual(result, ((0, 0, 0), (0, 1, 0)))

    def test_line_with_negative_coordinates(self):
        """
        Тест для прямой с отрицательными координатами.

        Проверяет, что функция правильно вычисляет направление прямой, если одна из точек имеет отрицательные координаты.
        """
        p1 = (-1, -1, -1)
        p2 = (1, 1, 1)
        result = line_from_two_points(p1, p2)
        self.assertEqual(result, ((-1, -1, -1), (2, 2, 2)))
