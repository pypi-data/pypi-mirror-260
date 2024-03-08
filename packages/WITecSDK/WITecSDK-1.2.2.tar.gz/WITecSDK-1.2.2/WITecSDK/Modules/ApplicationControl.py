from WITecSDK.Parameters import COMParameters

class ApplicationControl:

    def __init__(self, aCOMParameters: COMParameters):
        self._updateHardwareCOM = aCOMParameters.GetTriggerParameter("ApplicationControl|UpdateHardware")
        self._exitControlCOM = aCOMParameters.GetTriggerParameter("ApplicationControl|ExitApplication")
        self._physicalMemoryCOM = aCOMParameters.GetIntParameter("Status|Software|Application|MemoryStatus|PhysicalMemory")
        self._pageFileCOM = aCOMParameters.GetIntParameter("Status|Software|Application|MemoryStatus|PageFile")
        self._addressSpaceCOM = aCOMParameters.GetIntParameter("Status|Software|Application|MemoryStatus|AddressSpace")

    def UpdateHardware(self):
        self._updateHardwareCOM.ExecuteTrigger()

    def Exit(self):
        self._exitControlCOM.ExecuteTrigger()

    @property
    def PhysicalMemory(self) -> str:
        return self._physicalMemoryCOM.GetValue()

    @property
    def PageFile(self) -> str:
        return self._pageFileCOM.GetValue()
    
    @property
    def AddressSpace(self) -> str:
        return self._addressSpaceCOM.GetValue()