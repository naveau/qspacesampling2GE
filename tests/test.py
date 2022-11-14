import argparse
import math
from os import path

parser = argparse.ArgumentParser()
parser.add_argument('--samples', type=argparse.FileType('r'),
    help='Sample.txt generate from http://www.emmanuelcaruyer.com/q-space-sampling.php',
    default='samples_points-64_nbShells-3_alpha-2.txt')
parser.add_argument('--bvec', type=argparse.FileType('r'),
    help='bvec file generated by dcm2niix : https://github.com/rordenlab/dcm2niix',
    default='GE_dcm2niix.bvec')
parser.add_argument('--bval', type=argparse.FileType('r'),
    help='bvec file generated by dcm2niix : https://github.com/rordenlab/dcm2niix',
    default='GE_dcm2niix.bval')
parser.add_argument('--bvalues', nargs='+', type=float,
    help='B-Values vector separated by spaces (i.e: 1000 2000 3000). Number must match the shells in [samples]',
    default=[1000, 2000, 3000])

args = parser.parse_args()

# Some verbose about the arguments
print('Arguments :')
print('-----------')
print('Samples file: {}'.format(args.samples.name))
print('bvec file   : {}'.format(args.bvec.name))
print('bval file   : {}'.format(args.bval.name))
print('')
print('Testing samples match bval/bvec...')
print('')

# Read the samples file and do some sanity check
shells = []
u_x = []
u_y = []
u_z = []
for l in args.samples.readlines():
    if l.startswith('#'):
        # Header of the file
        continue
    data = l.split()
    try:
        shells.append(int(data[0]))
    except ValueError:
        print('ERROR: samples.txt file seems wrong. Shells are not integer, please check the input file')
        exit(1)
    try:
        u_x.append(float(data[1]))
        u_y.append(float(data[2]))
        u_z.append(float(data[3]))
    except ValueError:
        print('ERROR: samples.txt file seems wrong. Vectors coordinates are not numbers, please check the input file')
        exit(1)

expected_bvals = [args.bvalues[s-1] for s in shells]

# Read the bvec (remove the first one: b=0)
ge_x = args.bvec.readline().split()
ge_x = [float(x) for x in ge_x[1:]]
ge_y = args.bvec.readline().split()
ge_y = [float(y) for y in ge_y[1:]]
ge_z = args.bvec.readline().split()
ge_z = [float(z) for z in ge_z[1:]]

# Read the bval (remove the first one: b=0)
ge_b = args.bval.readline().split()
ge_b = [float(b) for b in ge_b[1:]]

# Skip bvals == 0
ge_x = [i for i,b in zip(ge_x, ge_b) if b!=0]
ge_y = [i for i,b in zip(ge_y, ge_b) if b!=0]
ge_z = [i for i,b in zip(ge_z, ge_b) if b!=0]
ge_b = [b for b in ge_b if b!=0]

# Check number of direction match
if len(expected_bvals) != len(ge_b):
    print('Number of directions do not match: expected {} directions / got {} directions'.format(
        len(expected_bvals), len(ge_b)))
    exit(1)

for i in range(len(expected_bvals)):

    if expected_bvals[i] != ge_b[i]:
        print("DIR{} Found bvalues mismatch : expected {} / got {}".format(
            i, expected_bvals[i], ge_b[i]))

    # test direction to 0.001 (precision of the q-space-sampling file)
    if abs(u_x[i] - ge_x[i]) > 0.001:
        print("DIR{} Found direction mismatch in X : expected {} / got {}".format(
            i, u_x[i], ge_x[i]))
    if abs(u_y[i] - ge_y[i]) > 0.001:
        print("DIR{} Found direction mismatch in Y : expected {} / got {}".format(
            i, u_y[i], ge_y[i]))
    if abs(u_z[i] - ge_z[i]) > 0.001:
        print("DIR{} Found direction mismatch in Z : expected {} / got {}".format(
            i, u_z[i], ge_z[i]))


print('If nothing written before this line, it seems good !')
