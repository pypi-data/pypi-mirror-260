import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
mu0 = np.pi*4e-7

class ObsPoint:
    def __init__(self, x=0., y=0., z=0., grid=True) -> None:
        self.x = np.array(x)
        self.y = np.array(y)
        self.z = np.array(z)
        
        if grid:
            self.grid()
        else:
            npoints = max(len(self.x), len(self.y),len(self.z))
            if len(self.x)==1: self.x = np.ones(npoints)*self.x
            if len(self.y)==1: self.y = np.ones(npoints)*self.y
            if len(self.z)==1: self.z = np.ones(npoints)*self.z

    def grid(self):
        X,Y,Z = np.meshgrid(self.x, self.y, self.z, indexing='ij')
        self.x = np.squeeze(X)
        self.y = np.squeeze(Y)
        self.z = np.squeeze(Z)
        return self
    
    @property
    def xyz(self):
        return np.squeeze(np.moveaxis(np.stack((self.x, self.y, self.z)), 0, -1))

    def __len__(self):
        return len(self.x.flatten())

@dataclass
class Loop:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray

    @classmethod
    def square(cls, side, **kwargs):
        half = side / 2.
        x = np.array([-half,  half, half, -half, -half])
        y = np.array([-half, -half, half,  half, -half])
        z = np.zeros_like(x)
        return cls(x, y, z)

    @classmethod
    def fig8(cls, side, **kwargs):
        half = side / 2.
        x = np.array([-side, 0, 0, side, side, 0, 0, -side, -side])
        y = np.array([-half, -half, half, half, -half, -half, half, half, -half])
        z = np.zeros_like(x)
        return cls(x, y, z)

    @classmethod
    def circle(cls, r, line=0.02):
        circumference = 2*np.pi*r
        n_seg = round(circumference / line)
        theta = np.linspace(0., 2*np.pi, n_seg)
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        z = np.zeros_like(x)
        return cls(x,y,z)

    @property
    def xyz(self):
        return np.moveaxis(np.stack((self.x,self.y,self.z)), 0, -1)

    def __len__(self):
        return len(self.x)
    
def biot_savart_finite_wire(x1, x2, y):
    """ calculate bfield for a finite wire. field observation point is at the origin by definition.
    """
    B3 = np.zeros(x1.shape+(3,))

    s = np.abs(y)
    s2 = s*s
    rs = 1./s
    del s
    sin_theta1 = x1 / np.sqrt(x1**2 + s2)
    sin_theta2 = x2 / np.sqrt(x2**2 + s2)
    del s2
    B = (sin_theta2 - sin_theta1)*rs
    B *= 1e-7
    B3[:, 2] = -B*y*rs

    return B3

def getR(P,Q):
    """https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d"""
    nhat = np.cross(P,Q, axis=-1)
    nhat /= np.linalg.norm(nhat, axis=-1)[:, None]

    zhat = np.array([0, 0, 1.])

    sign = nhat.dot(zhat)
    nhat[sign<0, :] *= -1.

    ab = nhat + zhat[None, :]
    num = np.einsum('...i,...j->...ij', ab, ab)
    den = np.einsum('...i,...i->...', ab, ab)

    R = 2*num / den[..., None, None]
    R += -np.eye(3)[None, :]
    iR = R.swapaxes(-1, -2)
    
    return R,iR

def getRz(P,Q):
    QP = Q-P
    mQP = np.linalg.norm(QP, axis=-1)
    cos_theta = QP[..., 0] / mQP
    sin_theta = QP[..., 1] / mQP

    Rz = np.zeros(QP.shape+(3,))

    Rz[..., 0,0] = cos_theta
    Rz[..., 1,1] = cos_theta
    Rz[..., 0,1] = sin_theta
    Rz[..., 1,0] = -sin_theta
    Rz[..., 2,2] = 1.
    
    return Rz, Rz.swapaxes(-1, -2)

def bfield_from_line(P,Q, xyz, I=1.):
    shp = xyz.shape
    assert shp[-1]==3, "position matrix must have 3 elements along the last axis"

    pt  = (P-xyz).reshape((-1,3))
    qt  = (Q-xyz).reshape((-1,3))

    R,iR = getR(pt,qt)

    pp  = np.einsum('...ij,...j->...i', iR, pt)
    qp  = np.einsum('...ij,...j->...i', iR, qt)

    Rz,iRz = getRz(pp,qp)

    ppp = np.einsum('...ij,...j->...i', Rz, pp)
    qpp = np.einsum('...ij,...j->...i', Rz, qp)

    Bpp = biot_savart_finite_wire(ppp[...,0], qpp[..., 0], ppp[...,1])
    Bp  = np.einsum('...ij,...j->...i', iRz, Bpp)
    B   = np.einsum('...ij,...j->...i', R, Bp).reshape(shp)
    
    if I!=1.: B *= I
    
    return B

def calc_bfield(loop, xyz, I=1.):
    n_segments = len(loop)-1
    Bfield = np.zeros_like(xyz)
    for i in range(n_segments):
        Bfield += np.nan_to_num(bfield_from_line(loop[i], loop[i+1], xyz))
    if I!=1.: Bfield*=I
    return Bfield