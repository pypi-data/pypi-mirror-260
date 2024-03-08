from WITecSDK.Parameters import COMParameters

class ObjectiveTurret:

    def __init__(self, aCOMParameters: COMParameters):
        parampath = "MultiComm|MicroscopeControl|ObjectiveTurrets|Top|"
        self._selectedSlotCOM = aCOMParameters.GetIntParameter(parampath + "SelectedSlot")
        self._changeDistanceCOM = aCOMParameters.GetFloatParameter(parampath + "ObjectiveChangeDistance")

    @property
    def Slot(self) -> int:
        return self._selectedSlotCOM.GetValue()

    @Slot.setter
    def Slot(self, slot: int):
        self._selectedSlotCOM.SetValue(slot)

    @property
    def ChangeDistance(self) -> float:
        return self._changeDistanceCOM.GetValue()

    @ChangeDistance.setter
    def ChangeDistance(self, slot: float):
        self._changeDistanceCOM.SetValue(slot)