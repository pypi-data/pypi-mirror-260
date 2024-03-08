from WITecSDK.Parameters import COMParameters, ParameterNotAvailableException
from WITecSDK.Parameters.COMParameterBase import NoWriteAccessException

class StateManager:

    def __init__(self, aCOMParameters: COMParameters):
        parampath = "MultiComm|MicroscopeControl|StateManager|"
        self._stateNameCOM = aCOMParameters.GetStringParameter(parampath + "StateName")
        self._resetAllCOM = aCOMParameters.GetTriggerParameter(parampath + "ResetAll")

    @property
    def State(self) -> str:
        return self._stateNameCOM.GetValue()
    
    @State.setter
    def State(self, value: str):
        self._stateNameCOM.SetValue(value)

    def ResetAll(self):
        self._resetAllCOM.ExecuteTrigger()