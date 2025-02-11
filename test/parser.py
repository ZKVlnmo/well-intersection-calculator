import numpy as np

def parse(filename: str):
    with open(filename) as irap_data:
        first_row = irap_data.readline().split()
        second_row = irap_data.readline().split()
        third_row = irap_data.readline().split()

        parsed_data = {
            "id": first_row[0],
            "y_cnt": int(first_row[1]),
            "x_inc": float(first_row[2]),
            "y_inc": float(first_row[3]),
            "x_min": float(second_row[0]),
            "x_max": float(second_row[1]),
            "y_min": float(second_row[2]),
            "y_max": float(second_row[3]),
            "x_cnt": int(third_row[0]),
            "rot": float(third_row[1]),
            "x_rot": float(third_row[2]),
            "y_rot": float(third_row[3]),
        }

        irap_data.readline()
        depths = np.array([float(value) for line in irap_data for value in line.split()], dtype=object)

    x_cnt = parsed_data["x_cnt"]
    y_cnt = parsed_data["y_cnt"]
    depths[depths == 9999900] = None
    height_matrix = depths.reshape((y_cnt, x_cnt))

    x_coords = np.linspace(parsed_data["x_min"], parsed_data["x_max"], x_cnt)
    y_coords = np.linspace(parsed_data["y_min"], parsed_data["y_max"], y_cnt)

    depth_map = {(x, y): height_matrix[i, j] for i, y in enumerate(y_coords) for j, x in enumerate(x_coords)}

    data = {
        "grid":
            {
                "y_coords": y_coords.tolist(),
                "x_coords": x_coords.tolist(),
                "height_matrix": height_matrix.tolist(),
            },
        "trajectories": [[[1, 1, 1], [1, 2, 2], [1, 3, 3]], [[1, 1, 1], [1, 2, 2], [1, 3, 3]]]
    }
    return data