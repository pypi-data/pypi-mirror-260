"""Module to hold dataclass or related data used in Bluetooth operations."""

import dataclasses
from bttc import constants


@dataclasses.dataclass
class BondedDeviceInfo:
  """Information of bonded device collected by bluetooth manager."""

  mac_addr: str
  bt_type: constants.BluetoothDeviceType
  name: str
