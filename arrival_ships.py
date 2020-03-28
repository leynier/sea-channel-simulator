from distributions import normal_distribution

parameters_table = [
    [(5, 2), (3, 1), (10, 2)], # Smaller
    [(15, 3), (10, 5), (20, 5)], # Medium
    [(45, 3), (35, 7), (60, 9)] # Bigger
]


class Ship:
    def __init__(self, time, size):
        self.time = time
        self.size = size

    def __iter__(self):
        return iter([self.time, self.size])

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        return self.time == other.time and self.size == other.size


class Ships:
    def __init__(self, time, ships):
        self.time = time
        self.ships = ships

    def __iter__(self):
        return iter([self.time, self.ships])


class ArrivalShips:
    def __init__(self, dike_rows=2, size_rows=6):
        self.dike_rows = dike_rows
        self.size_rows = size_rows

    def __parameters(self, time, size):
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
        assert False, f'Invalid parameters - time: {time}, size: {size}'

    def __distribution(self, time, size):
        mu, sigma2 = self.__parameters(time, size)
        return abs(normal_distribution(mu, sigma2 ** 0.5))

    def __iter__(self):
        time = 0
        ships_list = list()
        d = self.__distribution
        ships = [Ship(d(0, 1), 1), Ship(d(0, 2), 2), Ship(d(0, 4), 4)]
        while True:
            ship = min(ships)
            if ship.time > 720:
                break
            ships_list.append(ship)
            ships.remove(ship)
            ships.append(Ship(ship.time + d(*ship), ship.size))
        ships = ships_list
        while ships:
            next_ships = list()
            skips_ships = list()
            dike = [0 for _ in range(self.dike_rows)]
            for ship in ships:
                skip = True
                for index, row in enumerate(dike):
                    if ship.size + row <= self.size_rows:
                        dike[index] += ship.size
                        next_ships.append(ship)
                        skip = False
                        break
                if skip:
                    skips_ships.append(ship)
            time = max(time, max(next_ships).time)
            yield Ships(time, next_ships)
            ships = skips_ships
