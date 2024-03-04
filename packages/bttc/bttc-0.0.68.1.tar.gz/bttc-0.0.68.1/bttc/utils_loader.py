"""Utility to load functional modules of device."""
from bttc import general_utils
from bttc import bt_utils
import dataclasses
import importlib
import pkgutil
from typing import Any


@dataclasses.dataclass
class FuncModuleInfo:
  name: str
  module: Any
  auto_load: bool = False

  @classmethod
  def from_module(cls, module):
    func_modu_info = FuncModuleInfo(
        name=module.BINDING_KEYWORD,
        module=module)
    if hasattr(module, 'AUTO_LOAD') and module.AUTO_LOAD:
      func_modu_info.auto_load = True

    return func_modu_info


def get_func_modules() -> dict[str, FuncModuleInfo]:
  loaded_module_info_map: dict[str, FuncModuleInfo] = {}
  candidate_module_names = (
      [name for _, name, _ in pkgutil.iter_modules(['bttc'])]
  )
  func_util_module_names = list(filter(
      lambda m: m.endswith('_utils'), candidate_module_names))

  if not func_util_module_names:
    for util_module in [general_utils, bt_utils]:
      module_info = FuncModuleInfo.from_module(util_module)
      loaded_module_info_map[util_module.BINDING_KEYWORD] = module_info
  else:
    for module_name in func_util_module_names:
      loaded_module = importlib.import_module(f'bttc.{module_name}')
      module_info = FuncModuleInfo.from_module(loaded_module)
      loaded_module_info_map[loaded_module.BINDING_KEYWORD] = module_info

  return loaded_module_info_map
