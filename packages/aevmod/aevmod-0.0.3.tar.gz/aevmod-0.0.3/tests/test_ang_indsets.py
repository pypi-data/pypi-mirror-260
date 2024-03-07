import sys
import numpy as np
import math
import aevmod
import pytest
import utils

# ====================================================================================================
def test_ang_indsets():

	types = ['C','H']
	myaev = aevmod.aev(types,8,4,4)

	symb, vxyz = utils.read_xyz("tests/xyz_c2h5.txt")
	cnf  = aevmod.config(symb)
	myaev.build_index_sets(cnf)

	ais = utils.read_ang_indsets("tests/ais_c2h5_8_4_4.txt")
	assert cnf.get_angular_index_set() == ais

# ====================================================================================================
