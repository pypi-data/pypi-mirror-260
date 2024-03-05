from ctypes import (
    c_uint8,
    c_uint16,
    c_int32,
    c_uint32,
    c_double,
    c_void_p,
    POINTER,
    byref,
    create_string_buffer,
    cast as c_cast,
)
from pathlib import Path
from typing import List, Dict, Optional, Union, overload
from enum import IntEnum, IntFlag, unique
from . import _MPuLib, _check_limits
from .MPStatus import CTS3ErrorCode
from .MPException import CTS3Exception
from .Nfc import TechnologyType, NfcUnit, DataRate, _unit_autoselect
from warnings import warn


@unique
class VdcRange(IntEnum):
    """Vdc voltage range"""

    VDC_RANGE_24V = 0
    VDC_RANGE_12V = 1


def MPC_GetVDCIn(duration: float, voltmeter_range: VdcRange = VdcRange.VDC_RANGE_24V) -> float:
    """
    Performs a maximum voltage measurement on AUX 1 or VDC IN connector

    Args:
        duration: Measurement duration in s
        voltmeter_range: Voltage measurement range

    Returns:
        Maximum voltage in V
    """
    duration_ms = round(duration * 1e3)
    _check_limits(c_uint32, duration_ms, "duration")
    if not isinstance(voltmeter_range, VdcRange):
        raise TypeError("voltmeter_range must be an instance of VdcRange IntEnum")
    vdc = c_int32()
    CTS3Exception._check_error(
        _MPuLib.MPC_GetVDCIn(
            c_uint8(0), byref(vdc), c_uint32(duration_ms), c_uint32(voltmeter_range)
        )
    )
    return vdc.value / 1e3


def MPC_GetVOV(
    integration_time: float, timeout: float, voltmeter_range: VdcRange = VdcRange.VDC_RANGE_24V
) -> float:
    """
    Performs an integrated voltage measurement on AUX 1 or VDC IN connector

    Args:
        integration_time: Integration time in s
        timeout: Measurement timeout in s
        voltmeter_range: Voltage measurement range

    Returns:
        Voltage in V
    """
    integration_time_us = round(integration_time * 1e6)
    _check_limits(c_uint32, integration_time_us, "integration_time")
    timeout_ms = round(timeout * 1e3)
    _check_limits(c_uint32, timeout_ms, "timeout")
    if not isinstance(voltmeter_range, VdcRange):
        raise TypeError("voltmeter_range must be an instance of VdcRange IntEnum")
    vdc = c_int32()
    CTS3Exception._check_error(
        _MPuLib.MPC_GetVOV(
            c_uint8(0),
            byref(vdc),
            c_uint32(integration_time_us),
            c_uint32(timeout_ms),
            c_uint32(voltmeter_range),
        )
    )
    return vdc.value / 1e3


@unique
class MeasureTriggerSetting(IntFlag):
    """Measurement settings"""

    MEAS_TRIG_SETTING_CANCEL = 0
    MEAS_TRIG_SETTING_SINGLE = 1
    MEAS_TRIG_SETTING_DOWNLOAD = 2
    MEAS_TRIG_SETTING_MPLOG = 4


@unique
class MeasureSource(IntEnum):
    """Measurement source"""

    MEAS_SOURCE_RECEPTION = 1
    MEAS_SOURCE_DEMODULATED = 2
    MEAS_SOURCE_VDC_12V = 3
    MEAS_SOURCE_VDC_24V = 4
    MEAS_SOURCE_PHASE = 5
    MEAS_SOURCE_DAQ_CH1_DEMODULATED = 6
    MEAS_SOURCE_DAQ_CH2_DEMODULATED = 7


