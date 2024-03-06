"""Utility to support common BT operations/methods."""
import datetime
from functools import partial
import logging

from mobly.controllers import android_device
from mobly.controllers.android_device_lib import adb
from bttc import common_data
from bttc import constants
from bttc.utils import device_factory
from bttc.utils import log_parser

import shlex
import re
from typing import Any, Callable, Sequence, TypeAlias, Union


BINDING_KEYWORD = 'bt'
AUTO_LOAD = True
ANDROID_DEVICE: TypeAlias = android_device.AndroidDevice

# Logcat message timestamp format
_DATETIME_FMT = constants.LOGCAT_DATETIME_FMT

# Pattern to match message of logcat service.
_LOGCAT_MSG_PATTERN = constants.LOGTCAT_MSG_PATTERN


class BTModule:
  """BT module to hold BT related functions define in this module."""

  def __init__(self, ad: ANDROID_DEVICE):
    self.crash_since = partial(crash_since, ad)
    self.dump_bluetooth_manager = partial(dump_bluetooth_manager, ad)
    self.enable_snoop_log = partial(enable_snoop_log, ad)
    self.enable_gd_log_verbose = partial(enable_gd_log_verbose, ad)
    self.get_bonded_devices = partial(get_bonded_devices, ad)
    self.get_device_mac_by_name = partial(get_device_mac_by_name, ad)
    self.get_connected_ble_devices = partial(get_connected_ble_devices, ad)
    self.get_current_le_audio_active_group_id = partial(
      get_current_le_audio_active_group_id, ad)
    self.is_le_audio_device_connected = partial(
        is_le_audio_device_connected, ad)
    self.is_enabled = partial(is_bluetooth_enabled, ad)
    self.list_paired_devices = partial(list_paired_devices, ad)
    self.shell = safe_adb_shell(ad)
    self.enable = partial(toggle_bluetooth, ad=ad, enabled=True)
    self.disable = partial(toggle_bluetooth, ad=ad, enabled=False)

  @property
  def bonded_devices(self):
    return self.get_bonded_devices()


def bind(
    ad: Union[ANDROID_DEVICE, str],
    init_mbs: bool = False, init_sl4a: bool = False,
    init_snippet_uiautomator: bool = False) -> ANDROID_DEVICE:
  """Binds the input device with functions defined in module `bt_utils`.

  Sample Usage:
  ```python
  >>> from bttc import bt_utils
  >>> ad = bt_utils.bind('35121FDJG0005P', init_mbs=True, init_sl4a=True)
  >>> ad.bt.is_bluetooth_enabled()
  True
  >>> ad.bt.list_paired_devices()
  ['Galaxy Buds2 Pro', 'Galaxy Buds2 Pro']
  ```

  Args:
    ad: If string is given, it stands for serial of device. Otherwise, it should
        be the Android device object.
    init_mbs: True to initialize the MBS service of given device.
    init_sl4a: True to initialize the SL4A service of given device.

  Returns:
    The device with binded functions defined in `bt_utils`.
  """
  device = device_factory.get(
      ad, init_mbs=init_mbs, init_sl4a=init_sl4a,
      init_snippet_uiautomator=init_snippet_uiautomator)
  device.load_config({BINDING_KEYWORD: BTModule(device)})

  return device


