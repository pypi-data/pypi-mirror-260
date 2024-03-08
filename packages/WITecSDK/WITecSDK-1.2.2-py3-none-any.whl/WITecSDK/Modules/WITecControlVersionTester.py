from WITecSDK.Parameters import COMParameters

class WITecControlVersionTester:

    def __init__(self, aCOMParameters: COMParameters):
        self._programVersionCOM = aCOMParameters.GetStringParameter("Status|Software|Application|ProgramVersion")
        self._version = self.GetVersion()

    @property
    def IsVersionGreater51(self) -> bool:
        return (self.Version >= 5.1)
    
    @property
    def IsVersionGreater52(self) -> bool:
        return (self.Version >= 5.2)

    @property
    def IsVersionGreater53(self) -> bool:
        return (self.Version >= 5.3)
    
    @property
    def IsVersionGreater60(self) -> bool:
        return (self.Version >= 6.0)

    @property
    def IsVersionGreater61(self) -> bool:
        return (self.Version >= 6.1)

    @property
    def IsVersionGreater62(self) -> bool:
        return (self.Version >= 6.2)
    
    @property
    def Version(self) -> float:
        return self._version

    def GetVersion(self) -> float:
        witecControlVersion = self._programVersionCOM.GetValue()
        versionString = self._getVersionNumber(witecControlVersion)
        versionNumber = float(versionString)
        return versionNumber

    def _getVersionNumber(self, witecControlVersion):
        strsp1 = witecControlVersion.split(',')
        strsp2 = strsp1[1].strip().split(' ')
        
        return strsp2[0]