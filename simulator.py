from functools import namedtuple
from distributions import exponential_distribution, normal_distribution

INF = 2 ** 64

Ship = namedtuple('Ship', ['time', 'size'])
Ships = namedtuple('Ships', ['time', 'ships'])

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


def arrival_ships(dike_rows=2, size_rows=6):
    time = 0
    ships_list = list()
    d = arrival_ships_distribution
    ships = [Ship(d(0, 1), 1), Ship(d(0, 2), 2), Ship(d(0, 4), 4)]
    while True:
        ship = Ship(*min(ships))
        if ship.time > 720:
            break
        ships_list.append(ship)
        ships.remove(ship)
        ships.append(Ship(ship.time + d(*ship), ship.size))
    ships = ships_list
    while ships:
        next_ships = list()
        skips_ships = list()
        dike = [0 for _ in range(dike_rows)]
        for ship in ships:
            skip = True
            for index, row in enumerate(dike):
                if ship.size + row <= size_rows:
                    dike[index] += ship.size
                    next_ships.append(ship)
                    skip = False
                    break
            if skip:
                skips_ships.append(ship)
        time = max(time, Ship(*max(next_ships)).time)
        yield Ships(time, next_ships)
        ships = skips_ships


def dike_cycle(ships):
    d = exponential_distribution
    return d(4) + sum(d(2) for _ in ships) + d(7) + d(1.5 * len(ships))


def simulation(number_of_dikes=5):
    generator_ships = arrival_ships()
    finished = False
    time = 0
    number_of_arrivals = 0
    number_of_departures = 0
    dikes = [[] for _ in range(number_of_dikes)]
    arrivals = [[] for _ in range(number_of_dikes)]
    departures = []
    times = [INF for _ in range(number_of_dikes)]
    try:
        arrival = Ships(*next(generator_ships))
    except StopIteration:
        finished = True
    while True:
        min_time = min(times)
        if not finished and arrival.time <= min_time:
            time = arrival.time
            number_of_arrivals += 1
            dikes[0].append(arrival.ships)
            arrivals[0].append(Ships(time, arrival.ships))
            try:
                arrival = Ships(*next(generator_ships))
            except StopIteration:
                finished = True
            if len(dikes[0]) == 1:
                departure_ships = dikes[0][0]
                times[0] = time + dike_cycle(departure_ships)
        else:
            for p, ti in enumerate(times[:-1]):
                if ti == min_time and len(dikes[p]) > 0:
                    time = ti
                    departure_ships = dikes[p].pop(0)
                    dikes[p + 1].append(departure_ships)
                    arrivals[p + 1].append(Ships(time, departure_ships))
                    if dikes[p]:
                        times[p] = time + dike_cycle(dikes[p])
                    else:
                        times[p] = INF
                    if len(dikes[p + 1]) == 1:
                        departure_ships = dikes[p + 1][0]
                        times[p + 1] = time + dike_cycle(departure_ships)
                    break
            else:
                if len(dikes[-1]) > 0:
                    time = times[-1]
                    number_of_departures += 1
                    departure_ships = dikes[-1].pop(0)
                    if dikes[-1]:
                        times[-1] = time + dike_cycle(dikes[-1])
                    else:
                        times[-1] = INF
                    departures.append(Ships(time, departure_ships))
                else:
                    return arrivals, departures