def MPC_StartRFMeasure2(
    settings: MeasureTriggerSetting,
    source: MeasureSource,
    unit: NfcUnit,
    delay: float,
    duration: float,
    file_name: Union[str, Path] = "",
) -> None:
    """
    Triggers an RF signal acquisition

    Args:
        settings: Trigger settings
        source: Measurement source
        unit: Delay and duration unit
        delay: Trigger delay
        duration: Acquisition duration
        file_name: File name (only if settings contains MEAS_TRIG_SETTING_DOWNLOAD)
    """
    if not isinstance(settings, MeasureTriggerSetting):
        raise TypeError("settings must be an instance of MeasureTriggerSetting IntFlag")
    if not isinstance(source, MeasureSource):
        raise TypeError("source must be an instance of MeasureSource IntEnum")
    if not isinstance(unit, NfcUnit):
        raise TypeError("unit must be an instance of NfcUnit IntEnum")
    # Unit auto-selection
    computed_unit, [computed_delay, computed_duration] = _unit_autoselect(unit, [delay, duration])
    _check_limits(c_int32, computed_delay, "delay")
    _check_limits(c_uint32, computed_duration, "duration")
    if isinstance(file_name, Path):
        if str(file_name) != ".":
            file = str(file_name).encode("ascii")
        else:
            file = "".encode("ascii")
    else:
        file = file_name.encode("ascii")
    CTS3Exception._check_error(
        _MPuLib.MPC_StartRFMeasure2(
            c_uint8(0),
            c_uint32(settings),
            c_uint32(source),
            c_uint32(computed_unit),
            c_int32(computed_delay),
            c_uint32(computed_duration),
            file,
        )
    )


@unique
class RfStatus(IntEnum):
    """RF acquisition trigger status"""

    RFSTATUS_NONE = 0
    RFSTATUS_WAITING_TRIGGER = 1
    RFSTATUS_TRIGGERED = 2
    RFSTATUS_EOC = 3
    RFSTATUS_FILE_AVAILABLE = 4
    RFSTATUS_OVERFLOW = 5
    RFSTATUS_OVERRANGE = 6


def MPC_RFMeasureStatus() -> RfStatus:
    """
    Gets RF signal acquisition status

    Returns:
        Current trigger status
    """
    status = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_RFMeasureStatus(c_uint8(0), byref(status)))
    return RfStatus(status.value)


@unique
class MeasurementConnector(IntEnum):
    """Connector configuration"""

    CONNECTOR_AUTO = 0
    CONNECTOR_TX_RX = 1
    CONNECTOR_RES_FREQ = 2


def MPC_SwitchResonanceFrequencyConnector(connector: MeasurementConnector) -> None:
    """
    Changes the connector currently selected to perform a measurement

    Args:
        connector: Connector to activate
    """
    if not isinstance(connector, MeasurementConnector):
        raise TypeError("connector must be an instance of MeasurementConnector IntEnum")
    CTS3Exception._check_error(
        _MPuLib.MPC_SwitchResonanceFrequencyConnector(c_uint8(0), c_uint8(connector))
    )


@unique
class VoltmeterRange(IntEnum):
    """Voltmeter range"""

    VOLTMETER_RANGE_AUTO = 1
    VOLTMETER_RANGE_500 = 500
    VOLTMETER_RANGE_1000 = 1000
    VOLTMETER_RANGE_2000 = 2000
    VOLTMETER_RANGE_5000 = 5000
    VOLTMETER_RANGE_10000 = 10000


def MPC_SelectVoltmeterRange(voltmeter_range: VoltmeterRange) -> None:
    """
    Selects the voltmeter range on ANALOG IN connector

    Args:
        voltmeter_range: Voltmeter range
    """
    if not isinstance(voltmeter_range, VoltmeterRange):
        raise TypeError("voltmeter_range must be an instance of VoltmeterRange IntEnum")
    CTS3Exception._check_error(
        _MPuLib.MPC_SelectVoltmeterRange(c_uint8(0), c_uint16(voltmeter_range))
    )


def MPC_GetVoltmeterRange() -> VoltmeterRange:
    """
    Gets the voltmeter range on ANALOG IN connector

    Returns:
        Voltmeter range
    """
    voltmeter_range = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_GetVoltmeterRange(c_uint8(0), byref(voltmeter_range)))
    return VoltmeterRange(voltmeter_range.value)


@unique
class MeasurementType(IntEnum):
    """Type of measurement"""

    SCINFC_MEASTYPE_PICC_LMA = 0
    SCINFC_MEASTYPE_PCD_FIELD_STRENGTH = 1
    SCINFC_MEASTYPE_PCD_WAVEFORM = 2
    SCINFC_MEASTYPE_VDC = 3


