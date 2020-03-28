from arrival_ships import ArrivalShips, Ships
from distributions import exponential_distribution


class Simulation:
    INF = 2 ** 64

    def __init__(self, number_of_dikes=5, dike_rows=2, size_rows=6):
        self.number_of_dikes = number_of_dikes
        self.dike_rows = dike_rows
        self.size_rows = size_rows
        self.result = None

    def __cycle(self, ships):
        d = exponential_distribution
        return d(4) + sum(d(2) for _ in ships) + d(7) + d(1.5 * len(ships))

    def __process(self):
        generator_ships = iter(ArrivalShips(self.dike_rows, self.size_rows))
        finished = False
        time = 0
        number_of_arrivals = 0
        number_of_departures = 0
        dikes = [[] for _ in range(self.number_of_dikes)]
        arrivals = [[] for _ in range(self.number_of_dikes)]
        departures = []
        times = [Simulation.INF for _ in range(self.number_of_dikes)]
        try:
            arrival = next(generator_ships)
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
                    arrival = next(generator_ships)
                except StopIteration:
                    finished = True
                if len(dikes[0]) == 1:
                    departure_ships = dikes[0][0]
                    times[0] = time + self.__cycle(departure_ships)
            else:
                for p, ti in enumerate(times[:-1]):
                    if ti == min_time and len(dikes[p]) > 0:
                        time = ti
                        departure_ships = dikes[p].pop(0)
                        dikes[p + 1].append(departure_ships)
                        arrivals[p + 1].append(Ships(time, departure_ships))
                        if dikes[p]:
                            times[p] = time + self.__cycle(dikes[p])
                        else:
                            times[p] = Simulation.INF
                        if len(dikes[p + 1]) == 1:
                            departure_ships = dikes[p + 1][0]
                            times[p + 1] = time + self.__cycle(departure_ships)
                        break
                else:
                    if len(dikes[-1]) > 0:
                        time = times[-1]
                        number_of_departures += 1
                        departure_ships = dikes[-1].pop(0)
                        if dikes[-1]:
                            times[-1] = time + self.__cycle(dikes[-1])
                        else:
                            times[-1] = Simulation.INF
                        departures.append(Ships(time, departure_ships))
                    else:
                        return arrivals, departures

    def run(self, iterations=10):
        self.result = 0
        for _ in range(iterations):
            result = 0
            _, departures = self.__process()
            for time, ships in departures:
                result += sum(time - ship.time for ship in ships)
            self.result += result
        self.result /= iterations
