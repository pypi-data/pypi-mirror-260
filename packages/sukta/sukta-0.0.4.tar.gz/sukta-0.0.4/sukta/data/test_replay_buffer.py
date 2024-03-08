import numpy as np

import sukta.tree_util as stu

from .replay_buffer import ReplayBuffer


def dummy_episode(T: int = 10):
    return {
        "obs": {
            "qpos": np.random.rand(T, 10).astype(np.float16),
            "qvel": np.random.rand(T, 10).astype(np.float16),
            "images": {
                "front": np.random.randint(0, 255, (T, 128, 128, 3), dtype=np.uint8),
            },
        },
        "action": np.random.rand(T, 2).astype(np.float32),
        "reward": np.random.rand(T).astype(np.float32),
    }


def test_replay_buffer_backend_numpy():
    rb = ReplayBuffer.create_empty_numpy()
    ep1 = dummy_episode(T=10)
    ep2 = dummy_episode(T=200)
    rb.add_episode(ep1)
    assert rb.n_episodes == 1
    assert rb.n_steps == 10
    rb.add_episode(ep2)
    assert rb.n_episodes == 2
    assert rb.n_steps == 210
    assert np.all(rb.episode_ends == np.asarray([10, 210]))

    ep = rb.get_episode(0)
    for k, v in stu.iter_path(ep):
        assert np.all(v == stu.dict_get_path(ep1, k))

    rb.drop_episode()
    assert rb.n_episodes == 1
    assert rb.n_steps == 10

    del rb


def test_replay_buffer_backend_zarr():
    # MemoryStore
    rb = ReplayBuffer.create_empty_zarr()
    ep1 = dummy_episode(T=10)
    rb.add_episode(ep1)
    assert rb.n_episodes == 1
    assert rb.n_steps == 10

    ep = rb.get_episode(0)
    for k, v in stu.iter_path(ep):
        assert np.all(v == stu.dict_get_path(ep1, k))

    del rb
