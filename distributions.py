from random import random
from scipy import array, log, e


def exponential_distribution(alpha):
    return - log(random()) / alpha


def normal_distribution(mu, sigma):
    while True:
        exp = exponential_distribution(1)
        if random() <= e ** (-(exp - 1) ** 2 / 2):
            return sigma * exp + mu
