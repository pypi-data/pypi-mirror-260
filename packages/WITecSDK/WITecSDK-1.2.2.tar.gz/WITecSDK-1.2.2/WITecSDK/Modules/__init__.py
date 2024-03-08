"""Modules containing classes for different measurement modes or
hardware control."""

from WITecSDK.Modules.ActiveSequencer import ActiveSequencer, ActiveSequencer60, ActiveSequencer62
from WITecSDK.Modules.ApertureFieldStop import ApertureFieldStop
from WITecSDK.Modules.ApplicationControl import ApplicationControl
from WITecSDK.Modules.AutoFocus import AutoFocus61, AutoFocus
from WITecSDK.Modules.BeamPath import BeamPath, BeamPath51, CalibrationCoupler, CalibrationCoupler62
from WITecSDK.Modules.ConfigurationLoader import ConfigurationLoader
from WITecSDK.Modules.DetectorOutput import DetectorOutput
from WITecSDK.Modules.FastTimeSeries import FastTimeSeries
from WITecSDK.Modules.Heating import Heating
from WITecSDK.Modules.Illumination import TopIllumination, BottomIllumination
from WITecSDK.Modules.LargeAreaScan import LargeAreaScan,LargeAreaScan62
from WITecSDK.Modules.LaserManager import LaserManager61, LaserManager52, LaserManager, LaserInformation
from WITecSDK.Modules.LaserPowerSeries import LaserPowerSeries
from WITecSDK.Modules.LineScan import LineScan, LineScan62
from WITecSDK.Modules.ManualTopography import ManualTopography
from WITecSDK.Modules.ObjectiveTurret import ObjectiveTurret
from WITecSDK.Modules.ParameterNameGetter import ParameterNameGetter
from WITecSDK.Modules.Polarization import Polarization
from WITecSDK.Modules.ProjectCreatorSaver import ProjectCreatorSaver
from WITecSDK.Modules.SampleName import SampleName
from WITecSDK.Modules.SamplePositioner import SamplePositioner, SamplePositioner51
from WITecSDK.Modules.SilentSpectrum import SilentSpectrum
from WITecSDK.Modules.SingleSpectrum import SingleSpectrum
from WITecSDK.Modules.SlowTimeSeriesManual import SlowTimeSeriesManual
from WITecSDK.Modules.SlowTimeSeriesTimed import SlowTimeSeriesTimed
from WITecSDK.Modules.SpectralAutofocus import SpectralAutofocus53, SpectralAutofocus51, SpectralAutofocus
from WITecSDK.Modules.Spectrograph import Spectrograph
from WITecSDK.Modules.StateManager import StateManager
from WITecSDK.Modules.TrueSurface import TrueSurface62, TrueSurface
from WITecSDK.Modules.VideoControl import VideoControl61, VideoControl51, VideoControl50
from WITecSDK.Modules.WITecControlVersionTester import WITecControlVersionTester
from WITecSDK.Modules.XYAxes import XYAxes
from WITecSDK.Modules.ZAxis import ZAxis, ZStepper
from WITecSDK.Modules.HelperStructs import (AutofocusSettings, DataChannelDescription, SamplePositionerPosition, XYZPosition, LargeAreaSettings)