def GetAnalyzedMeasureVoltmeterToFile(
    measurement_type: MeasurementType,
    card_type: TechnologyType,
    data_rate: DataRate,
    path: Union[str, Path, None] = None,
) -> Dict[str, Union[float, bool, List[float]]]:
    """
    Analyzes analog measurements started with MPC_StartRFMeasure2
    and stores the results in a waveform file

    Args:
        measurement_type: Type of analyze to perform
        card_type: Technology type
        data_rate: Data rate in kb/s
        path: Path to waveform file

    Returns:
        If measurement_type is SCINFC_MEASTYPE_PCD_WAVEFORM, dictionary made of:
        - "t1": T1 in s (float), applicable to Type A and Vicinity only
        - "t2": T2 in s (float), applicable to Type A 106kb/s and Vicinity only
        - "t3": T3 in s (float), applicable to Type A 106kb/s and Vicinity only
        - "t4": T4 in s (float), applicable to Type A 106kb/s and Vicinity only
        - "t5": T5 in s (float), applicable to Type A > 106kb/s only
        - "t5": T5 list in s (list(float)), applicable to Type A 106kb/s only
        - "t6": T6 in s (float), applicable to Type A > 106kb/s only
        - "v1": V1 in V (float)
        - "v1_noise_floor": V1 noise floor in V (float),
            applicable to Type B, FeliCa and Vicinity only
        - "v2": V2 in V (float)
        - "v2_noise_floor": V2 noise floor in V (float), applicable to Type B and FeliCa only
        - "v3": V3 in V (float)
        - "v4": V4 in V (float)
        - "v5": V5 in V (float), applicable to Type A > 106kb/s only
        - "modulation_index": Modulation index in V (float)
        - "modulation_depth": Modulation depth in V (float),
            applicable to Type A 106kb/s, Type B, FeliCa and Vicinity only
        - "monotonic_rising_edge": True if rising edge is monotonic (bool)
        - "rising_time": Rising time in s (float),
            applicable to Type A > 106kb/s, Type B and FeliCa only
        - "overshoot_after_rising_edge": Rising edge overshoot in V (float)
        - "undershoot_after_rising_edge": Rising edge undershoot in V (float),
            applicable to Type A > 106kb/s, Type B and FeliCa only
        - "ringing_level": Ringing in V (float), applicable to Type A 106kb/s only
        - "high_state_noise_floor": High state noise in V (float), applicable to Type A only
        - "monotonic_falling_edge": True if falling edge is monotonic (bool)
        - "falling_time": Falling time in s (float),
            applicable to Type A > 106kb/s, Type B and FeliCa only
        - "overshoot_after_falling_edge": Falling edge overshoot in V (float)
        - "overshoot_delay_after_falling_edge": Delay adter falling edge in s (float),
            applicable to Type A and Vicinity only
        - "undershoot_after_falling_edge": Falling edge undershoot in V (float),
            applicable to Type B and FeliCa only

        If measurement_type is SCINFC_MEASTYPE_PICC_LMA, dictionary made of:
        - "lma": LMA in V (float)

        If measurement_type is SCINFC_MEASTYPE_PCD_FIELD_STRENGTH, dictionary made of:
        - "field_strength": Field strength in Vpp (float)
    """
    if not isinstance(measurement_type, MeasurementType):
        raise TypeError("measurement_type must be an instance of MeasurementType IntEnum")
    if not isinstance(card_type, TechnologyType):
        raise TypeError("card_type must be an instance of TechnologyType IntEnum")
    if not isinstance(data_rate, DataRate):
        raise TypeError("data_rate must be an instance of DataRate IntEnum")
    measurement_count = c_uint32()
    measurements = c_void_p()
    if path:
        if isinstance(path, Path):
            if str(path) != ".":
                file = str(path).encode("ascii")
            else:
                file = "".encode("ascii")
        else:
            file = path.encode("ascii")
        CTS3Exception._check_error(
            _MPuLib.GetAnalyzedMeasureVoltmeterToFile(
                c_uint8(0),
                c_uint32(measurement_type),
                c_uint32(card_type),
                c_uint32(data_rate),
                c_uint32(0),
                file,
                byref(measurement_count),
                byref(measurements),
            )
        )
    else:
        CTS3Exception._check_error(
            _MPuLib.GetAnalyzedMeasureVoltmeterToFile(
                c_uint8(0),
                c_uint32(measurement_type),
                c_uint32(card_type),
                c_uint32(int(data_rate)),
                c_uint32(0),
                None,
                byref(measurement_count),
                byref(measurements),
            )
        )
    if measurement_count.value:
        ptr = c_cast(measurements, POINTER(c_int32 * measurement_count.value))
        values = [i for i in ptr.contents]
        if measurement_type == MeasurementType.SCINFC_MEASTYPE_PCD_WAVEFORM:
            if card_type == TechnologyType.TYPE_A and data_rate == DataRate.DATARATE_106KB:
                t5 = []
                for i in range(16, 16 + values[15]):
                    t5 += [values[i] / 1e9]
                return {
                    "t1": values[0] / 1e9,
                    "t2": values[1] / 1e9,
                    "t3": values[2] / 1e9,
                    "t4": values[3] / 1e9,
                    "v1": values[4] / 1e6,
                    "v2": values[5] / 1e6,
                    "v3": values[6] / 1e6,
                    "v4": values[7] / 1e6,
                    "monotonic_falling_edge": values[8] > 0,
                    "monotonic_rising_edge": values[9] > 0,
                    "overshoot_after_falling_edge": values[10] / 1e6,
                    "overshoot_after_rising_edge": values[11] / 1e6,
                    "overshoot_delay_after_falling_edge": values[12] / 1e9,
                    "ringing_level": values[13] / 1e6,
                    "high_state_noise_floor": values[14] / 1e6,
                    "t5": t5,
                    "modulation_index": values[16 + len(t5)] / 1e6,
                    "modulation_depth": values[17 + len(t5)] / 1e6,
                }
            elif card_type == TechnologyType.TYPE_A and data_rate > DataRate.DATARATE_106KB:
                return {
                    "t1": values[0] / 1e9,
                    "t5": values[1] / 1e9,
                    "t6": values[2] / 1e9,
                    "v1": values[4] / 1e6,
                    "v2": values[5] / 1e6,
                    "v3": values[6] / 1e6,
                    "v4": values[7] / 1e6,
                    "v5": values[7] / 1e6,
                    "modulation_index": values[8] / 1e6,
                    "falling_time": values[9] / 1e9,
                    "rising_time": values[10] / 1e9,
                    "overshoot_after_falling_edge": values[11] / 1e6,
                    "overshoot_after_rising_edge": values[12] / 1e6,
                    "overshoot_delay_after_falling_edge": values[13] / 1e9,
                    "undershoot_after_rising_edge": values[14] / 1e6,
                    "high_state_noise_floor": values[15] / 1e6,
                    "monotonic_falling_edge": values[16] > 0,
                    "monotonic_rising_edge": values[17] > 0,
                }
            elif card_type == TechnologyType.TYPE_B or card_type == TechnologyType.TYPE_FELICA:
                return {
                    "falling_time": values[0] / 1e9,
                    "rising_time": values[1] / 1e9,
                    "monotonic_falling_edge": values[2] > 0,
                    "monotonic_rising_edge": values[3] > 0,
                    "v1": values[4] / 1e6,
                    "v2": values[5] / 1e6,
                    "v3": values[6] / 1e6,
                    "v4": values[7] / 1e6,
                    "modulation_index": values[8] / 1e6,
                    "v1_noise_floor": values[9] / 1e6,
                    "v2_noise_floor": values[10] / 1e6,
                    "overshoot_after_rising_edge": values[11] / 1e6,
                    "overshoot_delay_after_rising_edge": values[12] / 1e9,
                    "overshoot_after_falling_edge": values[13] / 1e6,
                    "undershoot_after_rising_edge": values[14] / 1e6,
                    "undershoot_after_falling_edge": values[15] / 1e6,
                    "modulation_depth": values[16] / 1e6,
                }
            elif card_type == TechnologyType.TYPE_VICINITY:
                return {
                    "t1": values[0] / 1e9,
                    "t2": values[1] / 1e9,
                    "t3": values[2] / 1e9,
                    "t4": values[3] / 1e9,
                    "v1": values[4] / 1e6,
                    "v2": values[5] / 1e6,
                    "v3": values[6] / 1e6,
                    "v4": values[7] / 1e6,
                    "monotonic_falling_edge": values[8] > 0,
                    "monotonic_rising_edge": values[9] > 0,
                    "overshoot_after_falling_edge": values[10] / 1e6,
                    "overshoot_after_rising_edge": values[11] / 1e6,
                    "overshoot_delay_after_falling_edge": values[12] / 1e9,
                    "v1_noise_floor": values[14] / 1e6,
                    "modulation_index": values[16] / 1e6,
                    "modulation_depth": values[17] / 1e6,
                }
            else:
                return {}
        elif measurement_type == MeasurementType.SCINFC_MEASTYPE_PICC_LMA:
            return {"lma": values[0] / 1e6}
        elif measurement_type == MeasurementType.SCINFC_MEASTYPE_PCD_FIELD_STRENGTH:
            return {"field_strength": values[0] / 1e6}
        else:
            return {}
    else:
        return {}


