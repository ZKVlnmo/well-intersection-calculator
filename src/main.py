from src.TrajectoryProcessor import TrajectoryProcessor

data = {
    "grid": {
        "x_coords": [-2, -1, 0, 1],
        "y_coords": [-1, 0, 1, 2],
        "height_matrix": [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],

    },
    "trajectories": [
        [[0, 0, 6], [0, 0, 4], [-2, 0, -4], [-2, 0, 4]],
        # [[0, 0, 6], [0, 0, 4], [0, 0, -4]],
        # [[100, 0, 6], [100, 0, 4], [100, 0, -4]],

    ]
}

arr = TrajectoryProcessor(data)
