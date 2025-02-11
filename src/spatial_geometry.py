import numpy as np
from typing import List, Tuple, Optional





def best_fit_plane(points: List[Tuple[float, float, Optional[float]]]) -> Optional[Tuple[float, float, float, float]]:
    """
    Вычисляет коэффициенты уравнения плоскости Ax + By + Cz + D = 0, наилучшим образом аппроксимирующей заданные точки.

    :param points: Список из четырех точек, каждая представлена кортежем (x, y, z), где z может быть None.
    :return: Кортеж коэффициентов (A, B, C, D) или None, если более одной точки имеет z = None.
    """
    x, y, z = np.array(points).T

    if list(z).count(None) > 0:
        return None

    M = np.c_[x, y, np.ones(len(points))]
    ABCD, _, _, _ = np.linalg.lstsq(M, -z, rcond=None)
    A, B, D = ABCD
    C = 1

    return A, B, C, D




def line_plane_intersection(
        plane: Tuple[float, float, float, float],
        line_point: Tuple[float, float, float],
        line_dir: Tuple[float, float, float]
    ) -> Optional[Tuple[float, float, float]]:
    """
    Вычисляет точку пересечения прямой и плоскости.

    :param plane: Коэффициенты плоскости (A, B, C, D).
    :param line_point: Точка на прямой (x, y, z).
    :param line_dir: Направляющий вектор прямой (dx, dy, dz).
    :return:
        - Точка пересечения (x, y, z), если пересечение существует.
        - line_point, если прямая лежит в плоскости.
        - None, если прямая параллельна плоскости и не лежит в ней.
    """
    A, B, C, D = plane
    x0, y0, z0 = line_point
    dx, dy, dz = line_dir

    denom = A * dx + B * dy + C * dz  # Вычисляем знаменатель для параметра t

    if abs(denom) < 1e-10:
        # Проверяем, лежит ли прямая в плоскости
        if abs(A * x0 + B * y0 + C * z0 + D) < 1e-10:
            return line_point  # Прямая лежит в плоскости
        return None  # Прямая параллельна плоскости, но не лежит в ней

    # Вычисляем параметр t для нахождения точки пересечения
    t = -(A * x0 + B * y0 + C * z0 + D) / denom
    return x0 + t * dx, y0 + t * dy, z0 + t * dz


def line_from_two_points(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> Tuple[
    Tuple[float, float, float], Tuple[float, float, float]]:
    """
    Создает уравнение прямой по двум точкам.

    :param p1: Первая точка (x, y, z).
    :param p2: Вторая точка (x, y, z).
    :return: Кортеж из начальной точки прямой и направляющего вектора.
    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    direction = (x2 - x1, y2 - y1, z2 - z1)
    return p1, direction
