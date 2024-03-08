"""Contains the COMClient version for pywin32 (fallback)"""

from WITecSDK.COMClientBase import COMClientBase
from pythoncom import CLSCTX_REMOTE_SERVER, VT_ARRAY, VT_R4, VT_BSTR
from win32com.client import DispatchEx, CastTo, VARIANT

CLSID = "{C45E77CE-3D66-489A-B5E2-159F443BD1AA}"
IBUCSCore = 'IBUCSCore'
IBUCSAccess = 'IBUCSAccess'
IBUCSSubSystemsList = 'IBUCSSubSystemsList'
IBUCSStatusContainer = 'IBUCSStatusContainer'
IBUCSTrigger = 'IBUCSTrigger'
IBUCSBool = 'IBUCSBool'
IBUCSEnum = 'IBUCSEnum'
IBUCSFillStatus = 'IBUCSFillStatus'
IBUCSFloat = 'IBUCSFloat'
IBUCSFloatMinMaxValues = 'IBUCSFloatMinMaxValues'
IBUCSInt = 'IBUCSInt'
IBUCSIntMinMaxValues = 'IBUCSIntMinMaxValues'
IBUCSString = 'IBUCSString'
IBUCSSubSystemInfo = 'IBUCSSubSystemInfo'
IBUCSSingleValue = 'IBUCSSingleValue'
IBUCSSingleValueHasLimits = 'IBUCSSingleValueHasLimits'

class COMClient(COMClientBase):
    """COMClient version for pywin32"""
    
    def __init__(self, aServerName: str):
        super().__init__(aServerName)

    def _createCoreInterface(self):
        wcCoreIDispatch = DispatchEx(CLSID, machine=self.ServerName, clsctx=CLSCTX_REMOTE_SERVER)
        self._wcCoreInterface = self.CastToInterface(wcCoreIDispatch, IBUCSCore)

    def _createAccessInterface(self):
        self._accessInterface = self.CastToInterface(self._wcCoreInterface, IBUCSAccess)
    
    @classmethod
    def Reorder(cls, aValues: tuple) -> tuple:
        """Reorders returned tuples"""

        return (aValues[1:] + aValues[0:1])
    
    @classmethod
    def ConvertToBSTRArray(cls, datalist: list) -> VARIANT:
        return VARIANT(VT_ARRAY | VT_BSTR, datalist)

    @classmethod
    def ConvertToFloatArray(cls, datalist: list) -> VARIANT:
        return VARIANT(VT_ARRAY | VT_R4, datalist)

    @classmethod
    def CastToInterface(cls, aObj, aInterface: str):
        return CastTo(aObj, aInterface)

    @classmethod
    def ReleaseSubSystemInterface(cls, aInterface):
        pass
