from argparse import ArgumentParser
from simulation import Simulation

parser = ArgumentParser()

parser.add_argument('-i', '--iter', type=int,
                    help='Simulation iterations. Default to 10.')
parser.add_argument('--nd', type=int,
                    help='Number of dikes. Default to 5.')
parser.add_argument('--rd', type=int,
                    help='Rows of dikes. Default to 2.')
parser.add_argument('--rs', type=int,
                    help='Row size. Default to 6.')

args = parser.parse_args()

number_of_dikes = args.nd if args.nd else 5
dike_rows = args.rd if args.rd else 2
size_rows = args.rs if args.rs else 6
iterations = args.iter if args.iter else 10

simulation = Simulation(number_of_dikes, dike_rows, size_rows)
simulation.run(iterations)

print(f'Result: {simulation.result}')
