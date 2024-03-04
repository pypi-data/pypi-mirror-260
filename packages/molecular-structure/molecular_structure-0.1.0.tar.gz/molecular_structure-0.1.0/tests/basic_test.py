# Here we will test the basic functionalities of the package
import unittest
from molecular_structure import MoleculeLevels


class TestCalculations(unittest.TestCase):

    def test_sum(self):
        print("Testing MoleculeLevels calculation")
        calculation = MoleculeLevels.initialize_state(
            "YbOH",
            "174",
            "X000",
            N_range=[0, 1, 2, 3],
            M_values="all",
            I=[0, 1 / 2],
            P_values=[1 / 2],
            S=1 / 2,
            round=6,
        )
        self.assertEqual(calculation is not None, True)


if __name__ == "__main__":
    unittest.main()
