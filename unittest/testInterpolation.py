import unittest
import math

from src.bilinear_interpolation import bilinear_interpolation_4terms, bilinear_interpolation_4terms_with_angle


# Здесь мы предполагаем, что функции bilinear_interpolation_4terms и bilinear_interpolation_4terms_with_angle уже определены

class TestBilinearInterpolation(unittest.TestCase):

    def test_bilinear_interpolation_4terms_normal(self):
        # Тест с обычными значениями
        x1, y1 = 0, 0
        x4, y4 = 2, 2
        z = [1, 2, 3, 4]  # f11, f12, f21, f22
        x, y = 1, 1

        result = bilinear_interpolation_4terms(x, y, x1, y1, x4, y4, z)
        expected = 2.5  # Ожидаемое значение для точки (1, 1)
        self.assertAlmostEqual(result, expected, places=5)

    def test_bilinear_interpolation_4terms_edge_case(self):
        # Тест с точками, расположенными на одной линии (может вызвать деление на ноль)
        x1, y1 = 0, 0
        x4, y4 = 2, 0  # Точки на одной горизонтальной линии
        z = [1, 2, 3, 4]  # f11, f12, f21, f22
        x, y = 1, 0  # Точка на этой линии

        result = bilinear_interpolation_4terms(x, y, x1, y1, x4, y4, z)
        self.assertIsNone(result, "Expected None due to division by zero in denominator")

    def test_bilinear_interpolation_with_angle(self):
        # Тест с поворотом точек
        angle_deg = 90  # Поворот на 90 градусов
        angle_rad = math.radians(angle_deg)
        x1, y1 = 0, 0
        x2, y2 = 0, 1
        x3, y3 = 1, 0
        x4, y4 = 1, 1
        z = [1, 1, 1, 2]  # f11, f12, f21, f22
        x, y = 1, 0.5  # Точка внутри квадрата

        result = bilinear_interpolation_4terms_with_angle(angle_rad, x, y, x1, y1, x2, y2, x3, y3, x4, y4, z)
        expected = 1.5  # После поворота значения должны оставаться такими же
        self.assertAlmostEqual(result, expected, places=5)


    def test_bilinear_interpolation_with_angle_no_rotation(self):
        # Тест без поворота, чтобы убедиться, что поворот работает корректно
        angle_deg = 0  # Без поворота
        angle_rad = math.radians(angle_deg)
        x1, y1 = 0, 0
        x2, y2 = 2, 0
        x3, y3 = 0, 2
        x4, y4 = 2, 2
        z = [1, 2, 3, 4]  # f11, f12, f21, f22
        x, y = 1, 1
        x, y = 1, 1  # Точка внутри квадрата

        result = bilinear_interpolation_4terms_with_angle(angle_rad, x, y, x1, y1, x2, y2, x3, y3, x4, y4, z)
        expected = 2.5  # Без поворота результат должен быть такой же
        self.assertAlmostEqual(result, expected, places=5)


if __name__ == "__main__":
    unittest.main()