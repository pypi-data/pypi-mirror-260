from WITecSDK.Parameters import COMParameters
from asyncio import sleep

class AutoFocus:

    _parampath = "MultiComm|MicroscopeControl|Video|"

    def __init__(self, aCOMParameters: COMParameters):
        self._executeAutoFocusCOM = aCOMParameters.GetTriggerParameter(self._parampath + "AutoFocus|Execute")

    async def ExecuteAutoFocus(self) -> bool:
        self._executeAutoFocusCOM.ExecuteTrigger()
        return await self._waitForAutoFocus()

    async def _waitForAutoFocus(self) -> bool:
        await sleep(5)
        return True
        
class AutoFocus61(AutoFocus):

    def __init__(self, aCOMParameters: COMParameters):
        self._statusAutoFocusCOM = aCOMParameters.GetEnumParameter(self._parampath + "AutoFocus|Status")
        #"Running", "LastSucceeded", "LastFailed"

    async def _waitForAutoFocus(self) -> bool:
        afstate: int = 0
        while afstate == 0:
            await sleep(0.1)
            afstate = self._statusAutoFocusCOM.GetValue()
        return afstate == 1