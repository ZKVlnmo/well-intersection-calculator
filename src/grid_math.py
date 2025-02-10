import math
import numpy as np
from typing import List, Tuple, Optional, Dict

def bilinear_interpolation_4terms(x: float, y: float, x1: float, x4: float, y1: float, y4: float, z: List[float]) -> Optional[float]:
    """
    Выполняет билинейную интерполяцию для заданной точки (x, y) внутри прямоугольной области,
    используя значения функции в 4 угловых точках, хранящиеся в массиве z.

    :param x: координата x точки
    :param y: координата y точки
    :param x1: координата x первой точки (нижний левый угол)
    :param x4: координата x второй точки (верхний правый угол)
    :param y1: координата y первой точки (нижний левый угол)
    :param y4: координата y второй точки (верхний правый угол)
    :param z: массив значений функции в 4 угловых точках [f11, f12, f21, f22]
    :return: Интерполированное значение функции в точке (x, y) или None если точки не задают квадрат
    """
    f11, f12, f21, f22 = z

    if x4 - x1 != 0 and y4 - y1 != 0:
        term1 = f11 * (x4 - x) * (y4 - y) / ((x4 - x1) * (y4 - y1))
        term2 = f12 * (x4 - x) * (y - y1) / ((x4 - x1) * (y4 - y1))
        term3 = f21 * (x - x1) * (y4 - y) / ((x4 - x1) * (y4 - y1))
        term4 = f22 * (x - x1) * (y - y1) / ((x4 - x1) * (y4 - y1))
        return term1 + term2 + term3 + term4
    else:
        return None



def binary_search_nearest(arr: List[float], target: float) -> Dict[str, List[Optional[float]]]:
    """
    Находит ближайший по значению элемент в отсортированном массиве.

    :param arr: отсортированный массив
    :param target: искомое значение
    :return: Словарь с ближайшими значениями  и их индексами вершин квадрата в которой лежит заданая точка
    """
    if not arr:
        return {"value": [None, None], "index": [None, None]}

    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            if mid < len(arr) - 1:
                return {"value": [arr[mid], arr[mid + 1]], "index": [mid, mid + 1]}
            else:
                return {"value": [arr[mid - 1], arr[mid]], "index": [mid - 1, mid]}
        if arr[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    return {"value": [arr[left], arr[right]], "index": [left, right]}

def is_point_in_rectangle(intersection: Tuple[float, float, float], points: List[Tuple[float, float]]) -> bool:
    """
    Проверяет, находится ли точка внутри заданного прямоугольника.

    :param intersection: координаты точки пересечения (x, y, z)
    :param points: список вершин прямоугольника
    :return: True, если точка внутри, иначе False
    """
    points = np.array(points)
    min_x = points[:, 0].min()
    max_x = points[:, 0].max()
    min_y = points[:, 1].min()
    max_y = points[:, 1].max()
    x, y, _ = intersection
    return min_x <= x <= max_x and min_y <= y <= max_y


def bresenham_grid_with_corners(
    x1: float, y1: float, x2: float, y2: float,
    grid_x: List[float], grid_y: List[float]
) -> List[Dict[str, Tuple[int, int, int, int]]]:
    """
    Определяет, через какие ячейки проходит отрезок, и возвращает координаты их углов.

    :param x1: Координата X начала отрезка
    :param y1: Координата Y начала отрезка
    :param x2: Координата X конца отрезка
    :param y2: Координата Y конца отрезка
    :param grid_x: Список координат узлов сетки по оси X
    :param grid_y: Список координат узлов сетки по оси Y
    :return: Список клеток, каждая представлена индексами угловых координат и их значениями
    """
    def find_index(grid: List[float], value: float) -> Optional[int]:
        """Ищет индекс ячейки, в которую попадает заданное значение."""
        for i in range(len(grid) - 1):
            if grid[i] <= value <= grid[i + 1]:
                return i
        return None

    i1, j1 = find_index(grid_x, x1), find_index(grid_y, y1)
    i2, j2 = find_index(grid_x, x2), find_index(grid_y, y2)

    if i1 is None or j1 is None or i2 is None or j2 is None:
        return []

    cells: List[Dict[str, Tuple[int, int, int, int]]] = []
    dx, dy = abs(i2 - i1), abs(j2 - j1)
    sx, sy = (1 if i1 < i2 else -1), (1 if j1 < j2 else -1)
    err = dx - dy

    while True:
        x_min, x_max = grid_x[i1], grid_x[i1 + 1]
        y_min, y_max = grid_y[j1], grid_y[j1 + 1]

        cells.append({
            "index": (i1, j1, i1 + 1, j1 + 1),
            "value": (x_min, y_min, x_max, y_max)
        })

        if i1 == i2 and j1 == j2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            i1 += sx
        if e2 < dx:
            err += dx
            j1 += sy

    return cells
