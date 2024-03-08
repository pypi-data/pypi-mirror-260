from WITecSDK.Parameters import COMParameters, ParameterNotAvailableException
from WITecSDK.Parameters.COMParameterBase import NoWriteAccessException

class BeamPath:
    
    _parampath = "MultiComm|MicroscopeControl|BeamPath|"
    
    def __init__(self, aCOMParameters: COMParameters):
        self._stateCOM = aCOMParameters.GetStringParameter(self._parampath + "State")
        self._setStateAllOffCOM = aCOMParameters.GetTriggerParameter(self._parampath + "SetStateAllOff")
        self._setStateVideoCOM = aCOMParameters.GetTriggerParameter(self._parampath + "SetStateVideo")
        self._setStateRamanCOM = aCOMParameters.GetTriggerParameter(self._parampath + "SetStateRaman")
        self._stateOnIdleCOM = aCOMParameters.GetStringParameter("UserParameters|MicroscopeStateOnIdle")
        self.CalibrationLamp = None
        self.AdjustmentSampleCoupler = AutomatedCoupler(aCOMParameters, "MultiComm|MicroscopeControl|AdjustmentSampleCoupler|State")
        self._preventIdleState = False
        self._initialIdleState = self._stateOnIdleCOM.GetValue()

    @property
    def State(self) -> str:
        return self._stateCOM.GetValue()

    def SetAllOff(self):
        self._setStateAllOffCOM.ExecuteTrigger()

    def SetVideo(self):
        self._setStateVideoCOM.ExecuteTrigger()

    def SetRaman(self):
        self._setStateRamanCOM.ExecuteTrigger()

    @property
    def PreventIdleState(self) -> bool:
        return self._preventIdleState

    @PreventIdleState.setter
    def PreventIdleState(self, value: bool):
        if value:
            self._stateOnIdleCOM.SetValue("")
        else:
            self._stateOnIdleCOM.SetValue(self._initialIdleState)
        self._preventIdleState = value

    def __del__(self):
        try:
            if self.PreventIdleState:
                self.PreventIdleState = False
        except NoWriteAccessException:
            print("Not possible to restore initial Idle State. Reload configuration to fix.")


class BeamPath51(BeamPath):
    
    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._setStateWhiteLightMeasurementCOM = aCOMParameters.GetTriggerParameter(self._parampath + "SetStateWhiteLightMeasurement")


    def SetWhiteLightMeasurement(self):
        self._setStateWhiteLightMeasurementCOM.ExecuteTrigger()


class BaseDevice:
    def __new__(cls, aCreateParam: callable, aParamPath: str):
        try:
            initCOM = aCreateParam(aParamPath)
        except ParameterNotAvailableException:
            return None
        except Exception as e:
            raise e
        else:
            devInstance = super().__new__(cls)
            devInstance._initCOM = initCOM
            return devInstance


class AutomatedCoupler(BaseDevice):
    def __new__(cls, aCOMParameters: COMParameters, aCouplerPath: str):
        couplerInstance = super().__new__(cls, aCOMParameters.GetBoolParameter, aCouplerPath)
        if couplerInstance is not None:
            couplerInstance._CouplerCOM = couplerInstance._initCOM
        return couplerInstance

    @property
    def Coupled(self) -> bool:
        return self._CouplerCOM.GetValue()
    
    @Coupled.setter
    def Coupled(self, state: bool):
        self._CouplerCOM.SetValue(state)


class CalibrationCoupler(BaseDevice):
    def __new__(cls, aCOMParameters: COMParameters):
        couplerInstance = super().__new__(cls, aCOMParameters.GetEnumParameter, "MultiComm|MicroscopeControl|CalibrationLamp|State")
        if couplerInstance is not None:
            couplerInstance._StateCOM = couplerInstance._initCOM
        return couplerInstance

    @property
    def State(self) -> int:
        return self._StateCOM.GetValue()

    def GetStates(self) -> dict:
        return self._StateCOM.GetAvailableValues()


class CalibrationCoupler62(CalibrationCoupler):
    def __init__(self, aCOMParameters: COMParameters):
        self._isPermanentlyOnCOM = aCOMParameters.GetStringParameter("MultiComm|MicroscopeControl|CalibrationLamp|IsPermanentlyOn")

    @property
    def IsPermanentlyOn(self) -> bool:
        return self._isPermanentlyOnCOM.GetValue()
    
    @IsPermanentlyOn.setter
    def IsPermanentlyOn(self, value: bool):
        self._isPermanentlyOnCOM.GetValue(value)