def crash_since(
    device: android_device.AndroidDevice,
    start_time: str | None = None) -> common_data.CrashInfo:
  """Collects crash timestamp.

  Usage example:
  ```python
  >>> import bttc
  >>> dut = bttc.get('36121FDJG000GR')
  >>> device_time = dut.gm.device_time
  >>> dut.bt.crash_since(device_time)  # We actually have two crash occurred before `device_time`  # noqa: E501
  CrashInfo(total_num_crash=2, collected_crash_times=[])
  >>> dut.bt.crash_since()  # Collect all crash time
  CrashInfo(total_num_crash=2, collected_crash_times=['02-07 08:55:35.085', '02-07 09:08:12.584'])
  >>> dut.bt.crash_since('02-07 08:56:35.085')  # Collect crash timestamp after  '02-07 08:56:35.085'
  CrashInfo(total_num_crash=2, collected_crash_times=['02-07 09:08:12.584'])
  ```

  Args:
    device: Adb like device.
    start_time: start time in string format of `_DATETIME_FMT`. If not give, all
      crash timestamp will be collected.

  Returns:
    Crash information including total crash count and collected crash timestamp.
  """
  start_datetime_obj = None
  try:
    if start_time:
      start_datetime_obj = datetime.datetime.strptime(start_time, _DATETIME_FMT)
  except ValueError as ex:
    logging.error('Invalid time format = "%s"!', start_time)
    raise ex

  crash_time_info = common_data.CrashInfo()
  bluetooth_crash_header_pattern = re.compile(
      r'Bluetooth crashed (?P<num_crash>\d+) time')

  # The interested parsing content will look lik:
  # usky:/ # dumpsys bluetooth_manager | grep -A 20 "Bluetooth crashed"
  # Bluetooth crashed 2 time
  # 02-07 08:55:35.085
  # 02-07 10:35:04.011
  #
  bt_manager_messages = dump_bluetooth_manager(device).split('\n')
  for i, line in enumerate(bt_manager_messages):
    matcher = bluetooth_crash_header_pattern.match(line)
    if matcher:
      crash_num = int(matcher.group('num_crash'))
      logging.info('Total %s crash being detected!', crash_num)
      crash_time_info.total_num_crash = crash_num
      for line_num in range(i+1, len(bt_manager_messages)):
        crash_time = bt_manager_messages[line_num].strip()
        if not crash_time:
          break

        crash_datetime_obj = datetime.datetime.strptime(
            crash_time, _DATETIME_FMT)
        if (
            not start_datetime_obj or
            crash_datetime_obj >= start_datetime_obj):
          crash_time_info.collected_crash_times.append(crash_time)

    if crash_time_info.total_num_crash >= 0:
      break

  return crash_time_info


def dump_bluetooth_manager(ad: android_device.AndroidDevice,
                           args: Sequence[str] = ()) -> str:
  """Dumps Bluetooth Manager log for the device.

  Args:
    args: Other arguments to be used in the dump command.

  Returns:
    Output of the dump command.
  """
  return ad.adb.shell(
      ('dumpsys', 'bluetooth_manager', *args)).decode()


def enable_snoop_log(ad: android_device.AndroidDevice) -> bool:
  """Enables Snoop log."""
  property_name = 'persist.bluetooth.btsnooplogmode'
  ad.log.info('Enabling Bluetooth Snoop log...')
  ad.adb.shell(f'setprop {property_name} full')
  property_setting = ad.adb.shell(
      f'getprop {property_name}').decode().strip()
  if property_setting == 'full':
    ad.log.info('Successfully enabled Bluetooth Snoop Log.')
    return True

  ad.log.warning(
      'Failed to enable Bluetooth Snoop Log with '
      'unexpected current setting="%s"', property_setting)
  return False


def enable_gd_log_verbose(ad: android_device.AndroidDevice) -> bool:
  """Enables bluetooth Gabeldorsche verbose log."""
  if int(ad.build_info['build_version_sdk']) >= 33:
    ad.log.info('Enabling Bluetooth GD verbose logging...')
    ad.adb.shell('device_config set_sync_disabled_for_tests persistent')
    ad.adb.shell('device_config put bluetooth '
                 'INIT_logging_debug_enabled_for_all true')
    out = ad.adb.shell(
        'device_config get bluetooth '
        'INIT_logging_debug_enabled_for_all').decode()
    if 'true' in out:
      ad.log.info('Successfully enabled Bluetooth GD verbose logging.')
      return True
  else:
    ad.log.warning(
        'Not TM or above build. Skip the enable GD verbose logging.')

  return False


def get_bonded_devices(
    ad: android_device.AndroidDevice) -> list[Any]:
  """Gets bonded device(s).

  Returns:
    List of collected bonded device.
  """
  return log_parser.parse_bonded_device_info(
      dump_bluetooth_manager(ad))


def get_connected_ble_devices(
    ad: android_device.AndroidDevice) -> list[dict[str, Any]]:
  """Returns devices connected through bluetooth LE.

  Returns:
       List of conncted le devices info.
  """
  return ad.sl4a.bluetoothGetConnectedLeDevices(
      constants.BluetoothProfile.GATT)


def get_current_le_audio_active_group_id(
    ad: android_device.AndroidDevice) -> int:
    """Gets current LE Audio active group ID.

    Returns:
      LE Audio group ID.
    """
    dump = dump_bluetooth_manager(
        ad, ('|', 'grep', '"currentlyActiveGroupId"', '||', 'echo', ' '))
    result = re.search(r'currentlyActiveGroupId: (.*)', dump)
    if result and result.group(1) != '-1':
      return int(result.group(1))
    ad.log.info('No LE Audio group active.')
    return -1


