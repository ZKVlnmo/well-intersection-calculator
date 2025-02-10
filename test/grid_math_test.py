import unittest
import math

from src.grid_math import bilinear_interpolation_4terms, binary_search_nearest, is_point_in_rectangle, \
    bresenham_grid_with_corners


class TestBilinearInterpolation(unittest.TestCase):
    """
    Тесты для функции билинейной интерполяции.
    """

    def test_interpolation_in_middle(self):
        """
        Тест для интерполяции в центре квадрата.

        Проверяет корректность вычисления значения в центре квадрата.
        """
        z = [1, 2, 3, 4]
        result = bilinear_interpolation_4terms(1, 1, 0, 2, 0, 2, z)
        self.assertAlmostEqual(result, 2.5, places=2)

    def test_interpolation_on_edge(self):
        """
        Тест для интерполяции на краю квадрата.

        Проверяет корректность вычисления значения на границе квадрата.
        """
        z = [1, 2, 3, 4]
        result = bilinear_interpolation_4terms(0, 0, 0, 2, 0, 2, z)
        self.assertEqual(result, 1)

    def test_invalid_square(self):
        """
        Тест для случая, когда квадрат некорректен.

        Проверяет корректность работы функции при некорректном квадрате (например, все точки совпадают).
        """
        z = [1, 2, 3, 4]
        result = bilinear_interpolation_4terms(1, 1, 0, 2, 0, 2, z)
        self.assertIsNotNone(result)  # Для корректного квадрата
        result_invalid = bilinear_interpolation_4terms(1, 1, 1, 1, 1, 1, z)
        self.assertIsNone(result_invalid)  # Для некорректного квадрата


class TestBinarySearch(unittest.TestCase):
    """
    Тесты для функции бинарного поиска ближайшего значения в отсортированном массиве.
    """

    def test_find_exact_value(self):
        """
        Тест для поиска точного значения.

        Проверяет, что поиск точного значения в массиве работает правильно.
        """
        arr = [1, 2, 3, 4, 5]
        result = binary_search_nearest(arr, 3)
        self.assertEqual(result["value"], [3, 4])
        self.assertEqual(result["index"], [2, 3])

    def test_find_value_between_elements(self):
        """
        Тест для поиска значения между элементами массива.

        Проверяет, что функция находит два ближайших значения, если искомое значение между ними.
        """
        arr = [1, 2, 3, 4, 5]
        result = binary_search_nearest(arr, 2.5)
        self.assertEqual(result["value"], [3, 2])
        self.assertEqual(result["index"], [2, 1])

    def test_empty_array(self):
        """
        Тест для пустого массива.

        Проверяет корректность работы функции при пустом массиве.
        """
        arr = []
        result = binary_search_nearest(arr, 3)
        self.assertEqual(result["value"], [None, None])
        self.assertEqual(result["index"], [None, None])


class TestIsPointInRectangle(unittest.TestCase):
    """
    Тесты для функции проверки нахождения точки внутри прямоугольника.
    """

    def test_point_inside(self):
        """
        Тест для точки внутри прямоугольника.

        Проверяет, что функция правильно определяет, находится ли точка внутри прямоугольника.
        """
        intersection = (1, 1, 0)
        points = [(0, 0), (0, 2), (2, 0), (2, 2)]
        result = is_point_in_rectangle(intersection, points)
        self.assertTrue(result)

    def test_point_outside(self):
        """
        Тест для точки за пределами прямоугольника.

        Проверяет, что функция правильно определяет, находится ли точка за пределами прямоугольника.
        """
        intersection = (3, 3, 0)
        points = [(0, 0), (0, 2), (2, 0), (2, 2)]
        result = is_point_in_rectangle(intersection, points)
        self.assertFalse(result)

    def test_point_on_border(self):
        """
        Тест для точки на границе прямоугольника.

        Проверяет, что функция правильно определяет, если точка лежит на границе прямоугольника.
        """
        intersection = (0, 1, 0)
        points = [(0, 0), (0, 2), (2, 0), (2, 2)]
        result = is_point_in_rectangle(intersection, points)
        self.assertTrue(result)


class TestBresenhamGridWithCorners(unittest.TestCase):
    """
    Тесты для функции, которая находит пересечение отрезка с сеткой и возвращает ячейки.
    """

    def test_basic_line(self):
        """
        Тест для базовой линии.

        Проверяет корректность работы функции для простого случая, когда линия пересекает две ячейки.
        """
        grid_x = [0, 1, 2, 3]
        grid_y = [0, 1, 2, 3]
        result = bresenham_grid_with_corners(0, 0, 2, 2, grid_x, grid_y)
        self.assertEqual(result, [{'index': (0, 0, 1, 1), 'value': (0, 0, 1, 1)}, {'index': (1, 1, 2, 2), 'value': (1, 1, 2, 2)}])

    def test_no_intersection(self):
        """
        Тест для случая без пересечения.

        Проверяет корректность работы функции, когда линия не пересекает сетку.
        """
        grid_x = [0, 1, 2, 3]
        grid_y = [0, 1, 2, 3]
        result = bresenham_grid_with_corners(0, 0, 5, 5, grid_x, grid_y)
        self.assertEqual(len(result), 0)

    def test_vertical_line(self):
        """
        Тест для вертикальной линии.

        Проверяет корректность работы функции для вертикальной линии, пересекающей несколько ячеек.
        """
        grid_x = [0, 1, 2, 3]
        grid_y = [0, 1, 2, 3]
        result = bresenham_grid_with_corners(1, 0, 1, 3, grid_x, grid_y)
        self.assertEqual(len(result), 3)


if __name__ == "__main__":
    unittest.main()
