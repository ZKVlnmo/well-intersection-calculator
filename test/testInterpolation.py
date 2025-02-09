import test
import math

from src.bilinear_interpolation import bilinear_interpolation_4terms, bilinear_interpolation_4terms_with_angle


# Здесь мы предполагаем, что функции bilinear_interpolation_4terms и bilinear_interpolation_4terms_with_angle уже определены

class TestBilinearInterpolation(test.TestCase):

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
        angle_deg = 15  # Поворот на 90 градусов
        angle_rad = math.radians(angle_deg)
        x1, y1 = 994.828774, 1219.067070
        x2, y2 = 1043.125065, 1232.008022
        x3, y3 = 981.887821, 1267.363361,
        x4, y4 = 1030.184113,1280.304313
        z = [23.00, 28.00, 24.00, 29.00]  # f11, f12, f21, f22
        x, y = 1025.000000, 1250.000000  # Точка внутри квадрата

        result = bilinear_interpolation_4terms_with_angle(angle_rad, x, y, x1, y1, x2, y2, x3, y3, x4, y4, z)
        expected = 25.94998714  # После поворота значения должны оставаться такими же
        self.assertAlmostEqual(result, expected, places=5)



    def test_bilinear_interpolation_with_angle_no_rotation(self):
        angle_deg = 0  # Без поворота
        angle_rad = math.radians(angle_deg)
        x1, y1 = 15,20
        x2, y2 = 16,20
        x3, y3 = 15,21
        x4, y4 = 16,21
        z = [4.34,4.25,5.17,5.18] # f11, f12, f21, f22
        x, y = 1, 1
        x, y = 15.5,20.5

        result = bilinear_interpolation_4terms_with_angle(angle_rad, x, y, x1, y1, x2, y2, x3, y3, x4, y4, z)
        expected = 4.73
        self.assertAlmostEqual(round(result, 2), expected, places=5)


if __name__ == "__main__":
    test.main()