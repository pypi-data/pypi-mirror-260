import copy
import threading
from pathlib import Path

import dill
import torch

import sukta.tree_util as stu
from sukta.workspace import Workspace


class TorchWorkspace(Workspace):
    def set_seed(self, seed):
        super().set_seed(seed)
        torch.manual_seed(seed)

    def save_snapshot(self, tag: str = "latest") -> str:
        path = self.cfg.run_dir / "snapshots" / f"{tag}.pkl"
        path.parent.mkdir(parents=False, exist_ok=True)
        torch.save(self, path.open("wb"), pickle_module=dill)
        return str(path.absolute())

    @classmethod
    def create_from_snapshot(cls, path):
        return torch.load(open(path, "rb"), pickle_module=dill)

    def save_checkpoint(
        self, path: Path = None, tag: str = "latest", use_thread: bool = True
    ):
        if path is None:
            path = self.cfg.ckpt.save_dir / f"{tag}.ckpt"
        payload = {
            "cfg": self.cfg,
            "state_dict": dict(),
            "pickles": dict(),
        }
        for key, value in self.__dict__.items():
            if hasattr(value, "state_dict") and hasattr(value, "load_state_dict"):
                # modules, optimizers and samplers etc
                if key not in self.exclude_keys:
                    if use_thread:
                        payload["state_dicts"][key] = _copy_to_cpu(value.state_dict())
                    else:
                        payload["state_dicts"][key] = value.state_dict()
            elif key in self.include_keys:
                payload["pickles"][key] = dill.dumps(value)
        if use_thread:
            self._saving_thread = threading.Thread(
                target=lambda: torch.save(payload, path.open("wb"), pickle_module=dill)
            )
            self._saving_thread.start()
        else:
            torch.save(payload, path.open("wb"), pickle_module=dill)
        return str(path.absolute())

    def load_checkpoint(self, path: Path = None, tag: str = "latest", **kwargs):
        if path is None:
            path = self.cfg.ckpt.save_dir / f"{tag}.ckpt"
        if path.exists():
            self.log.info("Loading checkpoint %s", path)
            payload = torch.load(path.open("rb"), pickle_module=dill, **kwargs)
            self._load_payload(payload, **kwargs)

    @classmethod
    def create_from_checkpoint(cls, path: Path, **kwargs):
        payload = torch.load(open(path, "rb"), pickle_module=dill)
        instance = cls(payload["cfg"])
        instance._load_payload(payload, **kwargs)
        return instance

    def _load_payload(self, payload, **kwargs):
        for key, value in payload["state_dicts"].items():
            self.__dict__[key].load_state_dict(value, **kwargs)
        for key in self.include_keys:
            if key in payload["pickles"]:
                self.__dict__[key] = dill.loads(payload["pickles"][key])


def _copy_to_cpu(x):
    return stu.apply_vfunc(
        stu.type_cond_func(
            {
                torch.Tensor: lambda v: v.detach().clone().to("cpu"),
            },
            fallback=copy.deepcopy,
        ),
        x,
    )