def MPC_StoreCoeffAlignStandard(measure_type: MeasurementType, coefficient: float) -> None:
    """
    Stores a measurement compensation factor into dual antenna EEPROM

    Args:
        measurement_type: Type of measurement to compensate
        coefficient: Compensation factor to be applied to the measurement
    """
    if not isinstance(measure_type, MeasurementType):
        raise TypeError("measure_type must be an instance of MeasurementType IntEnum")
    CTS3Exception._check_error(
        _MPuLib.MPC_StoreCoeffAlignStandard(
            c_uint8(0), c_uint32(measure_type), c_double(coefficient)
        )
    )


# region Reader frequency measurement


@unique
class FrequencyResolution(IntEnum):
    """Carrier frequency resolution"""

    RESOLUTION_1000HZ = 1
    RESOLUTION_100HZ = 2
    RESOLUTION_10HZ = 3
    RESOLUTION_1HZ = 4
    RESOLUTION_AUTO = 5


@overload
def MPC_GetRFFrequency() -> int:
    ...


@overload
def MPC_GetRFFrequency(resolution: FrequencyResolution, timeout: float) -> int:
    ...


def MPC_GetRFFrequency(resolution=None, timeout=None):  # type: ignore[no-untyped-def]
    """
    Performs a carrier frequency measurement

    Args:
        resolution: Not used
        timeout: Not used

    Returns:
        Measured frequency in Hz
    """
    if resolution is not None or timeout is not None:
        warn("deprecated 'resolution' or 'timeout' parameter", FutureWarning, 2)
    freq = c_uint32()
    CTS3Exception._check_error(
        _MPuLib.MPC_GetRFFrequency(c_uint8(0), c_uint32(0), c_uint32(0), byref(freq))
    )
    return freq.value


