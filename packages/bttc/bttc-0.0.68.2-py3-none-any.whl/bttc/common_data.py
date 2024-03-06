"""Module to hold common dataclass and enum."""
import dataclasses
import enum


@dataclasses.dataclass
class CrashInfo:
  total_num_crash: int = -1
  collected_crash_times: list[str] = dataclasses.field(
      default_factory=list)


class StrEnum(str, enum.Enum):
  """Accepts only string values."""


class BTLogLevel(StrEnum):
  """BT log level."""
  DEBUG = 'LOG_DEBUG'
  VERBOSE = 'LOG_VERBOSE'
