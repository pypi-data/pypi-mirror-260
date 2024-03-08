from WITecSDK.Parameters import COMParameters

class DetectorOutput:

    def __init__(self, aCOMParameters: COMParameters):
        parampath = "MultiComm|MicroscopeControl|DetectorOutput|"
        self._selectedCOM = aCOMParameters.GetStringParameter(parampath + "Selected")
        self._setAllOutCOM = aCOMParameters.GetTriggerParameter(parampath + "AllOut")
        self._setNoOutputCOM = aCOMParameters.GetTriggerParameter(parampath + "NoOutput")
        self._setCCD1COM = aCOMParameters.GetTriggerParameter(parampath + "CCD1")
        self._setCCD2COM = aCOMParameters.GetTriggerParameter(parampath + "CCD2")
        self._setCCD3COM = aCOMParameters.GetTriggerParameter(parampath + "CCD3")
        self._setSinglePhotonCounting1COM = aCOMParameters.GetTriggerParameter(parampath + "SinglePhotonCounting1")
        self._setSinglePhotonCounting2COM = aCOMParameters.GetTriggerParameter(parampath + "SinglePhotonCounting2")
        self._setSinglePhotonCounting3COM = aCOMParameters.GetTriggerParameter(parampath + "SinglePhotonCounting3")

    def SetAllOut(self):
        self._setAllOutCOM.ExecuteTrigger()

    def SetNoOutput(self):
        self._setNoOutputCOM.ExecuteTrigger()

    def SetCCD1(self):
        self._setCCD1COM.ExecuteTrigger()
    
    def SetCCD2(self):
        self._setCCD1COM.ExecuteTrigger()

    def SetCCD3(self):
        self._setCCD1COM.ExecuteTrigger()
    
    def SetSinglePhotonCounting1(self):
        self._setSinglePhotonCounting1COM.ExecuteTrigger()
    
    def SetSinglePhotonCounting2(self):
        self._setSinglePhotonCounting2COM.ExecuteTrigger()

    def SetSinglePhotonCounting3(self):
        self._setSinglePhotonCounting3COM.ExecuteTrigger()

    @property
    def SelectedOutput(self) -> str:
        return self._selectedCOM.GetValue()