# endregion

# region Data rate measurement


def MPC_GetDatarate(card_type: TechnologyType) -> int:
    """
    Measures the last received frame data rate

    Args:
        card_type: Technology type

    Returns:
        Measured data rate in b/s
    """
    if not isinstance(card_type, TechnologyType):
        raise TypeError("card_type must be an instance of TechnologyType IntEnum")
    datarate = c_uint32()
    CTS3Exception._check_error(
        _MPuLib.MPC_GetDatarate(c_uint8(0), c_uint8(card_type), byref(datarate))
    )
    return datarate.value


# endregion

# region Impedance measurement


def MPC_ImpedanceSelfCompensation(
    connector: MeasurementConnector, channel: int, label: Optional[str]
) -> None:
    """
    Performs cable impedance compensation

    Args:
        connector: Connector used to perform the cable impedance compensation
        channel: DAQ SMA input channel used to perform the cable impedance compensation
        label: Compensation identifier
    """
    if not isinstance(connector, MeasurementConnector):
        raise TypeError("connector must be an instance of MeasurementConnector IntEnum")
    _check_limits(c_uint8, channel, "channel")
    if label is None:
        CTS3Exception._check_error(
            _MPuLib.MPC_ImpedanceSelfCompensation(c_uint8(connector), c_uint8(channel), None)
        )
    else:
        CTS3Exception._check_error(
            _MPuLib.MPC_ImpedanceSelfCompensation(
                c_uint8(connector), c_uint8(channel), label.encode("ascii")
            )
        )


def MPC_ImpedanceLoadCable(label: Optional[str]) -> None:
    """
    Loads cable compensation information

    Args:
        label: Compensation identifier
    """
    if label is None:
        CTS3Exception._check_error(_MPuLib.MPC_ImpedanceLoadCable(c_uint8(0), None))
    else:
        CTS3Exception._check_error(
            _MPuLib.MPC_ImpedanceLoadCable(c_uint8(0), label.encode("ascii"))
        )


def MPC_ImpedanceListCables() -> List[str]:
    """
    Lists available cable compensations information

    Returns:
        Compensation identifiers list
    """
    cables_list = create_string_buffer(0xFFFF)
    CTS3Exception._check_error(_MPuLib.MPC_ImpedanceListCables(c_uint8(0), cables_list))
    list_string = cables_list.value.decode("ascii").strip()
    return list_string.split(";") if len(list_string) else []


def MPC_ImpedanceDeleteCable(label: str) -> None:
    """
    Removes cable compensation information from database

    Args:
        label: Compensation identifier
    """
    CTS3Exception._check_error(_MPuLib.MPC_ImpedanceDeleteCable(c_uint8(0), label.encode("ascii")))


