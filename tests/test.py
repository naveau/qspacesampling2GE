# Read the samples file and do some sanity check
shells = []
u_x = []
u_y = []
u_z = []
with open('samples_points-64_nbShells-3_alpha-2.txt', 'r') as f:
    for l in f.readlines():
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

bvalues = [3000, 2000, 1000]
expected_bvals = [bvalues[s-1] for s in shells]

# Read the bvec (remove the first one: b=0)
with open('GE_dcm2niix.bvec', 'r') as f:
    ge_x = f.readline().split()
    ge_x = [float(x) for x in ge_x[1:]]
    ge_y = f.readline().split()
    ge_y = [float(y) for y in ge_y[1:]]
    ge_z = f.readline().split()
    ge_z = [float(z) for z in ge_z[1:]]

# Read the bval (remove the first one: b=0)
with open('GE_dcm2niix.bval', 'r') as f:
    ge_b = f.readline().split()
    ge_b = [float(b) for b in ge_b[1:]]

for i in range(len(expected_bvals)):
    if expected_bvals[i] != ge_b[i]:
        print("DIR{} Found bvalues mismatch : expected {} / got {}".format(
            i, expected_bvals[i], ge_b[i]))
    if u_x[i] != ge_x[i]:
        print("DIR{} Found direction mismatch in X : expected {} / got {}".format(
            i, u_x[i], ge_x[i]))
    if u_y[i] != ge_y[i]:
        print("DIR{} Found direction mismatch in Y : expected {} / got {}".format(
            i, u_y[i], ge_y[i]))
    if u_z[i] != ge_z[i]:
        print("DIR{} Found direction mismatch in Z : expected {} / got {}".format(
            i, u_z[i], ge_z[i]))