def get_device_mac_by_name(
    ad: android_device.AndroidDevice, bt_name: str) -> list[str]:
  """Gets MAC address of given device BT name."""

  paired_devices = ad.mbs.btGetPairedDevices()
  mac_address_list = []

  for device_info in paired_devices:
    if device_info['Name'] == bt_name:
      mac_address_list.append(device_info['Address'])

  if not mac_address_list:
    raise Exception(f'BT name={bt_name} not found!')

  return mac_address_list


def is_bluetooth_enabled(ad: android_device.AndroidDevice) -> bool:
  """Returns True iff Bluetooth is enabled."""
  return 'enabled: true' in dump_bluetooth_manager(
      ad, ('|', 'grep', '-A1', '"Bluetooth Status"', '||', 'echo', ' '))


def is_le_audio_device_connected(
    ad: android_device.AndroidDevice, mac_address: str) -> bool:
  """Checks if the LE Audio device is connected.

  Args:
    mac_address: Bluetooth MAC address of the LE Audio device.

  Returns:
    True iff the LE Audio device is connected.
  """
  # NOMUTANTS -- Grep keyword in dump.
  dump = dump_bluetooth_manager(ad, (
      '|', 'grep', '-B5',
      f'"group lead: XX:XX:XX:XX:{mac_address[-5:].upper()}"', '||', 'echo',
      ' '))
  return 'isConnected: true' in dump


def list_paired_devices(
    ad: android_device.AndroidDevice, only_name: bool = True):
  """Gets paired devices of given device."""
  paired_devices = ad.mbs.btGetPairedDevices()
  if only_name:
    return list(
        map(lambda paired_info: paired_info['Name'], paired_devices))

  return paired_devices


def safe_adb_shell(
    device: android_device.AndroidDevice,
    use_shlex_split: bool = True,
    timeout: float | None = None) -> Callable[[str], tuple[str, str, int]]:
  """Gets safe adb shell executor.

  Below is demo of this function:
  ```python
  >>> from bttc import bt_utils
  >>> from mobly.controllers import android_device
  >>> phone = android_device.create([{'serial': '07311JECB08252'}])[0]
  >>> safe_adb = bt_utils.safe_adb_shell(phone)
  >>> stdout, stderr, rt = safe_adb('getprop ro.build.version.sdk')
  >>> stdout  # My phone is of SDK 30.
  '30\n'
  ```

  Args:
    device: Adb like device.
    use_shlex_split: Leverage shlex.split iff True.
    timeout: float, the number of seconds to wait before timing out. If not
      specified, no timeout takes effect.

  Returns:
    Safe callable adb object.
  """

  def _adb_wrapper(command: str) -> tuple[str, str, int]:
    try:
      command = shlex.split(command) if use_shlex_split else command
      command_output = device.adb.shell(command, timeout=timeout).decode()
      return (command_output, '', 0)
    except adb.AdbError as err:
      return (err.stdout.decode(encoding='utf-8', errors='strict'),
              err.stderr.decode(encoding='utf-8',
                                errors='strict'), err.ret_code)
    except adb.AdbTimeoutError as err:
      device.log.warning('Timeout in executing command: %s', command)
      return ('', str(err), -1)

  return _adb_wrapper


def toggle_bluetooth(
    ad: android_device.AndroidDevice, enabled: bool = True) -> None:
  """Toggles Bluetooth on the device."""
  status = 'enable' if enabled else 'disable'
  cmd = f'svc bluetooth {status}'
  stdout, _, ret_code = safe_adb_shell(ad)(cmd)
  stdout = stdout.strip()
  # Expect 'disable: Success' or 'enable: Success'
  if ret_code == 0 and any([
      'Success' in stdout,
      stdout in {
          'Enabling Bluetooth',  # BDS's output
          '',  # SDK version < 33 (b/297539822#comment4)
      }]):
    return

  ad.log.warning(
      'Failed to toggle bluetooth with enabled=%s (rt=%s):\n%s\n',
      enabled, ret_code, stdout)

  raise RuntimeError(
      f'Failed in toggling bluetooth (enabled={enabled}) '
      f'with stdout: "{stdout}"')