def MPC_ImpedanceAdapterCompensation(
    label: str,
    meas_load: complex,
    meas_short: complex,
    meas_open: complex,
    ref_load: complex,
    ref_short: complex = 0,
    ref_open: complex = complex("inf"),
) -> None:
    """
    Performs adapter impedance compensation

    Args:
        label: Adapter identifier
        meas_load: Measured load condition complex impedance in Ω
        meas_short: Measured short condition complex impedance in Ω
        meas_open: Measured open condition complex impedance in Ω
        ref_load: Reference load condition complex impedance in Ω
        ref_short: Reference short condition complex impedance in Ω
        ref_open: Reference open condition complex impedance in Ω
    """
    CTS3Exception._check_error(
        _MPuLib.MPC_ImpedanceAdapterCompensation(
            label.encode("ascii"),
            c_double(meas_load.real),
            c_double(meas_load.imag),
            c_double(meas_short.real),
            c_double(meas_short.imag),
            c_double(meas_open.real),
            c_double(meas_open.imag),
            c_double(ref_load.real),
            c_double(ref_load.imag),
            c_double(ref_short.real),
            c_double(ref_short.imag),
            c_double(ref_open.real),
            c_double(ref_open.imag),
        )
    )


def MPC_ImpedanceLoadAdapter(label: Optional[str]) -> None:
    """
    Loads adapter compensation information

    Args:
        label: Compensation identifier
    """
    if label is None:
        CTS3Exception._check_error(_MPuLib.MPC_ImpedanceLoadAdapter(None))
    else:
        CTS3Exception._check_error(_MPuLib.MPC_ImpedanceLoadAdapter(label.encode("ascii")))


def MPC_ImpedanceListAdapters() -> List[str]:
    """
    Lists available adapter compensations information

    Returns:
        Compensation identifiers list
    """
    adapters_list = create_string_buffer(0xFFFF)
    CTS3Exception._check_error(_MPuLib.MPC_ImpedanceListAdapters(adapters_list))
    list_string = adapters_list.value.decode("ascii").strip()
    return list_string.split(";") if len(list_string) else []


def MPC_ImpedanceDeleteAdapter(label: str) -> None:
    """
    Removes adapter compensation information from database

    Args:
        label: Compensation identifier
    """
    CTS3Exception._check_error(_MPuLib.MPC_ImpedanceDeleteAdapter(label.encode("ascii")))


@unique
class ImpedanceConfiguration(IntEnum):
    """Impedance measurement configuration"""

    WITH_NO_CABLE = 0
    WITH_CABLE = 1
    WITH_CABLE_AND_HEAD = 2


@overload
def MPC_MeasureImpedance(config: bool = True, average: int = 1) -> Dict[str, Union[float, complex]]:
    ...


@overload
def MPC_MeasureImpedance(
    config: ImpedanceConfiguration = ImpedanceConfiguration.WITH_CABLE, average: int = 1
) -> Dict[str, Union[float, complex]]:
    ...


def MPC_MeasureImpedance(  # type: ignore[no-untyped-def]
    config=ImpedanceConfiguration.WITH_CABLE, average=1
) -> Dict[str, Union[float, complex]]:
    """
    Performs an impedance measurement

    Args:
        config: Configuration of impedance to measure
        average: Measurements number to average

    Returns:
        Dictionary made of:
        - "impedance": Measured complex impedance in Ω (complex)
        - "resistance": Measured resistance in Ω (float)
        - "capacitance": Measured capacitance in F (float)
        - "inductance": Measured inductance in H (float)
        - "vcc": Estimated voltage on the measured impedance in Vpp (float)
        - "icc": Estimated current on the measured impedance in App (float)
    """
    if isinstance(config, bool):
        warn("deprecated 'config' parameter type", FutureWarning, 2)
        configuration = c_uint8(1) if config else c_uint8(0)
    elif isinstance(config, ImpedanceConfiguration):
        configuration = c_uint8(config)
    else:
        raise TypeError("config must be an instance of ImpedanceConfiguration IntEnum")
    _check_limits(c_uint32, average, "average")
    real_part = c_double()
    imaginary_part = c_double()
    resistance = c_double()
    capacitance = c_double()
    inductance = c_double()
    vcc = c_double()
    icc = c_double()
    CTS3Exception._check_error(
        _MPuLib.MPC_MeasureImpedance(
            c_uint8(0),
            configuration,
            c_uint32(average),
            byref(real_part),
            byref(imaginary_part),
            byref(resistance),
            byref(capacitance),
            byref(inductance),
            byref(vcc),
            byref(icc),
        )
    )
    return {
        "impedance": complex(real_part.value, imaginary_part.value),
        "resistance": resistance.value,
        "capacitance": capacitance.value,
        "inductance": inductance.value,
        "vcc": vcc.value,
        "icc": icc.value,
    }


