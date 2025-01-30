from src.WellIntersectionCalculator import WellIntersectionCalculator
# with open("C:/Users/user/PycharmProjects/well-intersection-calculator/Copy of P50_J14_Toppr.irap", "r", encoding="utf-8") as f:
#     content = f.readline()
#     content2 = f.readline()
#     content3 = f.readline()
#     content4 = f.readline()
#     arr = f.read().split()
# print(content,content2,content3,content4)
# print( "должно быть по х максимум" )

data = {
    "grid": {
        "x_coords": [0.1, 0.2, 0.3],
        "y_coords": [1.0, 2.0],
        "height_matrix": [[10, 20, 30], [40, 50, 60]],

    },
    "trajectories": [
        [[0.1, 1.0, 10.0], [0.2, 1.5, 12.0]],
        [[0.3, 2.0, 15.0]]
    ]
}

arr = WellIntersectionCalculator(data)