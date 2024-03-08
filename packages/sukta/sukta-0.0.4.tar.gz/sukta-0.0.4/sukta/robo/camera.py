from dataclasses import dataclass

import numpy as np


@dataclass
class Camera:
    intrinsics: np.ndarray
    extrinsics: np.ndarray

    @property
    def I(self):
        """intrinsics"""
        return self.intrinsics

    @property
    def E(self):
        """intrinsics"""
        return self.extrinsics

    @property
    def T(self):
        """camera translation"""
        return self.extrinsics[:3, 3]

    @property
    def R(self):
        """camera rotation matrix"""
        return self.extrinsics[:3, :3]

    @property
    def proj_homo(self):
        """Homographic projection matrix"""
        R_inv = self.R.T  # inverse is the transpose
        return np.concatenate(
            [
                self.I @ np.concatenate([R_inv, -R_inv @ self.T[:, None]], axis=1),
                np.array([[0, 0, 0, 1.0]]),
            ]
        )


## point cloud helpers (ack: RLBench)
def _create_uniform_pixel_coords_image(height, width):
    pixel_x_coords = np.reshape(
        np.tile(np.arange(width), [height]),
        (height, width, 1),
    ).astype(np.float32)
    pixel_y_coords = np.reshape(
        np.tile(np.arange(height), [width]),
        (width, height, 1),
    ).astype(np.float32)
    pixel_y_coords = np.transpose(pixel_y_coords, (1, 0, 2))
    uniform_pixel_coords = np.concatenate(
        (pixel_x_coords, pixel_y_coords, np.ones_like(pixel_x_coords)), -1
    )
    return uniform_pixel_coords


def _pixel_to_world_coords(pixel_coords, cam_proj_mat_inv):
    h, w = pixel_coords.shape[:2]
    pixel_coords = np.concatenate([pixel_coords, np.ones((h, w, 1))], -1)
    world_coords = _transform(pixel_coords, cam_proj_mat_inv)
    world_coords_homo = np.concatenate([world_coords, np.ones((h, w, 1))], axis=-1)
    return world_coords_homo


def _transform(coords, trans):
    h, w = coords.shape[:2]
    coords = np.reshape(coords, (h * w, -1))
    coords = np.transpose(coords, (1, 0))
    transformed_coords_vector = np.matmul(trans, coords)
    transformed_coords_vector = np.transpose(transformed_coords_vector, (1, 0))
    return np.reshape(transformed_coords_vector, (h, w, -1))


def pointcloud_from_depth_and_camera_params(
    depth: np.ndarray, camera: Camera
) -> np.ndarray:
    """Converts depth (in meters) to point cloud in word frame.
    :return: A numpy array of size (width, height, 3)
    """
    upc = _create_uniform_pixel_coords_image(depth.shape)
    pc = upc * np.expand_dims(depth, -1)
    cam_proj_mat_homo = camera.proj_homo
    cam_proj_mat_inv = np.linalg.inv(cam_proj_mat_homo)[0:3]
    world_coords_homo = np.expand_dims(_pixel_to_world_coords(pc, cam_proj_mat_inv), 0)
    world_coords = world_coords_homo[..., :-1][0]
    return world_coords
