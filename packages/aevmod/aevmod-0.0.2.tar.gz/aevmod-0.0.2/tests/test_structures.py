# nb. source code must be called test_base.py

import sys
import numpy as np
import math
import aevmod
import pytest
import utils

# ====================================================================================================
def test_structures():

	types = ['C','H']
	myaev = aevmod.aev(types,8,4,4)

	symb, vxyz = utils.read_xyz("tests/xyz_c2h5.txt")
	cnf  = aevmod.config(symb)

	npt   = cnf.add_structures(vxyz);
	np.testing.assert_array_equal(vxyz,cnf.get_structures())
# ====================================================================================================
