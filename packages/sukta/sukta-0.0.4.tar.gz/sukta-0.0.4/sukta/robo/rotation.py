import numpy as np
from scipy.spatial.transform import Rotation as R


def delta_quaternion(q1: np.ndarray, q2: np.ndarray):
    return (R.from_quat(q2) * R.from_quat(q1).inv()).as_quat()


def axis_angle_to_matrix(axis_angle: np.ndarray):
    return R.from_rotvec(axis_angle).as_matrix()


def matrix_to_axis_angle(matrix: np.ndarray):
    return R.from_matrix(matrix).as_rotvec()


def quaternion_to_matrix(quaternion: np.ndarray):
    return R.from_quat(quaternion).as_matrix()


def matrix_to_quaternion(matrix: np.ndarray):
    return R.from_matrix(matrix).as_quat()


def euler_to_matrix(euler: np.ndarray, degrees=False):
    return R.from_euler("xyz", euler, degrees=degrees).as_matrix()


def matrix_to_euler(matrix: np.ndarray, degrees=False):
    return R.from_matrix(matrix).as_euler("xyz", degrees=degrees)


## From PyTorch3D
def matrix_to_rotation_6d(matrix: np.ndarray):
    """
    Converts rotation matrices to 6D rotation representation by Zhou et al. [1]
    by dropping the last row. Note that 6D representation is not unique.
    Args:
        matrix: batch of rotation matrices of size (*, 3, 3)

    Returns:
        6D rotation representation, of size (*, 6)

    [1] Zhou, Y., Barnes, C., Lu, J., Yang, J., & Li, H.
    On the Continuity of Rotation Representations in Neural Networks.
    IEEE Conference on Computer Vision and Pattern Recognition, 2019.
    Retrieved from http://arxiv.org/abs/1812.07035
    """
    return matrix[..., :2, :].copy().reshape(matrix.shape[:-2] + (6,))


def rotation_6d_to_matrix(d6: np.ndarray):
    """
    Converts 6D rotation representation by Zhou et al. [1] to rotation matrix
    using Gram--Schmidt orthogonalization per Section B of [1].
    Args:
        d6: 6D rotation representation, of size (*, 6)

    Returns:
        batch of rotation matrices of size (*, 3, 3)

    [1] Zhou, Y., Barnes, C., Lu, J., Yang, J., & Li, H.
    On the Continuity of Rotation Representations in Neural Networks.
    IEEE Conference on Computer Vision and Pattern Recognition, 2019.
    Retrieved from http://arxiv.org/abs/1812.07035
    """
    a1, a2 = d6[..., :3], d6[..., 3:]
    b1 = a1 / np.linalg.norm(a1, ord=2, axis=-1, keepdims=True).clip(min=1e-12)
    b2 = a2 - (b1 * a2).sum(axis=-1, keepdims=True) * b1
    b2 = b2 / np.linalg.norm(b2, ord=2, axis=-1, keepdims=True).clip(min=1e-12)
    b3 = np.cross(b1, b2)
    return np.stack((b1, b2, b3), axis=-2)
