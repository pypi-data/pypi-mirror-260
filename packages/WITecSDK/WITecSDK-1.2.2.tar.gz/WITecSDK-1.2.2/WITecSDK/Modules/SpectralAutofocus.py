from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules.HelperStructs import AutofocusSettings
        
class SpectralAutofocus:
    
    _parampath = "UserParameters|SequencerAutoFocus|"

    def __init__(self, aComParameters: COMParameters):
        self._startAutoFocusCOM = aComParameters.GetTriggerParameter(self._parampath + "Start")
        self._maximumRangeCOM = aComParameters.GetFloatParameter(self._parampath + "MaximumRange")
        self._minimalIntegrationTimeCOM = aComParameters.GetFloatParameter(self._parampath + "MinimalIntegrationTime")
        self._postFocusMoveCOM = aComParameters.GetFloatParameter(self._parampath + "PostAutoFocusMovement")

    def PerformAutofocus(self, autofocusSettings: AutofocusSettings = None):
        if autofocusSettings is not None:
            self.Initialize(autofocusSettings)
            
        self.Start()
    
    def Initialize(self, settings: AutofocusSettings):
        self.MaxRange = settings.MaximumRange
        self.MinIntegrationTime = settings.MinimalIntegrationTime

    @property
    def MinIntegrationTime(self) -> float:
        return self._minimalIntegrationTimeCOM.GetValue()
    
    @MinIntegrationTime.setter
    def MinIntegrationTime(self, integrationTime: float):
        self._minimalIntegrationTimeCOM.SetValue(integrationTime)

    @property
    def MaxRange(self) -> float:
        return self._maximumRangeCOM.GetValue()
    
    @MaxRange.setter
    def MaxRange(self, range: float):
        self._maximumRangeCOM.SetValue(range)

    @property
    def PostFocusMove(self) -> float:
        return self._postFocusMoveCOM.GetValue()
    
    @PostFocusMove.setter
    def PostFocusMove(self, range: float):
        self._postFocusMoveCOM.SetValue(range)
    
    def Start(self):
        self._startAutoFocusCOM.ExecuteTrigger()


class SpectralAutofocus51(SpectralAutofocus):

    def __init__(self, aComParameters: COMParameters):
        super().__init__(aComParameters)
        self._centerCOM = aComParameters.GetFloatParameter(self._parampath + "Center")
        self._stepSizeMultiplierCOM = aComParameters.GetFloatParameter(self._parampath + "StepSizeMultiplier")
        self._autoFocusModeCOM = aComParameters.GetEnumParameter(self._parampath + "AutoFocusMode")

    def PerformAutofocus(self, autofocusSettings: AutofocusSettings = None):
        if autofocusSettings is not None:
            self.InitializeFindRaman(autofocusSettings)
            
        self.Start()
        
    def InitializeFindRaman(self, settings: AutofocusSettings):
        super().Initialize(settings)
        self.Center = settings.Center
        self.SetModeFindRaman()
        self.StepsizeMultiplier = settings.StepSizeMultiplier

    def InitializeFindPeak(self, settings: AutofocusSettings):
        super().Initialize(settings)
        self.Center = settings.Center
        self.SetModeFindPeak()

    def SetModeFindPeak(self):
        self._autoFocusModeCOM.SetValue(0)

    def SetModeFindRaman(self):
        self._autoFocusModeCOM.SetValue(1)

    @property
    def Center(self) -> float:
        return self._centerCOM.GetValue()
    
    @Center.setter
    def Center(self, center: float):
        self._centerCOM.SetValue(center)

    @property
    def StepsizeMultiplier(self) -> float:
        return self._stepSizeMultiplierCOM.GetValue()
    
    @StepsizeMultiplier.setter
    def StepsizeMultiplier(self, stepsize: float):
        self._stepSizeMultiplierCOM.SetValue(stepsize)


class SpectralAutofocus53(SpectralAutofocus51):

    def __init__(self, aComParameters: COMParameters):
        super().__init__(aComParameters)
        self._spectralMaskCOM = aComParameters.GetStringParameter("UserParameters|SpectralDataAnalysis|Mask")

    def setSpectralMask(self, mask: str = "100;3600"):
        self._spectralMaskCOM.SetValue(mask)