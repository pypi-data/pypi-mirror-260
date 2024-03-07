import sys
import numpy as np
import math
import aevmod
import pytest
import utils

# ====================================================================================================
def test_rad_indsets():

	types = ['C','H']
	myaev = aevmod.aev(types,8,4,4)

	symb, vxyz = utils.read_xyz("tests/xyz_c2h5.txt")
	cnf  = aevmod.config(symb)
	myaev.build_index_sets(cnf)

	ris = utils.read_rad_indsets("tests/ris_c2h5_8_4_4.txt")
	assert cnf.get_radial_index_set()  == ris
# ====================================================================================================
