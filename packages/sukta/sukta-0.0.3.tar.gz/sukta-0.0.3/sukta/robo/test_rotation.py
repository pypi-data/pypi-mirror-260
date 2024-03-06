from scipy.spatial.transform import Rotation as R
import numpy as np

from .rotation import matrix_to_rotation_6d, rotation_6d_to_matrix
import pdb


def test_rotation_6d():
    r = R.random(1_000_000)
    m = r.as_matrix()
    d6 = matrix_to_rotation_6d(m)
    m_p = rotation_6d_to_matrix(d6)
    assert np.isclose(m_p, m).all()
