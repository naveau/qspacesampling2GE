# q-space-sampling to GE

This script allows you to convert a `samples.txt` file generated
from the [Emmanuel Caruyer's web application](http://www.emmanuelcaruyer.com/q-space-sampling.php)
to a tensorXXX.dat file you can use for DTI sequences on a GE MRI System.

## Disclaimer

As usual it's "AS IS" and for research only !

## Cite

Please kindly cite the following relevant article when you use
the sampling scheme :

> Emmanuel Caruyer, Christophe Lenglet, Guillermo Sapiro, Rachid Deriche. Design of multishell sampling schemes with uniform coverage in diffusion MRI. Magnetic Resonance in Medicine, Wiley, 2013, 69 (6), pp. 1534-1540. http://dx.doi.org/10.1002/mrm.24736

## Usage

This installation was tested on a SIGNA Premier system (RX29.1).

Download your sample scheme from the [Emmanuel Caruyer's web application](http://www.emmanuelcaruyer.com/q-space-sampling.php)
Get the script and the file `samples.txt` to your home directory and open a terminal.

Generate the `tensorXXX.dat` from the `samples.txt` file (here with an example of [64 directions and 3 shells](http://www.emmanuelcaruyer.com/WebApp/q-space-sampling.php?nbPoints=64&nbShells=3&alpha=2)) :

```bash
python qspacesampling2ge.py samples.txt tensorXXX.dat 3000 2000 1000
```

Copy and rename the `tensorXXX.dat` to `/usr/g/bin/` (be careful to not erase previously existing tensor files) :

```bash
ls -l /usr/g/bin/tensor*
cp tensorXXX.dat /usr/g/bin/tensor666.dat
```

In a DTI sequence :
- Set the number of direction to the number you setup in the Q-space-sampling scheme
- Set the b-value to the maximum b-value of your shell
[Diffusion-setup](docs/q-space-sampling_diffusion-setup.png)
- use the advanced panel to setup the tensor file number.
[Advanced-setup](docs/q-space-sampling_advanced-setup.png)


## Tests

This script was tested on a 3T MRI SIGNA PREMIER system (MR29.1).

Using the same sampling described in the Usage section, here are the bvec/bval obtained after
converting the DICOM using [dcm2niix](https://github.com/rordenlab/dcm2niix)


