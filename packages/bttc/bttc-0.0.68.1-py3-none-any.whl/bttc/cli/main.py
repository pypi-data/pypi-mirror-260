"""Entry point of BTTC Cli prompt."""

import cmd2
import copy
import contextlib
import datetime
import functools
import logging
import mobly
import os
from ppadb import client
from pprint import pprint
import re
import sys

import bttc
from bttc import constants as bttc_constants
from bttc.cli import constants
from bttc.utils import device_factory


Color = constants.Color
EXIST_MSG = 'Welcome to use BTTC Cli and see you next time!'
MAIN_COMMANDS = "Main Commands"

select_parser = cmd2.Cmd2ArgumentParser()
select_parser.add_argument(
    '-s', '--serial', type=str, default=None, help='DUT serial')

logcat_filter_parser = cmd2.Cmd2ArgumentParser()
logcat_filter_parser.add_argument(
    '--logcat_wait_sec', type=int, default=10,
    help='Time in sec to follow logcat.')
logcat_filter_parser.add_argument(
    '--logcat_only_match', type=bool, default=False,
    help='Setup to show only matched line')


def dec_require_dut(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    self = args[0]
    is_dut_ready = False
    if isinstance(self, BttcCmdApp) and self._dut:
      is_dut_ready = True
    elif hasattr(self, '_app') and self._app._dut:
      is_dut_ready = True

    if not is_dut_ready:
      logging.warning('Please select your DUT first!')
      return

    return func(*args, **kwargs)

  return wrapper


def dec_require_sl4a(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    self = args[0]
    is_sl4a_ready = False
    if isinstance(self, BttcCmdApp) and self._dut:
      is_sl4a_ready = 'sl4a' in self._dut.services.list_live_services()
    elif hasattr(self, '_app') and self._app._dut:
      is_sl4a_ready = 'sl4a' in self._app._dut.services.list_live_services()

    if not is_sl4a_ready:
      logging.warning('Please load SL4A in DUT first!')
      return

    return func(*args, **kwargs)

  return wrapper


@cmd2.with_default_category('Properties')
class PropsCommandSet(cmd2.CommandSet):
  def __init__(self, app: 'BttcCmdApp'):
    super().__init__()
    self._app = app

  @dec_require_dut
  def do_airplane_mode_state(self, args):
    self._app.poutput(
        f'Airplane state: {self._app._dut.gm.airplane_mode_state}\n')

  @dec_require_dut
  def do_device_info(self, args):
    device_info = copy.copy(self._app._dut.device_info)
    device_info['init_sl4a'] = self._app.dut_init_sl4a
    device_info['init_snippet_uiautomator'] = (
        self._app.dut_init_snippet_uiautomator)
    pprint(device_info)
    print('')

  @dec_require_dut
  def do_build_id(self, args):
    self._app.poutput(f'Model: {self._app._dut.build_id}\n')

  @dec_require_dut
  def do_model(self, args):
    self._app.poutput(f'Model: {self._app._dut.model}\n')

  @dec_require_dut
  def do_sdk(self, args):
    self._app.poutput(f'SDK: {self._app._dut.gm.sdk}\n')


@cmd2.with_default_category('BT')
class BTCommandSet(cmd2.CommandSet):
  def __init__(self, app: 'BttcCmdApp'):
    super().__init__()
    self._app = app

  @dec_require_dut
  def do_bonded_devices(self, args):
    bonded_devices = self._app._dut.bt.bonded_devices
    self._app.poutput(f'Total {len(bonded_devices)} bonded devices:')
    for bonded_device in bonded_devices:
      print(f'\t{bonded_device}')

    print('')

  @dec_require_sl4a
  def do_sl4a_bonded_devices(self, args):
    """Shows bonded device(s)."""
    bonded_devices = self._app._dut.sl4a.bluetoothGetBondedDevices()
    if not bonded_devices:
      self._app.poutput('No bonded device!\n')
      return

    self._app.poutput(f'Total {len(bonded_devices)} bonded devices:')
    for d in bonded_devices:
      d['state'] = bttc_constants.BluetoothBondedState.from_int(d['state'])
      d['type'] = bttc_constants.BluetoothDeviceType.from_int(d['type'])
      print(f'\t- {d}')

    print('')

  crash_since_parser = cmd2.Cmd2ArgumentParser()
  crash_since_parser.add_argument(
      '--hour', type=int, default=-1,
      help='Look back for # hour(s).')
  crash_since_parser.add_argument(
      '-m', '--minute', type=int, default=-1,
      help='Look back for # minute(s).')

  @dec_require_dut
  @cmd2.with_argparser(crash_since_parser)
  def do_crash_since(self, args):
    """Collects crash information within certain time in the past."""
    search_datetime = self._app._dut.gm.device_datetime
    if args.hour > 0:
      search_datetime = (
          search_datetime - datetime.timedelta(hours=args.hour))

    if args.minute > 0:
      search_datetime = (
          search_datetime - datetime.timedelta(minutes=args.minute))

    if args.hour < 0 and args.minute < 0:
      self._app.poutput('Collects all crash...')
      search_datetime = None
    else:
      self._app.poutput(f'Collects crash after {search_datetime}...')

    crash_since_datetime_str = (
        datetime.datetime.strftime(
            search_datetime, bttc_constants.LOGCAT_DATETIME_FMT)
        if search_datetime else None)

    crash_info = self._app._dut.bt.crash_since(crash_since_datetime_str)
    self._app.poutput(f'{crash_info}\n')

  @dec_require_dut
  def do_enable_snoop_log(self, args):
    """Enables snoop log."""
    if self._app._dut.bt.enable_snoop_log():
      self._app.poutput('Snoop log is enabled!\n')
    else:
      self._app.poutput('Failed to set snoop log!\n')

  @dec_require_sl4a
  def do_sl4a_local_name(self, args):
    """Gets device's local name by SL4A."""
    device_name = self._app._dut.sl4a.bluetoothGetLocalName()
    self._app.poutput(f'Local name: {device_name}\n')

  @dec_require_sl4a
  def do_sl4a_mac_address(self, args):
    """Gets device's MAC address by SL4A."""
    mac_addr = self._app._dut.sl4a.bluetoothGetLocalAddress()
    self._app.poutput(f'MAC address: {mac_addr}\n')


@cmd2.with_default_category('UI')
class UICommandSet(cmd2.CommandSet):
  def __init__(self, app: 'BttcCmdApp'):
    super().__init__()
    self._app = app

  ui_dump_parser = cmd2.Cmd2ArgumentParser()
  ui_dump_parser.add_argument(
      'path', nargs='*',
      help='File path to dump the current UI page.')

  @dec_require_dut
  @cmd2.with_argparser(ui_dump_parser)
  def do_take_screenshot(self, args):
    """Takes screenshot of UI page and save it to host."""
    dump_path_list = args.path or ['/tmp/test.png']
    for path in dump_path_list:
      with contextlib.suppress(FileNotFoundError):
        os.remove(path)
      self._app.poutput(f'Save UI screenshot to {path}...\n')
      self._app._dut.gm.take_screenshot(path)

    print('')

  @dec_require_dut
  @cmd2.with_argparser(ui_dump_parser)
  def do_ui_dump_to(self, args):
    """Dump current UI page to host."""
    dump_path_list = args.path or ['/tmp/test.xml']
    for path in dump_path_list:
      self._app.poutput(f'Dump UI page to {path}...\n')
      self._app._dut.gm.get_ui_xml(path)

    print('')


class BttcCmdApp(cmd2.Cmd):
  """BTTC  cmd2 application."""
  MAIN_PROMPT = f'{Color.BOLD}{Color.BLUE}bttc>{Color.END} '
  DEVICE_PROMPT_PROMPT = (
      f'{Color.BOLD}{Color.BLUE}bttc/{Color.YELLOW}' + r'{serial}' +
      Color.BLINK_SLOW + '> ' + Color.END)

  def __init__(self, serial: str | None = None):
    super().__init__(
        shortcuts=cmd2.DEFAULT_SHORTCUTS,
        command_sets=[
            UICommandSet(self), PropsCommandSet(self), BTCommandSet(self)])

    self.prompt = BttcCmdApp.MAIN_PROMPT
    self.adb = client.Client(host='localhost', port=5037)
    self.dut_init_snippet_uiautomator = True
    self.dut_init_sl4a = False
    self.add_settable(
        cmd2.Settable(
            'dut_init_snippet_uiautomator', bool,
            'Initialize snippet_uiautomator in DUT during selection.', self))
    self.add_settable(
        cmd2.Settable(
            'dut_init_sl4a', bool,
            'Initialize SL4A in DUT during selection.', self))

    self._dut = None
    if serial:
      self._init_dut(serial)

    self.logcat_pattern_history = []
    self.selected_device_history = [
        device.serial for device in self.adb.devices()]

  def _init_dut(self, serial: str):
    self._dut = bttc.get(
        serial,
        init_snippet_uiautomator=self.dut_init_snippet_uiautomator,
        init_sl4a=self.dut_init_sl4a)
    self.prompt = BttcCmdApp.DEVICE_PROMPT_PROMPT.format(serial=serial)

  @dec_require_dut
  def do_device_time(self, args):
    self.poutput(f'{self._dut.gm.device_datetime}\n')

  @dec_require_dut
  def do_load_sl4a(self, args):
    """Loads SL4A service in DUT."""
    device_factory.load_sl4a(self._dut)
    self.dut_init_sl4a = True

  @dec_require_dut
  @cmd2.with_argparser(logcat_filter_parser)
  def do_logcat_filter(self, args):
    pattern_list = []
    while True:
      try:
        pattern_str = self.read_input(
            "Pattern (enter nothing to stop)? ",
            history=self.logcat_pattern_history,
            completion_mode=cmd2.CompletionMode.CUSTOM).strip()
        pattern_str = pattern_str.strip()
        if not pattern_str:
          break

        if pattern_str.startswith('file:'):
          pattern_file_path = pattern_str.split(':')[1]
          if not os.path.isfile(pattern_file_path):
            logging.warning(
                'Pattern file=%s does not exist!', pattern_file_path)
            continue

          load_pattern_count = 0
          with open(pattern_file_path, 'r') as fo:
            for line in fo:
              pattern_str = line.strip()
              if pattern_str:
                pattern_list.append(pattern_str)
                load_pattern_count += 1

          self.poutput(
              f'Total {load_pattern_count} patterns loaded from '
              f'{pattern_file_path}\n')
        else:
          pattern_list.append(pattern_str)

      except EOFError:
        pass

    def hit_pattern(line):
      for pattern in pattern_list:
        if re.search(pattern, line):
          return True

      return False

    for line in self._dut.gm.follow_logcat_within(
        time_sec=args.logcat_wait_sec):
      if hit_pattern(line):
        print(f'{Color.BOLD}{Color.YELLOW}{line}{Color.END}')
      elif not args.logcat_only_match:
        print(f'{Color.GREEN}{line}{Color.END}')

    print('\n\n')

  @cmd2.with_category(MAIN_COMMANDS)
  @cmd2.with_argparser(select_parser)
  def do_select(self, args):
    """Selects DUT."""
    selected_serial = args.serial
    connected_device_serials = {
        device.serial: device for device in self.adb.devices()}
    if not args.serial or args.serial not in connected_device_serials.keys():
      for _ in range(5):
        self.poutput('Connected device(s): ')
        for pair in connected_device_serials.items():
          print(f'\t- {pair[0]}')

        print('')
        try:
          selected_serial = self.read_input(
              "Select? ",
              history=self.selected_device_history,
              completion_mode=cmd2.CompletionMode.CUSTOM,
              choices=list(connected_device_serials.keys()))
        except EOFError:
          pass
        else:
          if selected_serial in connected_device_serials.keys():
            self.selected_device_history.append(selected_serial)
            break
      else:
        self.poutput('Failed to select eligible device!')

    self.poutput(f'You select DUT with serial={selected_serial}\n')
    self._init_dut(selected_serial)

  @cmd2.with_category(MAIN_COMMANDS)
  def do_devices(self, _):
    """Self test command by list connected device(s)."""
    connected_devices = self.adb.devices()
    if not connected_devices:
      self.poutput("No device connected from host!")
      return

    self.poutput("Connected devices from host:")
    for device in connected_devices:
      print(f'\t- {device.serial}')

    print('')

  def free_dut(self):
    print('Releasing DUT resource...')
    if self._dut:
      stopped_services = []
      with contextlib.suppress(mobly.snippet.errors.ProtocolError):
        try:
          for service_name in self._dut.services._service_objects.keys():
            service = self._dut.services._service_objects[service_name]
            if service_name == 'sl4a':
              self.poutput('Stopping SL4A...')
              service._sl4a_client.host_port = None
              service._sl4a_client._client.close()
              service._sl4a_client.close_socket_connection()
              service.stop()
              continue

            self.poutput(f'Stopping {service_name}...')
            service.stop()
            stopped_services.append(service_name)
        except Exception as ex:
          logging.warning('Error: %s', ex)

        for service_name in stopped_services:
          self.poutput(f'Unregistering {service_name}...')
          self._dut.services.unregister(service_name)

        self._dut.adb.forward('--remove-all')


def go(serial: str | None = None):
  """Enters Cli prompt."""
  c = BttcCmdApp(serial)
  c.cmdloop()
  c.free_dut()
  print('=' * 10 + f' {EXIST_MSG} ' + '=' * 10)
  print('')
  os._exit(0)


if __name__ == '__main__':
  args = select_parser.parse_args()
  # Remove command line argument to prevent Cmd2 mis-interpreting them.
  sys.argv = sys.argv[:1]
  go(args.serial)
