"""Contains the COMClient version for comtypes"""

from WITecSDK.COMClientBase import COMClientBase
from comtypes.client import GetModule, CreateObject
from comtypes.automation import BSTR, VARIANT, VT_ARRAY, _SysAllocStringLen, _VariantClear, _midlSAFEARRAY
from ctypes import c_float, memmove, byref, cast, sizeof, _SimpleCData

bucstlb_id = '{E84FEF4C-DD2F-4B8D-9C2F-D016FEBB01F4}'
try:
    GetModule((bucstlb_id, 1, 0))
except Exception as e:
    raise Exception("BasicUniversalCOMServerLib not found.") from e

from comtypes.gen.BasicUniversalCOMServerLib import (CBUCSCore, IBUCSCore, IBUCSAccess, IBUCSSubSystemsList, IBUCSStatusContainer, IBUCSTrigger,
                                                     IBUCSSingleValueHasLimits, IBUCSBool, IBUCSEnum, IBUCSFillStatus, IBUCSFloat, IBUCSFloatMinMaxValues,
                                                     IBUCSInt, IBUCSIntMinMaxValues, IBUCSString, IBUCSSubSystemInfo, IBUCSSingleValue)

def ConvertToVARIANT(value: list, atype: type(_SimpleCData)) -> VARIANT:
    """Creates SAFEARRAY of a certain type in comtypes"""

    varobj = VARIANT()
    _VariantClear(varobj)
    obj = _midlSAFEARRAY(atype).create(value)
    memmove(byref(varobj._), byref(obj), sizeof(obj))
    varobj.vt = VT_ARRAY | obj._vartype_
    return varobj

class COMClient(COMClientBase):
    """COMClient version for comtypes"""
    
    def __init__(self, aServerName: str):
        super().__init__(aServerName)

    def _createCoreInterface(self):
        self._wcCoreInterface = CreateObject(CBUCSCore, interface = IBUCSCore, machine = self.ServerName)
    
    def _createAccessInterface(self):
        self._accessInterface = self.CastToInterface(self._wcCoreInterface, IBUCSAccess)

    @classmethod
    def Reorder(cls, aValues: tuple) -> tuple:
        """Reorders returned tuples"""

        return aValues
    
    @classmethod
    def ConvertToBSTRArray(cls, datalist: list[str]) -> VARIANT:
        datalist = [cast(_SysAllocStringLen(item, len(item)), BSTR) for item in datalist]
        return ConvertToVARIANT(datalist, BSTR)

    @classmethod
    def ConvertToFloatArray(cls, datalist: list[float]) -> VARIANT:
        return ConvertToVARIANT(datalist, c_float)
    
    @classmethod
    def CastToInterface(cls, aObj, aInterface):
        return aObj.QueryInterface(aInterface)
    
    @classmethod
    def ReleaseSubSystemInterface(cls, aInterface):
        if aInterface is not None:
            aInterface.Release()
