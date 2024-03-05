from . import _MPuLib, GetErrorMessageFromCode, GetMifareErrorMessageFromCode
from .MPStatus import CTS3ErrorCode, MifareErrorCode
from ctypes import c_int32, c_uint8, byref
from typing import Union
from warnings import warn


class CTS3Exception(Exception):
    """
    CTS3 exception

    Attributes:
        ErrorCode: Error code
    """

    def __init__(self, err: Union[str, CTS3ErrorCode]):
        """
        Inits CTS3Exception

        Args:
            err: Error code or error message
        """
        if isinstance(err, CTS3ErrorCode):
            Exception.__init__(self, GetErrorMessageFromCode(err.value))
            self.ErrorCode = err
        else:
            Exception.__init__(self, err)

    @staticmethod
    def _check_error(status: int) -> None:
        """
        Checks CTS3 status

        Args:
            status: CTS3 status
        """
        try:
            ret = CTS3ErrorCode(status)
        except ValueError:
            raise CTS3Exception(f"Unknown error code 0x{status:04x}")
        if (
            ret == CTS3ErrorCode.ERR_TIME_FDT_MAX
            or ret == CTS3ErrorCode.ERR_TIME_FDT_MIN
            or ret == CTS3ErrorCode.ERR_TIME_TR1_MAX
            or ret == CTS3ErrorCode.ERR_TIME_TR1_MIN
            or ret == CTS3ErrorCode.ERR_PHASE_DRIFT
            or ret == CTS3ErrorCode.ERR_ADJUST_THRESHOLD_RF_FIELD
            or ret == CTS3ErrorCode.RET_INCOMPATIBLE_BOOT_VERSION
        ):
            warn(GetErrorMessageFromCode(status), UserWarning, 3)
        elif ret == CTS3ErrorCode.ERR_NO_VALID_ATR_REQ_RECEIVED:
            warn(GetErrorMessageFromCode(status), Warning, 3)
        elif ret != CTS3ErrorCode.RET_OK:
            raise CTS3Exception(ret)


class CTS3MifareException(Exception):
    """
    CTS3 MIFARE exception

    Attributes:
        ErrorCode: Error code
    """

    def __init__(self, err_code: MifareErrorCode):
        """
        Inits CTS3MifareException

        Args:
            err_code: Error code
        """
        Exception.__init__(self, GetMifareErrorMessageFromCode(err_code.value))
        self.ErrorCode = err_code

    @staticmethod
    def _check_error(status: int) -> None:
        """
        Checks MIFARE status

        Args:
            status: MIFARE status
        """
        if status == 0:
            error = c_int32()
            _MPuLib.CLP_GetLastErrorNumber.restype = c_int32
            ret = _MPuLib.CLP_GetLastErrorNumber(c_uint8(0), byref(error))
            if ret == 0:
                if _MPuLib.GetLastComError() == 0:
                    raise CTS3Exception(CTS3ErrorCode.RET_RESOURCE_NOT_OPEN)
                else:
                    raise CTS3Exception(CTS3ErrorCode.DLLCOMERROR)
            raise CTS3MifareException(MifareErrorCode(error.value))
        if status > 1:
            raise CTS3Exception(CTS3ErrorCode(status))
