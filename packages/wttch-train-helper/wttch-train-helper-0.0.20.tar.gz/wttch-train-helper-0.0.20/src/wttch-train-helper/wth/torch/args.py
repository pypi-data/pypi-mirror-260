import torch

from .utils import try_gpu, set_device_local, set_dtype_local

import json
import sys

import yaml


class Config:
    """
    环境配置，使用 yml 文件。
    例如:
    ```
    active: local
      school-server:
      local:
        epochs: 10
        batch-size: 64
        dtype: float32
        cuda_no: 1
        dataset_path: /your/dataset/path
    ```
    active 必需标识启用的环境。
    后续使用 key: 环境配置的方式可以定义多个环境。
    """

    def __init__(self, config_file='config.yml'):
        """
        构造函数。
        Args:
            config_file: 配置文件所在位置，默认 config.yml。
        """
        with open(config_file) as f:
            self.original = yaml.load(f, Loader=yaml.FullLoader)
            self.active_profile = self.original['active']
            if self.active_profile is None:
                raise ValueError("No active profile")

            print(f"Active profile[{self.active_profile}].")
            sys.stdout.flush()

            self.args = self.original[self.active_profile]  # type: dict
            if self.args is None:
                print(f"Active profile[{self.active_profile}] has no arguments.", file=sys.stderr)
                sys.stderr.flush()
                self.args = {}
            self.epochs = self.args.get('epochs', 10)
            self.batch_size = self.args.get('batch-size', 64)
            self.dtype = self.args.get('dtype', 'float32')
            self.cuda_no = self.args.get('cuda-no')
            self.dataset_path = self.args.get('dataset-path')

        # 设置设备
        if self.cuda_no is not None:
            set_device_local(try_gpu(self.cuda_no))
        # 设置 dtype
        if self.dtype is not None:
            if self.dtype == 'float32':
                set_dtype_local(torch.float32)
            else:
                set_dtype_local(torch.float64)

    def __getitem__(self, item):
        if self.args.__contains__(item):
            return self.args[item]
        key = item.replace("_", "-")
        if self.args.__contains__(key):
            return self.args[key]
        return None

    def __str__(self):
        return json.dumps(self.original)
