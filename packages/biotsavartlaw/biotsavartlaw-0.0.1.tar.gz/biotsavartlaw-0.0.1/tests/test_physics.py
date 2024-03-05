import numpy as np
import matplotlib.pyplot as plt
from biotsavart import *

def test_circle_loop_on_axis():
    
    I = 1.
    R = 1.
    lp = Loop.circle(R, line=0.1)

    z = np.linspace(-5, 5, 1001)
    r_obs = Loop(z*0, z*0, z).xyz # bit of a hack for making an observation grid
    
    bz = calc_bfield(lp.xyz, r_obs, I=I)[..., 2]
    bz_anly = 0.5*mu0*I*R**2 / (R**2 + z**2)**(3/2)
    assert np.allclose(bz, bz_anly), "on-axis circular loop test failed."

def test_circle_loop_on_axis_poor_approximation():

    I = 1.
    R = 1.
    lp = Loop.circle(R, line=0.5)

    z = np.linspace(-5, 5, 1001)
    r_obs = Loop(z*0, z*0, z).xyz # bit of a hack for making an observation grid
    
    bz = calc_bfield(lp.xyz, r_obs, I=I)[..., 2]
    bz_anly = 0.5*mu0*I*R**2 / (R**2 + z**2)**(3/2)
    assert not np.allclose(bz, bz_anly), "poor approximation for loop, so this should not be equal"

def test_infinite_wire_y_case():
    I = 1.

    y = np.array([1, -1])*1000
    l1 = Loop(y*0, y, y*0)
    
    x = np.geomspace(0.01, 10, 101)
    r_obs = Loop(x, x*0, x*0).xyz # bit of a hack for making an observation grid

    bfield = calc_bfield(l1.xyz, r_obs, I=I)

    b_analytical = mu0*I / (2*np.pi*x)

    assert np.allclose(np.log10(bfield[..., 2]), np.log10(b_analytical)), "infinite wire approximation test"


def test_infinite_wire_x_case():
    I = 1.

    x = np.array([-1, 1])*1000
    l1 = Loop(x, x*0., x*0)
    
    y = np.geomspace(0.01, 10, 101)
    r_obs = Loop(y*0, y, y*0).xyz # bit of a hack for making an observation grid

    bfield = calc_bfield(l1.xyz, r_obs, I=I)

    b_analytical = mu0*I / (2*np.pi*y)

    assert np.allclose(np.log10(bfield[..., 2]), np.log10(b_analytical)), "infinite wire approximation test x-direction"


