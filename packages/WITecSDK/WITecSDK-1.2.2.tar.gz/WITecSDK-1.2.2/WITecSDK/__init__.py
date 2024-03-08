"""This package simplifies to access the COM interface of WITec Control.

It is downwards compatible with WITec Control versions older than the
current release. Ready-to-use classes are offered for most common
measurement modes. The package contains the COM client to connect to
the COM interface and two sub-packages.

The package will use the COMClient based on the comtypes package by
default. If this package is not installed it will try to use the
COMClient passed on pywin32 (less tested).

Typical usage example:
    
    from WITecSDK import WITecSDKClass
    WITec = WITecSDKClass()
"""

# Use "from WITecSDK.COMClientComTyp" for comtypes package or "from WITecSDK.COMClientW32Com" for Win32Com
try:
    from WITecSDK.COMClientComTyp import (COMClient, IBUCSSubSystemsList, IBUCSStatusContainer, IBUCSTrigger, IBUCSBool, IBUCSEnum,
                                        IBUCSFillStatus, IBUCSSingleValueHasLimits, IBUCSFloat, IBUCSFloatMinMaxValues, IBUCSInt,
                                        IBUCSIntMinMaxValues, IBUCSString, IBUCSSubSystemInfo, IBUCSSingleValue)
except ImportError:
    print("Package comtypes not found. Try to use pywin32 instead.")
    from WITecSDK.COMClientW32Com import (COMClient, IBUCSSubSystemsList, IBUCSStatusContainer, IBUCSTrigger, IBUCSBool, IBUCSEnum,
                                        IBUCSFillStatus, IBUCSSingleValueHasLimits, IBUCSFloat, IBUCSFloatMinMaxValues, IBUCSInt,
                                        IBUCSIntMinMaxValues, IBUCSString, IBUCSSubSystemInfo, IBUCSSingleValue)
except Exception as e:
    raise e

from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules import (WITecModules, LaserInformation, AutofocusSettings, DataChannelDescription,
                              SamplePositionerPosition, XYZPosition, LargeAreaSettings)
from socket import gethostname

class WITecSDKClass(WITecModules):
    """Main class that connects to WITec Control and could create
    classes for the measurement modes."""

    def __init__(self, aServerName: str = gethostname()):
        """Initializes an instance of the class and allows to connect to WITec
        Control running on a remote computer. By default the localhost is used."""

        self._client = COMClient(aServerName)
        self.comParameters = COMParameters(self._client)
        super().__init__()
    
    def RequestWriteAccess(self) -> bool:
        """Requests write access from WITec Control and returns success as boolean.
        Precondition:
            WITec Control must allow Remote Write Access
            (Control-Form, Parameter: COM Automation -> Allow Remote Access)"""

        self._client.WriteAccess = True
        return self._client.WriteAccess

    def ReleaseWriteAccess(self):
        """Returns write access to WITec Control."""

        self._client.WriteAccess = False

    @property
    def HasReadAccess(self) -> bool:
        """Checks for read access."""

        return self._client.ReadAccess
    
    @property
    def HasWriteAccess(self) -> bool:
        """Checks for write access."""

        return self._client.WriteAccess
