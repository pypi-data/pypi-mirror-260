import sys
import numpy as np
import math
import aevmod
import pytest
import utils

# ====================================================================================================
def test_jac():

	types = ['C','H']
	myaev = aevmod.aev(types,8,4,4)

	symb, vxyz = utils.read_xyz("tests/xyz_c2h5.txt")
	cnf  = aevmod.config(symb)
	myaev.build_index_sets(cnf)

	npt  = cnf.add_structures(vxyz);

	nptt, n_atom, dout, din, tru_jac = utils.read_jac("tests/jac_c2h5_8_4_4.txt");
	got_jac = myaev.eval_Jac(cnf)
	
	try:
		assert nptt == npt
		assert np.allclose(got_jac,tru_jac, rtol=1.e-15, atol=1.e-15)
	except AssertionError:
	    print("got_jac disagrees with tru_jac")
	    errmx = 0.0
	    for p in range(npt):
	        for a in range(n_atom):
	            for r in range(dout):
	            	for k in range(din):
	                	errmx=max(errmx,abs(got_jac[p][a][r][k]-tru_jac[p][a][r][k]))
	    print("errmx:",errmx)
	    sys.exit(1)

# ====================================================================================================