# endregion

# region Resonance frequency measurement


@unique
class ResonanceMethod(IntEnum):
    """Resonance frequency measurement method"""

    RESONANCE_ISO = 0
    RESONANCE_NFC = 2


def MPC_ResonanceFrequency(
    method: ResonanceMethod,
    power_dbm: float,
    step: float,
    freq_min: float,
    freq_max: float,
    average: int = 1,
) -> Dict[str, Union[int, float]]:
    """
    Performs a resonance frequency measurement

    Args:
        method: Resonance frequency measurement method
        power_dbm: Field power in dBm
        step: Frequency step in Hz
        freq_min: Lower frequency bound in Hz
        freq_max: Upper frequency bound in Hz
        average: Measurements number for each point

    Returns:
        Dictionary made of:
        - "resonance_frequency" Measured resonance frequency in Hz (int)
        - "q_factor": Measured quality factor (float)
    """
    if not isinstance(method, ResonanceMethod):
        raise TypeError("method must be an instance of ResonanceMethod IntEnum")
    power_dbm_int = round(power_dbm)
    _check_limits(c_int32, power_dbm_int, "power_dbm")
    step_Hz = round(step)
    _check_limits(c_uint32, step_Hz, "step")
    freq_min_Hz = round(freq_min)
    _check_limits(c_uint32, freq_min_Hz, "freq_min")
    freq_max_Hz = round(freq_max)
    _check_limits(c_uint32, freq_max_Hz, "freq_max")
    _check_limits(c_uint32, average, "average")
    freq = c_uint32()
    q = c_uint32()
    CTS3Exception._check_error(
        _MPuLib.MPC_ResonanceFrequencyVS(
            c_uint8(0),
            c_uint8(method),
            c_int32(power_dbm_int),
            c_uint32(step_Hz),
            c_uint32(average),
            c_uint32(freq_min_Hz),
            c_uint32(freq_max_Hz),
            byref(freq),
            byref(q),
        )
    )
    return {"resonance_frequency": freq.value, "q_factor": float(q.value) / 1e1}


@unique
class ResFreqMeasureType(IntEnum):
    """Resonance frequency measurement type"""

    RF_REAL_PART = 1
    RF_IMAGINARY_PART = 2


def MPC_GetMeasureResFreq(
    measure_type: ResFreqMeasureType = ResFreqMeasureType.RF_REAL_PART,
) -> List[float]:
    """
    Reads resonance frequency measured values

    Args:
        measure_type: Measure to be returned

    Returns:
        Measured values
    """
    if not isinstance(measure_type, ResFreqMeasureType):
        raise TypeError("measure_type must be an instance of ResFreqMeasureType IntEnum")
    measurement_count = c_uint32()
    measurements = c_void_p()
    CTS3Exception._check_error(
        _MPuLib.MPC_GetMeasureResFreq(
            c_uint8(0), byref(measurement_count), byref(measurements), c_int32(measure_type)
        )
    )
    if measurement_count.value:
        ptr = c_cast(measurements, POINTER(c_double * measurement_count.value))
        return [i for i in ptr.contents]
    else:
        return []


# endregion

# region S11 measurement


def MPC_S11StartMeasurement(
    frequency_min: float, frequency_max: float, step: float, power_dbm: float, average: int = 1
) -> None:
    """
    Starts as S11 measurement

    Args:
        frequency_min: Lower frequency bound in Hz
        frequency_max: Upper frequency bound in Hz
        step: Frequency step in Hz
        power_dbm: Field power in dBm
        average: Measurements number for each point
    """
    freq_min_Hz = round(frequency_min)
    _check_limits(c_uint32, freq_min_Hz, "frequency_min")
    freq_max_Hz = round(frequency_max)
    _check_limits(c_uint32, freq_max_Hz, "frequency_max")
    step_Hz = round(step)
    _check_limits(c_uint32, step_Hz, "step")
    power_dbm_int = round(power_dbm)
    _check_limits(c_int32, power_dbm_int, "power_dbm")
    _check_limits(c_uint32, average, "average")
    CTS3Exception._check_error(
        _MPuLib.MPC_S11StartMeasurement(
            c_uint8(0),
            c_uint32(freq_min_Hz),
            c_uint32(freq_max_Hz),
            c_uint32(step_Hz),
            c_int32(power_dbm_int),
            c_uint32(average),
        )
    )


