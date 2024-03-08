"""Contains the Base class of the COMClient"""

from abc import ABC, abstractmethod
from _ctypes import COMError

class COMClientBase(ABC):
    """Handles the communication with the COM server (WITec Control)"""
    
    def __init__(self, aServerName: str):
        """Accepts a server name of a remote PC in case WITec Control
        doesn't run on the same computer (refer to help)"""

        self.ServerName = aServerName
        self._wcCoreInterface = None
        self._accessInterface = None

        try:
            self._createCoreInterface()
        except Exception as e:
            raise COMClientException(self.ServerName, "Could not instantiate an Object of the Core Interface class.") from  e
        
        if self._wcCoreInterface is None:
            raise COMClientException(self.ServerName, "Create Object of IBUCSCore returned null")
        
        print("WITec COM Client connected")
        self._createAccessInterface()

    def GetSubSystemsList(self, aName: str, aSubSystemsDepth: int):
        """Implements GetSubSystemsList of IBUCSCore interface"""

        return self._wcCoreInterface.GetSubSystemsList(aName, aSubSystemsDepth)
    
    def GetSubSystemDefaultInterface(self, aParameter: str):
        """Implements GetSubSystemDefaultInterface of IBUCSCore interface"""
        return self._wcCoreInterface.GetSubSystemDefaultInterface(aParameter)
    
    @property
    def ReadAccess(self) -> bool:
        """Checks for read access over IBUCSAccess"""

        return self._accessInterface.HasReadAccess()
    
    @property
    def WriteAccess(self) -> bool:
        """Checks/Requests write access over IBUCSAccess"""

        return self._accessInterface.HasWriteAccess()
    
    @WriteAccess.setter
    def WriteAccess(self, value: bool):
        if self.WriteAccess != value:
            self._accessInterface.RequestWriteAccess(value)
            if self.WriteAccess:
                print("WITec COM Client write access granted")
            elif not value:
                print("WITec COM Client write access released")
    
    @abstractmethod
    def ReleaseSubSystemInterface(self):
        pass
    
    @abstractmethod
    def _createCoreInterface(self):
        """Creates an instance of IBUCSCore interface"""

        pass

    @abstractmethod
    def _createAccessInterface(self):
        """Creates an instance of IBUCSAccess interface"""

        pass
    
    def __del__(self):
        if self._wcCoreInterface is not None:
            try:
                self.WriteAccess = False
            except COMError as e:
                if e.hresult == -2147023174: #RPC server unavailable
                    print("WITec Control is not available")
                else:
                    print(e.details)
                    raise COMClientException(self.ServerName, "Not possible to release WriteAccess") from e
            
            self.ReleaseSubSystemInterface(self._accessInterface)
            self.ReleaseSubSystemInterface(self._wcCoreInterface)
            print("WITec COM Client disconnected")

class COMClientException(Exception):
    def __init__(self, serverName: str, message: str):
        super().__init__(serverName + ": " + message)