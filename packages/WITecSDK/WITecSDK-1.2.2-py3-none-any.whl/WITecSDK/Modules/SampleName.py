from WITecSDK.Parameters import COMParameters

class SampleName:

    def __init__(self, aCOMParameters: COMParameters):
        self._sampleNameCOM = aCOMParameters.GetStringParameter("UserParameters|Naming|SampleName")
        self._formatCOM = aCOMParameters.GetEnumParameter("UserParameters|Naming|Format")
        self._counterCOM = aCOMParameters.GetIntParameter("UserParameters|Naming|Counter")

    @property
    def SampleName(self) -> str:
        return self._sampleNameCOM.GetValue()
    
    @SampleName.setter
    def SampleName(self, sampleName: str):
        self._sampleNameCOM.SetValue(sampleName)

    @property
    def Counter(self) -> int:
        return self._counterCOM.GetValue()

    @Counter.setter
    def Counter(self, counter: int):
        self._counterCOM.SetValue(counter)

    def setLongDescription(self):
        self._formatCOM.SetValue(0)

    def setShortDescription(self):
        self._formatCOM.SetValue(1)

    def setNameOnly(self):
        self._formatCOM.SetValue(2)