class WITecModules:
    """Base class of the main class for creating the module classes."""
    
    _activeSequencer = None
    _applicationControl = None
    _apertureFieldStop = None
    _beamPath = None
    _autofocus = None
    _detectorOutput = None
    _xyAxes = None
    _samplePositioner = None
    _zAxis = None
    _zStepper = None
    _manualTopography = None
    _trueSurface = None
    _topIllumination = None
    _bottomIllumination = None
    _objectiveTurret = None
    _sampleName = None
    _slowTimeSeriesManual = None
    _slowTimeSeriesTimed = None
    _singleSpectrum = None
    _silentSpectrum = None
    _fastTimeSeries = None
    _lineScan = None
    _largeAreaScan = None
    _spectrograph1 = None
    _spectrograph2 = None
    _spectrograph3 = None
    _stateManager = None
    _videoControl = None
    _laserManager = None
    _laserPowerSeries = None
    _projectCreatorSaver = None
    _heating = None
    _polarization = None
    _spectralAutofocus = None
    _configurationLoader = None
    _parameterNameGetter = None
    _versionTester = None
    
    def __init__(self):
        self._versionTester = WITecControlVersionTester(self.comParameters)

    def CreateActiveSequencer(self) -> ActiveSequencer|ActiveSequencer60:
        """Creates a class instance to query and stop the active sequencer."""

        if self._activeSequencer is None:
            if self._versionTester.IsVersionGreater62:
                self._activeSequencer = ActiveSequencer62(self.comParameters)
            elif self._versionTester.IsVersionGreater60:
                self._activeSequencer = ActiveSequencer60(self.comParameters)
            else:
                self._activeSequencer = ActiveSequencer(self.comParameters)
        return self._activeSequencer
    
    def CreateApplicationControl(self) -> ApplicationControl:
        """Creates a class instance of Application Control"""

        if self._applicationControl is None:
            self._applicationControl = ApplicationControl(self.comParameters)    
        return self._applicationControl
    
    def CreateApertureFieldStop(self) -> ApertureFieldStop:
        """Creates a class instance to control Aperture and field stop.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._apertureFieldStop is None:
            self._apertureFieldStop = ApertureFieldStop(self.comParameters)
        return self._apertureFieldStop
        
    def CreateBeamPath(self) -> BeamPath|BeamPath51:
        """Creates a class instance to control the beampath."""

        if self._beamPath is None:
            if self._versionTester.IsVersionGreater51:
                self._beamPath = BeamPath51(self.comParameters)
            else:
                self._beamPath = BeamPath(self.comParameters)
            if self._versionTester.IsVersionGreater62:
                self._beamPath.CalibrationLamp = CalibrationCoupler62(self.comParameters)
            else:
                self._beamPath.CalibrationLamp = CalibrationCoupler(self.comParameters)
        return self._beamPath
    
    def CreateAutoFocus(self) -> AutoFocus61|AutoFocus:
        """Creates a class instance to control the video autofocus.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._autofocus is None:
            if self._versionTester.IsVersionGreater61:
                self._autofocus = AutoFocus61(self.comParameters)
            else:
                self._autofocus = AutoFocus(self.comParameters)
        return self._autofocus
    
    # Only for internal use only, use ConfigurationLoader instead to change the output
    def CreateDetectorOutput(self) -> DetectorOutput:
        """Creates a class instance to control the detector output.
        Throws an ParameterNotAvailableException if hardware is not available.
        Only for internal use."""

        if self._detectorOutput is None:
            self._detectorOutput = DetectorOutput(self.comParameters)
        return self._detectorOutput
    
    def CreateXYAxes(self) -> XYAxes|SamplePositioner:
        """Creates a class instance to control the motorized xy stage.
        Throws an ParameterNotAvailableException if hardware is not available.
        For versions before 6.1 the SamplePositioner class is returned
        instead of the XYAxes class."""

        if self._versionTester.IsVersionGreater61:
            if self._xyAxes is None:
                self._xyAxes = XYAxes(self.comParameters)
            return self._xyAxes
        else:
            return self.CreateSamplePositioner()
    
    # Depricated, will be removed in future versions, use XYAxes
    def CreateSamplePositioner(self) -> SamplePositioner|SamplePositioner51:
        """Creates a class instance to control the motorized xy stage.
        Throws an ParameterNotAvailableException if hardware is not available.
        Depricated, will be removed in future versions, use CreateXYAxes"""

        if self._samplePositioner is None:
            if self._versionTester.IsVersionGreater51:
                self._samplePositioner = SamplePositioner51(self.comParameters)
            else:
                self._samplePositioner = SamplePositioner(self.comParameters)
        return self._samplePositioner

    def CreateZAxis(self) -> ZAxis|ZStepper:
        """Creates a class instance to control the motorized z stage.
        Throws an ParameterNotAvailableException if hardware is not available.
        For versions before 6.1 the ZStepper class is returned
        instead of the ZAxis class."""

        if self._versionTester.IsVersionGreater61:
            if self._zAxis is None:
                self._zAxis = ZAxis(self.comParameters)
            return self._zAxis
        else:
            return self.CreateZStepper()

    # Depricated, will be removed in future versions, use ZAxis
    def CreateZStepper(self) -> ZStepper:
        """Creates a class instance to control the motorized z stage.
        Throws an ParameterNotAvailableException if hardware is not available.
        Depricated, will be removed in future versions, use CreateZAxis"""

        if self._zStepper is None:
            self._zStepper = ZStepper(self.comParameters)
        return self._zStepper
    
    def CreateManualTopography(self) -> ManualTopography:
        """Creates a class instance to control the manual topography correction.
        Throws an ParameterNotAvailableException if function is not available.
        Only useful in combination XYAxes and ZAxis class starting in 6.1."""

        if self._versionTester.IsVersionGreater61:
            if self._manualTopography is None:
                self._manualTopography = ManualTopography(self.comParameters, self.CreateXYAxes(), self.CreateZAxis(),
                                                           self.CreateSpectralAutofocus(), self.CreateActiveSequencer())
            return self._manualTopography
    
    def CreateTrueSurface(self) -> TrueSurface|TrueSurface62:
        """Creates a class instance to control TrueSurface (Mk3).
        Throws an ParameterNotAvailableException if hardware is not available.
        Only available for version >= 6.1"""

        if self._trueSurface is None:
            if self._versionTester.IsVersionGreater62:
                self._trueSurface = TrueSurface62(self.comParameters)
            elif self._versionTester.IsVersionGreater60:
                self._trueSurface = TrueSurface(self.comParameters)
        return self._trueSurface
    
    def CreateTopIllumination(self) -> TopIllumination:
        """Creates a class instance to control the top illumination.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._topIllumination is None:
            self._topIllumination = TopIllumination(self.comParameters)
        return self._topIllumination
    
    def CreateBottomIllumination(self) -> BottomIllumination:
        """Creates a class instance to control the top illumination.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._bottomIllumination is None:
            self._bottomIllumination = BottomIllumination(self.comParameters)
        return self._bottomIllumination

    def CreateObjectiveTurret(self) -> ObjectiveTurret|None:
        """Creates a class instance to control the objective turret.
        Throws an ParameterNotAvailableException if hardware is not available.
        Only available for version >= 6.1"""

        if self._objectiveTurret is None:
            if self._versionTester.IsVersionGreater61:
                self._objectiveTurret = ObjectiveTurret(self.comParameters)
        return self._objectiveTurret

    def CreateSampleName(self) -> SampleName:
        """Creates a class instance for setting the sample name.
        Only available for version >= 5.2"""

        if self._sampleName is None:
            if self._versionTester.IsVersionGreater52:
                self._sampleName = SampleName(self.comParameters)
        return self._sampleName

    def CreateSlowTimeSeriesManual(self) -> SlowTimeSeriesManual:
        """Creates a class instance for software-triggered slow series."""

        if self._slowTimeSeriesManual is None:
            self._slowTimeSeriesManual = SlowTimeSeriesManual(self.comParameters, self.CreateActiveSequencer())
        return self._slowTimeSeriesManual

    def CreateSlowTimeSeriesTimed(self) -> SlowTimeSeriesTimed:
        """Creates a class instance for a slow time series."""

        if self._slowTimeSeriesTimed is None:
            self._slowTimeSeriesTimed = SlowTimeSeriesTimed(self.comParameters)
        return self._slowTimeSeriesTimed

    def CreateSingleSpectrum(self) -> SingleSpectrum:
        """Creates a class instance for a single spectrum."""

        if self._singleSpectrum is None:
            self._singleSpectrum = SingleSpectrum(self.comParameters)
        return self._singleSpectrum

    # Unsupported class, can be removed or changed in future versions
    def CreateSilentSpectrum(self) -> SilentSpectrum:
        """Creates a class instance for a silent spectrum which returns the spectrum
        as ASCII.
        Only available for version >= 5.2
        Unsupported, can be removed or changed in future versions"""

        if self._silentSpectrum is None:
            if self._versionTester.IsVersionGreater52:
                self._silentSpectrum = SilentSpectrum(self.comParameters, self.CreateBeamPath())
        return self._silentSpectrum

    def CreateFastTimeSeries(self) -> FastTimeSeries:
        """Creates a class instance for a fast time series."""

        if self._fastTimeSeries is None:
            self._fastTimeSeries = FastTimeSeries(self.comParameters)
        return self._fastTimeSeries

    def CreateLineScan(self) -> LineScan|LineScan62:
        """Creates a class instance for a line time series."""

        if self._lineScan is None:
            if self._versionTester.IsVersionGreater62:
                self._lineScan = LineScan62(self.comParameters)
            else:
                self._lineScan = LineScan(self.comParameters)
        return self._lineScan

    def CreateLargeAreaScan(self) -> LargeAreaScan|LargeAreaScan62:
        """Creates a class instance for a large area series."""

        if self._largeAreaScan is None:
            if self._versionTester.IsVersionGreater62:
                self._largeAreaScan = LargeAreaScan62(self.comParameters)
            else:
                self._largeAreaScan = LargeAreaScan(self.comParameters)
        return self._largeAreaScan
    
    def CreateLaserManager(self) -> LaserManager61|LaserManager52|LaserManager:
        """Creates a class instance to control the lasers."""

        if self._laserManager is None:
            if self._versionTester.IsVersionGreater61:
                self._laserManager = LaserManager61(self.comParameters)
            elif self._versionTester.IsVersionGreater52:
                self._laserManager = LaserManager52(self.comParameters)
            else:
                self._laserManager = LaserManager(self.comParameters)
        return self._laserManager
    
    def CreateLaserPowerSeries(self) -> LaserPowerSeries:
        """Creates a class instance for a Laser Power series.
        Only available for version >= 5.1"""

        if self._laserPowerSeries is None:
            if self._versionTester.IsVersionGreater51:
                self._laserPowerSeries = LaserPowerSeries(self.comParameters)
        return self._laserPowerSeries

    def CreateSpectrograph1(self) -> Spectrograph:
        """Creates a class instance to control spectrograph 1.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._spectrograph1 is None:
            self._spectrograph1 = Spectrograph(self.comParameters, 1)
        return self._spectrograph1

    def CreateSpectrograph2(self) -> Spectrograph:
        """Creates a class instance to control spectrograph 2.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._spectrograph2 is None:
            self._spectrograph2 = Spectrograph(self.comParameters, 2)
        return self._spectrograph2

    def CreateSpectrograph3(self) -> Spectrograph:
        """Creates a class instance to control spectrograph 3.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._spectrograph3 is None:
            self._spectrograph3 = Spectrograph(self.comParameters, 3)
        return self._spectrograph3

    def CreateStateManager(self) -> StateManager|None:
        """Creates a class instance for setting the state manager.
        Only available for version >= 6.2"""

        if self._stateManager is None:
            if self._versionTester.IsVersionGreater62:
                self._stateManager = StateManager(self.comParameters)
        return self._stateManager
    
    def CreateVideoControl(self) -> VideoControl61|VideoControl51|VideoControl50:
        """Creates a class instance to control the video image."""

        if self._videoControl is None:
            if self._versionTester.IsVersionGreater61:
                self._videoControl = VideoControl61(self.comParameters)
            elif self._versionTester.IsVersionGreater51:
                self._videoControl = VideoControl51(self.comParameters)
            else:
                self._videoControl = VideoControl50(self.comParameters)
        return self._videoControl

    def CreateProjectCreatorSaver(self) -> ProjectCreatorSaver:
        """Creates a class instance to save and load projects."""
        
        if self._projectCreatorSaver is None:
            self._projectCreatorSaver = ProjectCreatorSaver(self.comParameters)
        return self._projectCreatorSaver 

    def CreateHeating(self) -> Heating:
        """Creates a class instance to control the heating stage.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._heating is None:
            self._heating = Heating(self.comParameters)
        return self._heating

    def CreatePolarization(self) -> Polarization|None:
        """Creates a class instance to control polarizer and analyzer.
        Throws an ParameterNotAvailableException if hardware is not available.
        Only available for version >= 5.1"""

        if self._polarization is None:
            if self._versionTester.IsVersionGreater51:
                self._polarization = Polarization(self.comParameters)
        return self._polarization

    def CreateSpectralAutofocus(self) -> SpectralAutofocus53|SpectralAutofocus51|SpectralAutofocus:
        """Creates a class instance to control the spectral autofocus.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._spectralAutofocus is None:
            if self._versionTester.IsVersionGreater53:
                self._spectralAutofocus = SpectralAutofocus53(self.comParameters)
            elif self._versionTester.IsVersionGreater51:
                self._spectralAutofocus = SpectralAutofocus51(self.comParameters)
            else:
                self._spectralAutofocus = SpectralAutofocus(self.comParameters)
        return self._spectralAutofocus

    def CreateConfigurationLoader(self) -> ConfigurationLoader:
        """Creates a class instance to change the configuration."""

        if self._configurationLoader is None:
            self._configurationLoader = ConfigurationLoader(self.comParameters)
        return self._configurationLoader

    def CreateParameterNameGetter(self) -> ParameterNameGetter:
        """Creates a class instance to read available parameters."""

        if self._parameterNameGetter is None:
            self._parameterNameGetter = ParameterNameGetter(self.comParameters)
        return self._parameterNameGetter

    def CreateWITecControlVersionTester(self) -> WITecControlVersionTester:
        """Creates a class instance to check the WITec Control version."""
        
        return self._versionTester
    