import math
import numpy as np


def bilinear_interpolation_4terms(x, y, x1, x4, y1, y4, z):
    """
    Выполняет билинейную интерполяцию для заданной точки (x, y) внутри прямоугольной области,
    используя значения функции в 4 угловых точках, хранящиеся в массиве z.

    Параметры:
    - x, y: координаты точки, для которой нужно вычислить значение функции
    - x1, y1: координаты первой точки (нижний левый угол)
    - x4, y4: координаты второй точки (верхний правый угол)
    - z: массив значений функции в 4 угловых точках [f11, f12, f21, f22]

    Возвращает:
    - Интерполированное значение функции в точке (x, y)
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


def bilinear_interpolation_4terms_with_angle(angle_rad, x, y, x1, y1, x2, y2, x3, y3, x4, y4, z):
    x0 = (x1 + x2 + x3 + x4) / 4
    y0 = (y1 + y2 + y3 + y4) / 4

    cos = math.cos(angle_rad)
    sin = math.sin(angle_rad)
    x1_new = (x1 - x0) * cos + (y1 - y0) * sin
    y1_new = -(x1 - x0) * sin + (y1 - y0) * cos
    x4_new = (x4 - x0) * cos + (y4 - y0) * sin
    y4_new = -(x4 - x0) * sin + (y4 - y0) * cos
    x_new = (x - x0) * cos + (y - y0) * sin
    y_new = -(x - x0) * sin + (y - y0) * cos

    return bilinear_interpolation_4terms(x_new, y_new, x1_new, y1_new, x4_new, y4_new, z)
# print(bilinear_interpolation_4terms_with_angle(math.radians(15),1025.000000, 1250.000000,994.828774 , 1219.067070,1043.125065 , 1232.008022, 981.887821 , 1267.363361,1030.184113 , 1280.304313,[23.00,28.00, 24.00,29.00]))


def binary_search_nearest(arr, target):
    """
    Находит ближайший по значению элемент в отсортированном массиве.
    :param arr: отсортированный массив
    :param target: число, для которого ищем ближайший элемент
    :return: ближайший элемент
    """
    if not arr:
        return None  # Если массив пуст, возвращаем None

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        # Если нашли точное совпадение — возвращаем его
        if arr[mid] == target:
            if mid<len(arr)-1:
                return {"value":[arr[mid], arr[mid+1]],"index":[mid,mid+1]}
            else:
                return {"value": [arr[mid-1], arr[mid ]], "index": [mid-1, mid ]}

        # Если target меньше, идем влево
        if arr[mid] > target:
            right = mid - 1
        else:  # Если target больше, идем вправо
            left = mid + 1

    # Теперь right указывает на самый большой элемент <= target
    # left указывает на самый маленький элемент > target
    # Нужно выбрать ближайший из arr[right] и arr[left]

    if right < 0:  # Все элементы в массиве больше target
        return {"value":[None, None],"index":[None,None]}
    if left >= len(arr):  # Все элементы в массиве меньше target
        return {"value":[None, None],"index":[None,None]}

    # Выбираем ближайший элемент по модулю разницы
    return {"value":[arr[left], arr[right]],"index":[left,right]}


def bresenham_grid_with_corners(x1, y1, x2, y2, grid_x, grid_y):
    """
    Определяет, через какие ячейки проходит отрезок и возвращает координаты их углов.

    Параметры:
    - x1, y1, x2, y2: координаты начала и конца отрезка
    - grid_x, grid_y: массивы координат узлов сетки по X и Y

    Возвращает:
    - Список клеток, каждая представлена 4 угловыми координатами [(x_min, y_min, x_max, y_max), ...]
    """

    def find_index(grid, value):
        for i in range(len(grid) - 1):
            if grid[i] <= value < grid[i + 1]:
                return i
        return None


    i1, j1 = find_index(grid_x, x1), find_index(grid_y, y1)
    i2, j2 = find_index(grid_x, x2), find_index(grid_y, y2)

    if i1 is None or j1 is None or i2 is None or j2 is None:
        return []

    cells = []
    dx = abs(i2 - i1)
    dy = abs(j2 - j1)
    sx = 1 if i1 < i2 else -1
    sy = 1 if j1 < j2 else -1
    err = dx - dy

    while True:

        x_min, x_max = grid_x[i1], grid_x[i1 + 1]
        y_min, y_max = grid_y[j1], grid_y[j1 + 1]

        cells.append((x_min, y_min, x_max, y_max))

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

def is_point_in_rectangle(intersection, points):
    # Преобразуем список точек в numpy массив для удобства
    points = np.array(points)

    # Получаем минимальные и максимальные значения для x и y
    min_x = points[:, 0].min()
    max_x = points[:, 0].max()
    min_y = points[:, 1].min()
    max_y = points[:, 1].max()

    # Проверяем, лежит ли точка пересечения внутри прямоугольника
    x, y, _ = intersection  # предполагаем, что intersection — это кортеж или список вида [x, y, z]
    if min_x <= x <= max_x and min_y <= y <= max_y:
        return True
    return False