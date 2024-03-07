# SPDX-FileCopyrightText: 2023 Helge
# SPDX-FileCopyrightText: 2024 Helge
#
# SPDX-License-Identifier: MIT

from glob import glob
import importlib.util

available = {}


for file_path in glob(f"{__file__.removesuffix('__init__.py')}/*.py"):
    if (
        not file_path.endswith("__init__.py")
        and not file_path.endswith("types.py")
        and not file_path.endswith("utils.py")
        and "test_" not in file_path
    ):
        module_name = (
            "fediverse_pasture_inputs." + file_path.split(".")[0].split("/")[-1]
        )

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        try:
            available[module.data.filename.removesuffix(".md")] = module.data
        except Exception:
            print(file_path)