@unique
class S11MeasureType(IntEnum):
    """S11 measurement type"""

    S11_RETURN_LOSS = 0
    S11_REAL_PART = 1
    S11_IMAGINARY_PART = 2


def MPC_GetMeasureS11(measure_type: S11MeasureType = S11MeasureType.S11_RETURN_LOSS) -> List[float]:
    """
    Reads S11 measured values

    Args:
        measure_type: Measure to be returned

    Returns:
        Measured values
    """
    if not isinstance(measure_type, S11MeasureType):
        raise TypeError("measure_type must be an instance of S11MeasureType IntEnum")
    measurement_count = c_uint32()
    measurements = c_void_p()
    CTS3Exception._check_error(
        _MPuLib.MPC_GetMeasureS11(
            c_uint8(0), byref(measurement_count), byref(measurements), c_int32(measure_type)
        )
    )
    if measurement_count.value:
        ptr = c_cast(measurements, POINTER(c_double * measurement_count.value))
        return [i for i in ptr.contents]
    else:
        return []


def MPC_GetS11(frequency: float = 0.0) -> Dict[str, Union[float, complex]]:
    """
    Gets the S11 value at a specific frequency

    Args:
        frequency: Measurement frequency in Hz

    Returns:
        Dictionary made of:
        - "dbm_at_min": Minimum Return Loss in dB (float)
        - "frequency_at_min": Frequency giving the minimum return loss in Hz (int)
        - "impedance_at_min": Measured complex impedance in Ω at minimum return loss (complex)
        - "dbm_at_frequency": Return loss in dB at requested frequency, if not 0 (float)
        - "impedance_at_frequency": Measured complex impedance in Ω at requested frequency,
          if not 0 (complex)
    """
    freq_Hz = round(frequency)
    _check_limits(c_uint32, freq_Hz, "frequency")
    dbm_at_min = c_double()
    frequency_at_min = c_uint32()
    real_at_min = c_double()
    imaginary_at_min = c_double()
    module_at_min = c_double()
    dbm_at_frequency = c_double()
    real_at_frequency = c_double()
    imaginary_at_frequency = c_double()
    module_at_frequency = c_double()
    ret = _MPuLib.MPC_GetS11(
        c_uint8(0),
        c_uint32(freq_Hz),
        byref(dbm_at_min),
        byref(frequency_at_min),
        byref(real_at_min),
        byref(imaginary_at_min),
        byref(module_at_min),
        byref(dbm_at_frequency),
        byref(real_at_frequency),
        byref(imaginary_at_frequency),
        byref(module_at_frequency),
    )
    if ret == CTS3ErrorCode.ERR_RESONANCE_FREQUENCY_MEASUREMENT.value and frequency > 0.0:
        return {
            "dbm_at_frequency": dbm_at_frequency.value,
            "impedance_at_frequency": complex(
                real_at_frequency.value, imaginary_at_frequency.value
            ),
        }
    CTS3Exception._check_error(ret)
    if frequency > 0.0:
        return {
            "dbm_at_min": dbm_at_min.value,
            "frequency_at_min": frequency_at_min.value,
            "impedance_at_min": complex(real_at_min.value, imaginary_at_min.value),
            "dbm_at_frequency": dbm_at_frequency.value,
            "impedance_at_frequency": complex(
                real_at_frequency.value, imaginary_at_frequency.value
            ),
        }
    else:
        return {
            "dbm_at_min": dbm_at_min.value,
            "frequency_at_min": frequency_at_min.value,
            "impedance_at_min": complex(real_at_min.value, imaginary_at_min.value),
        }


# endregion

# region RF field measurement


@unique
class CalibrationCoil(IntEnum):
    """Calibration coil type"""

    RFFIELD_ASSEMBLY_1 = 1
    RFFIELD_ASSEMBLY_2 = 2


def MPC_GetRFField(coil: CalibrationCoil = CalibrationCoil.RFFIELD_ASSEMBLY_1) -> float:
    """
    Measures the field strength on ANALOG IN connector

    Args:
        coil: Calibration coil to measure the field from

    Returns:
        Field strength in Arms/m
    """
    if not isinstance(coil, CalibrationCoil):
        raise TypeError("coil must be an instance of CalibrationCoil IntEnum")
    voltage = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_GetRFField(c_uint8(0), c_uint32(coil), byref(voltage)))
    return voltage.value / 1e3


# endregion
