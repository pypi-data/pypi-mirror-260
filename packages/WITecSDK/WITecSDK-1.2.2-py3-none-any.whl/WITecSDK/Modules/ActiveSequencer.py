from WITecSDK.Parameters import COMParameters, COMStringStatusParameter
from asyncio import sleep
from _ctypes import COMError

class ActiveSequencer:
    
    _parampath = "Status|Software|Sequencers|"

    def __init__(self, aParameters: COMParameters):
        self._isASequencerActiveCOM = aParameters.GetBoolParameter(self._parampath + "IsASequencerActive")
        self._activeSequencerNameCOM = aParameters.GetStringParameter(self._parampath + "ActiveSequencer|Name")
        self._currentActivityCOM = aParameters.GetStringParameter(self._parampath + "ActiveSequencer|CurrentActivity")
        self._stopSequencerCOM = aParameters.GetTriggerParameter("UserParameters|StopSequencer")
        self._showViewersCOM = aParameters.GetEnumParameter("UserParameters|CreateViewers")
        
    @property
    def ActiveSequencerName(self) -> str:
        return self._getParameterValue(self._activeSequencerNameCOM)

    @property
    def CurrentActivity(self) -> str:
        return self._getParameterValue(self._currentActivityCOM)

    @property
    def IsASequencerActive(self) -> bool:
        return self._isASequencerActiveCOM.GetValue()
    
    @property
    def ShowViewers(self) -> bool:
        return bool(self._showViewersCOM.GetValue())
    
    @ShowViewers.setter
    def ShowViewers(self, value: bool):
        self._showViewersCOM.SetValue(int(value))

    async def WaitActiveSequencerFinished(self):
        while self.IsASequencerActive:
            await sleep(0.1)

    def StopActiveSequencer(self):
        self._stopSequencerCOM.ExecuteTrigger()
     
    async def StopActiveSequencerAndWaitUntilFinished(self):
        self.StopActiveSequencer()
        await self.WaitActiveSequencerFinished()

    def _getParameterValue(self, paramobj: COMStringStatusParameter) -> str:
        val = None
        try:
            val = paramobj.GetValue()
        except COMError as e:
            # Throws an exception, if there is no active sequencer. 
            # This can happen, if a sequencer stops working inbetween two operations.
            if e.hresult != -2147024891: #UnauthorizedAccessException
                raise e
        except Exception as e:
            raise e
        return val
    

class ActiveSequencer60(ActiveSequencer):
    
    def __init__(self, aParameters: COMParameters):
        super().__init__(aParameters)
        self._statusOrResultCOM = aParameters.GetStringParameter(self._parampath + "StatusOrResult")

    @property
    def StatusAndResult(self) -> tuple[str, str]:
        value = self._statusOrResultCOM.GetValue().split('|')
        #Status: "Running", "Finished", "Warning", "Error", "StoppedByUser"
        status = value[0]
        result = ''
        if len(value) == 2:
            result = value[1]
        return status, result


class ActiveSequencer62(ActiveSequencer60):
    
    def __init__(self, aParameters: COMParameters):
        super().__init__(aParameters)
        self._askForUserOKCOM = aParameters.GetBoolParameter("UserParameters|AskForUserOK")

    @property
    def AskForUserOK(self) -> bool:
        return self._askForUserOKCOM.GetValue()
    
    @AskForUserOK.setter
    def AskForUserOK(self, value: bool):
        self._askForUserOKCOM.SetValue(value)