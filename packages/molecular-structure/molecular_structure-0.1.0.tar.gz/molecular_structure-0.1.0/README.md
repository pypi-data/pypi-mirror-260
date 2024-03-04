# Molecular-Structure

Python code to calculate molecular energy levles and shifts.
The way the code is structured is to allow for easy calculation of the energy levels of a molecule, and the shifts of these levels in the presence of an electric and magnetic field, along with the hyperfine structure.

## Installation

To install this code we recommend using a brand new conda environment

```bash
conda create -n envMolecularStructure python=3.11 -y
conda activate envMolecularStructure
```

After this just pip install the repo. In your terminal, run:

```bash
git clone git
cd Molecule-Structure
pip install .
```

If you want to check that the installation was successful, you can run the tests:

```bash
python -m unittest python -m unittest Molecule-Structure/tests/basic_test.py
```

## Usage

```python
from molecular_structure import MoleculeLevels
X = MoleculeLevels.initialize_state('YbOH','174','X000',
                                    N_range=[0,1,2,3], M_values = 'all',
                                    I=[0,1/2],
                                    P_values=[1/2], S=1/2, round=6)
sy.N(X.H_symbolic[:6,:6],2)
```
```latex
$\displaystyle \left[\begin{matrix}-72.0 & 0 & 1.4 B_{z} & 0 & 0 & 0\\0 & 24.0 - 1.4 B_{z} & 0 & 0 & 0 & - 0.66 E_{z}\\1.4 B_{z} & 0 & 24.0 & 0 & 0.66 E_{z} & 0\\0 & 0 & 0 & 1.4 B_{z} + 24.0 & 0 & 0\\0 & 0 & 0.66 E_{z} & 0 & 1.1 \cdot 10^{4} & 0\\0 & - 0.66 E_{z} & 0 & 0 & 0 & 0.47 B_{z} + 1.1 \cdot 10^{4}\end{matrix}\right]$
```

There are plenty of examples on how to use the code in the `notebooks` folder.
We recommend you to start with:

- [RaF molecule](./notebooks/RaX/RaF_Calcs_Tutorial.ipynb)



## Developer

The physics of all the repository was developed by [Arian Jadbabaie](https://iqim.caltech.edu/profile/arian-jadbabaie/).

Slight refactoring by [Jose M Munoz](munozariasjm.github.io)

**EMA Lab**
*Laboratory for Nuclear Science, MIT*