import sys
import numpy as np
import math
import aevmod
import pytest
import utils

# ====================================================================================================
def test_hes():

	types = ['C','H']
	myaev = aevmod.aev(types,8,4,4)

	symb, vxyz = utils.read_xyz("tests/xyz_c2h5.txt")
	cnf  = aevmod.config(symb)
	myaev.build_index_sets(cnf)
	npt  = cnf.add_structures(vxyz);

	nptt, n_atom, dout, din, tru_hes = utils.read_hes("tests/hes_c2h5_8_4_4.txt");
	got_hes = myaev.eval_Hess_sac(cnf)
	try:
		assert nptt == npt
		assert np.allclose(got_hes,tru_hes, rtol=1.e-15, atol=1.e-14)
	except AssertionError:
	    print("got_hes disagrees with tru_hes")
	    errmx = 0.0
	    for p in range(npt):
	        for a in range(n_atom):
	            for r in range(dout):
	            	for k in range(din):
	            		for l in range(din):
	                		errmx=max(errmx,abs(got_hes[p][a][r][k][l]-tru_hes[p][a][r][k][l]))
	    print("errmx:",errmx)
	    sys.exit(1)


# ====================================================================================================
