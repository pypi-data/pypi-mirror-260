#For internal use only, can be removed or changed in future versions
from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules.BeamPath import BeamPath
from asyncio import sleep
from time import sleep as tsleep

class SilentSpectrum:

    def __init__(self, aCOMParameters: COMParameters, aBeamPath: BeamPath):
        self._beamPath = aBeamPath
        parampath = "MultiComm|SequencerSingleSpectrum|"
        self._acquisitionParameterCOM = aCOMParameters.GetStringParameter(parampath + "SilentSpectrumAcquisitionParameter")
        self._acquisitionInformationCOM = aCOMParameters.GetStringParameter(parampath + "SilentSpectrumAcquisitionInformation")
        self._sequenceDoneCOM = aCOMParameters.GetBoolParameter(parampath + "SilentSpectrumSequenceDone")
        self._spectrumAsTextCOM = aCOMParameters.GetStringParameter(parampath + "SilentSpectrumAsText")
        self._errorCOM = aCOMParameters.GetStringParameter(parampath + "SilentSpectrumError")
        self._startSilentSpectrumCOM = aCOMParameters.GetTriggerParameter(parampath + "StartSilentSpectrumAcquisition")

    def SetParameters(self, numberOfAccumulations: int, integrationTime: float):
        parameterString = f"IntegrationTime {integrationTime}\n NumberOfAccumulations {numberOfAccumulations}\n"
        self._acquisitionParameterCOM.SetValue(parameterString)

    def GetacquisitionInformation(self) -> str:
        return self._acquisitionInformationCOM.GetValue()

    def GetSpectrumAsText(self) -> str:
        return self._spectrumAsTextCOM.GetValue()

    def IsSequenceDone(self) -> bool:
        return self._sequenceDoneCOM.GetValue()

    def ResetSequenceDone(self):
        self._sequenceDoneCOM.SetValue(False)

    def GetError(self) -> str:
        return self._errorCOM.GetValue()

    def Start(self):
        self._startSilentSpectrumCOM.ExecuteTrigger()

    async def AwaitSilentSpectrumAvailableBeamPath(self) -> str:
        self._beamPath.SetRaman()
        result = await self.AwaitSilentSpectrumAvailable()
        return result

    async def AwaitSilentSpectrumAvailable(self) -> str:
        # Returns when spectrum is available, sequence maybe not completed, check with ActiveSequencer
        self.ResetSequenceDone()
        self.Start()
        await self.waitUntilFinished()
        self.throwIfError()
        return self.GetSpectrumAsText()

    async def waitUntilFinished(self):
        while True:
            val = self.IsSequenceDone()
            if val:
                break
            await sleep(0.1)

    def throwIfError(self):
        result = self.GetError()
        if result != "Ok":
            raise SilentSpectrumNoSuccessException(result)


class SilentSpectrumNoSuccessException(Exception):
    def __init__(self, errormsg: str):
        super().__init__("Silent spectrum ended with error: " + errormsg)
