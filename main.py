from distributions import normal_distribution

parameters_table = [
    [(5, 2), (3, 1), (10, 2)],
    [(15, 3), (10, 5), (20, 5)],
    [(45, 3), (35, 7), (60, 9)]
]


def arrival_ships_parameters(time, size):
    if size == 1:
        if 0 <= time <= 180:
            return parameters_table[0][0]
        if 180 <= time <= 540:
            return parameters_table[0][1]
        if 540 <= time <= 720:
            return parameters_table[0][2]
    if size == 2:
        if 0 <= time <= 180:
            return parameters_table[1][0]
        if 180 <= time <= 540:
            return parameters_table[1][1]
        if 540 <= time <= 720:
            return parameters_table[1][2]
    if size == 4:
        if 0 <= time <= 180:
            return parameters_table[2][0]
        if 180 <= time <= 540:
            return parameters_table[2][1]
        if 540 <= time <= 720:
            return parameters_table[2][2]
    assert False, f'Invalid parameters in arrival_ships_parameters - time: {time}, size: {size}'


def arrival_ships_distribution(time, size):
    mu, sigma2 = arrival_ships_parameters(time, size)
    return abs(normal_distribution(mu, sigma2 ** 0.5))
