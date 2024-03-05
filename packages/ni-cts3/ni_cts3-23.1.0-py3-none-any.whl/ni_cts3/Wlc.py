from enum import IntEnum, unique
from ctypes import c_uint8, c_uint32, c_double, byref
from . import _MPuLib
from .MPException import CTS3Exception

# region Poller


def WLC_P_PowerTransfer(duration: float, field: float) -> None:
    """
    Performs a Wireless Power Transfer phase

    Args:
        duration: WPT duration in s
        field: Charging RF field strength in Vpp
    """
    CTS3Exception._check_error(
        _MPuLib.WLC_P_PowerTransfer(c_double(duration), c_double(field), c_uint32(0))
    )


@unique
class WlcPTiming(IntEnum):
    """Poller Timings"""

    WLC_P_TIMING_HOLD_OFF = 0
    WLC_P_TIMING_SETTLE = 1


def WLC_P_SetTiming(type: WlcPTiming, value: float) -> None:
    """
    Sets a WLC Poller timing

    Args:
        type: Poller timing type
        value: Value of the timing to change in s
    """
    if not isinstance(type, WlcPTiming):
        raise TypeError("type must be an instance of WlcPTiming IntEnum")
    CTS3Exception._check_error(_MPuLib.WLC_P_SetTiming(c_uint8(type), c_double(value)))


def WLC_P_GetTiming(type: WlcPTiming) -> float:
    """
    Gets a WLC Poller timing

    Args:
        type: Poller timing type

    Returns:
        Timing value in s
    """
    if not isinstance(type, WlcPTiming):
        raise TypeError("type must be an instance of WlcPTiming IntEnum")
    value = c_double()
    CTS3Exception._check_error(_MPuLib.WLC_P_GetTiming(c_uint8(type), byref(value)))
    return value.value


# endregion

# region Listener


def WLC_L_StopRequest() -> None:
    """Generates a Stop Request"""
    CTS3Exception._check_error(_MPuLib.WLC_L_StopRequest())


def WLC_L_ImpPulse(duration: float) -> None:
    """
    Generates an Impedance Pulse

    Args:
        duration: Pulse duration in s
    """
    CTS3Exception._check_error(_MPuLib.WLC_L_ImpPulse(c_double(duration)))


def WLC_L_ImpChange(duration: float) -> None:
    """
    Generates an Impedance Change

    Args:
        duration: Impedance change duration in s
    """
    CTS3Exception._check_error(_MPuLib.WLC_L_ImpChange(c_double(duration)))


def WLC_L_SetVic(v_nic: float, v_ic: float) -> None:
    """
    Selects Voltage Impedance Change

    Args:
        v_nic: Voltage during No Impedance Change in V
        v_ic: Voltage during Impedance Change in V
    """
    CTS3Exception._check_error(_MPuLib.WLC_L_SetVic(c_double(v_nic), c_double(v_ic)))


@unique
class WlcLTiming(IntEnum):
    """Listener Timings"""

    WLC_L_TIMING_TRANSITION = 0
    WLC_L_TIMING_STOP_IMP_CHANGE = 1


def WLC_L_SetTiming(type: WlcLTiming, value: float) -> None:
    """
    Sets a WLC Listener timing

    Args:
        type: Listener timing type
        value: Value of the timing to change in s
    """
    if not isinstance(type, WlcLTiming):
        raise TypeError("type must be an instance of WlcLTiming IntEnum")
    CTS3Exception._check_error(_MPuLib.WLC_L_SetTiming(c_uint8(type), c_double(value)))


def WLC_L_GetTiming(type: WlcLTiming) -> float:
    """
    Gets a WLC Listener timing

    Args:
        type: Listener timing type

    Returns:
        Timing value in s
    """
    if not isinstance(type, WlcLTiming):
        raise TypeError("type must be an instance of WlcLTiming IntEnum")
    value = c_double()
    CTS3Exception._check_error(_MPuLib.WLC_L_GetTiming(c_uint8(type), byref(value)))
    return value.value


# endregion
