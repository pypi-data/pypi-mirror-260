from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules.HelperStructs import SamplePositionerPosition
from asyncio import sleep

class SamplePositionerBase:

    positionPollInterval = 0.1
    _parampath = "UserParameters|SamplePositioning|"
    _moveToPositionCOM = None
        
    def __init__(self, aCOMParameters: COMParameters):
        statuspath = "Status|Software|SamplePositioner|"
        self._absolutePositionXCOM = aCOMParameters.GetFloatParameter(self._parampath + "AbsolutePositionX")
        self._absolutePositionYCOM = aCOMParameters.GetFloatParameter(self._parampath + "AbsolutePositionY")
        self._stopDrivingCOM = aCOMParameters.GetTriggerParameter(self._parampath + "StopDriving")
        self._currentPositionXCOM = aCOMParameters.GetFloatParameter(statuspath + "CurrentPositionX")
        self._currentPositionYCOM = aCOMParameters.GetFloatParameter(statuspath + "CurrentPositionY")

    async def MoveTo(self, x: float, y: float):
        await self._moveTo(x, y)

    async def _moveTo(self, x: float, y: float):
        retryCounter = 0

        while True:
            try:
                self._absolutePositionXCOM.SetValue(x)
                self._absolutePositionYCOM.SetValue(y)
                break;

            except:
                if retryCounter == 3:
                     raise

                retryCounter += 1
                await sleep(0.1 * retryCounter)

        self._moveToPositionCOM.ExecuteTrigger();
        await self.waitForMovingFinished()

    async def waitForMovingFinished(self):
        positionNotChangedCounter = 0
        lastX = 0
        lastY = 0

        while True:
            if self.isTargetPositionReached():
                await sleep(0.1)
                break

            currentX = self._currentPositionXCOM.GetValue()
            currentY = self._currentPositionYCOM.GetValue()

            if lastX == currentX and lastY == currentY:
                positionNotChangedCounter += 1
            else:
                positionNotChangedCounter = 0;

            lastX = currentX
            lastY = currentY

            if positionNotChangedCounter >= 5:
                self._stopDrivingCOM.ExecuteTrigger()
                raise SamplePositionerPositionNotReachedException("Requested Position not reached, check End Switches")

            await sleep(self.positionPollInterval)
        

    def isTargetPositionReached(self) -> bool:
        diffX = abs(self._absolutePositionXCOM.GetValue() - self._currentPositionXCOM.GetValue())
        diffY = abs(self._absolutePositionYCOM.GetValue() - self._currentPositionYCOM.GetValue())

        if diffX <= 0.2 and diffY <= 0.2:
            return True
        else:
            return False

    @property
    def CurrentPosition(self) -> SamplePositionerPosition:
        return SamplePositionerPosition(self._currentPositionXCOM.GetValue(), self._currentPositionYCOM.GetValue())


class SamplePositioner(SamplePositionerBase):
    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._moveToPositionCOM = aCOMParameters.GetTriggerParameter(self._parampath + "GoToPosition")


class SamplePositioner51(SamplePositionerBase):
    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._moveToPositionCOM = aCOMParameters.GetTriggerParameter(self._parampath + "GoToPositionWithoutQuery")


class SamplePositionerPositionNotReachedException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
