from WITecSDK.Parameters import COMParameters

class LaserInformation:
    def __init__(self, aPower: float, aWavelength: float, aHasShutter: bool, aHasFilter: bool):
        self.Power: float = aPower
        self.Wavelength: float = aWavelength
        self.HasShutter: bool = aHasShutter
        self.HasFilter: bool = aHasFilter


class LaserManager:

    _parampath = "MultiComm|MicroscopeControl|Laser|"

    def __init__(self, aCOMParameters: COMParameters):
        self._numberOfLasersCOM = aCOMParameters.GetIntParameter(self._parampath + "NumberOfLasers")
        self._selectNoLaserCOM = aCOMParameters.GetTriggerParameter(self._parampath + "SelectNoLaser")
        self._laserPowerCOM = aCOMParameters.GetFloatParameter(self._parampath + "Selected|Power")
        self._waveLengthCOM = aCOMParameters.GetFloatParameter(self._parampath + "Selected|Wavelength")
        self._filterCOM = aCOMParameters.GetBoolParameter(self._parampath + "Selected|Filter")
        self._shutterCOM = aCOMParameters.GetBoolParameter(self._parampath + "Selected|Shutter")
        
        self.availableLasers: list[Laser] = []
        for i in range(self.NumberOfLasers):
            self.availableLasers.append(Laser(aCOMParameters, i))

    def SelectLaser(self, LaserNo: int):
        if self.NumberOfLasers == 0:
            raise NoLaserAvailableException("No lasers available.")
        if LaserNo < 0 or LaserNo >= self.NumberOfLasers:
            raise LaserNotExistingException(f"Available lasers: {self.NumberOfLasers}, indexing 0 to {self.NumberOfLasers - 1}.")
        self.availableLasers[LaserNo].Select()

    def SelectNoLaser(self):
        self._selectNoLaserCOM.ExecuteTrigger()

    @property
    def SelectedLaserInfo(self) -> LaserInformation:
        laserPower = self.SelectedLaserPower
        waveLength = self._waveLengthCOM.GetValue()
        return LaserInformation(laserPower, waveLength, None, None)

    @property
    def SelectedLaserPower(self) -> float:
        return self._laserPowerCOM.GetValue()

    @SelectedLaserPower.setter
    def SelectedLaserPower(self, laserPower: float):
        self._laserPowerCOM.SetValue(laserPower)

    @property
    def SelectedLaserShutterOpen(self) -> bool:
        return self._shutterCOM.GetValue()

    @SelectedLaserShutterOpen.setter
    def SelectedLaserShutterOpen(self, state: bool):
        self._shutterCOM.SetValue(state)

    @property
    def SelectedLaserFilterIn(self) -> bool:
        return self._filterCOM.GetValue()

    @SelectedLaserFilterIn.setter
    def SelectedLaserFilterIn(self, state: bool):
        self._filterCOM.SetValue(state)
    
    @property
    def NumberOfLasers(self) -> int:
        return self._numberOfLasersCOM.GetValue()


class Laser:
    def __init__(self, aCOMParameters, laserNo: int):
        self._laserSelectCOM = aCOMParameters.GetTriggerParameter("MultiComm|MicroscopeControl|Laser|SelectLaser" + str(laserNo));

    def Select(self):
        self._laserSelectCOM.ExecuteTrigger()


class LaserManager52(LaserManager):
    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._hasShutterCOM = aCOMParameters.GetBoolParameter(self._parampath + "Selected|HasShutter")
        self._hasFilterCOM = aCOMParameters.GetBoolParameter(self._parampath + "Selected|HasFilter")

    @property
    def SelectedLaserInfo(self) -> LaserInformation:
        laserinfo = super().SelectedLaserInfo
        laserinfo.HasShutter = self._hasShutterCOM.GetValue()
        laserinfo.HasFilter = self._hasFilterCOM.GetValue()
        return laserinfo


class LaserManager61(LaserManager52):
    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._correctionFactorCOM = aCOMParameters.GetFloatParameter(self._parampath + "Selected|PowerCorrectionFactor")
    
    @property
    def SelectedLaserPower(self):
        correctionFactor = self._correctionFactorCOM.GetValue()
        return correctionFactor * self.SelectedLaserPowerUncorrected
    
    @SelectedLaserPower.setter
    def SelectedLaserPower(self, laserPower: float):
        correctionFactor = self._correctionFactorCOM.GetValue()
        self._laserPowerCOM.SetValue(laserPower / correctionFactor)

    @property
    def SelectedLaserPowerUncorrected(self):
        return super().SelectedLaserPower
    
    @SelectedLaserPowerUncorrected.setter
    def SelectedLaserPowerUncorrected(self, laserPower: float):
        super().SelectedLaserPower = laserPower


class NoLaserAvailableException(IndexError):
    pass

class LaserNotExistingException(IndexError):
    pass