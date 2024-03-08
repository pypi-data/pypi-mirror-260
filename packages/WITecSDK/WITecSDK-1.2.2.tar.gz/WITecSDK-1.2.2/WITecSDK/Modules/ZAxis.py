from WITecSDK.Parameters import COMParameters, ParameterNotAvailableException
from asyncio import sleep
from time import sleep as tsleep

class SoftwareZLimits:
    def __init__(self, value):
        self.Min = -value
        self.Max = value

    def IsInRange(self, aValue: float) -> bool:
            return aValue >= self.Min and aValue <= self.Max
    
class SoftwareZConstraints:
    
    def __init__(self, aCOMParameters):
        constraintpath = "UserParameters|HardwareConstraints|"
        self._currentZRangeCOM = aCOMParameters.GetFloatParameter(constraintpath + "MaximumZStepperTravel")
        self._extendedZRangeCOM = aCOMParameters.GetFloatParameter(constraintpath + "ExtendedZStepperTravel")
        self._setExtendedZRangeCOM = aCOMParameters.GetTriggerParameter(constraintpath + "SetExtendedZStepperTravel")
        self._setDefaultZRangeCOM = aCOMParameters.GetTriggerParameter(constraintpath + "SetDefaultZStepperTravel")

    @property
    def CurrentZRange(self) -> float:
        #+/-value
        return self._currentZRangeCOM.GetValue() / 2

    @property
    def Limits(self) -> SoftwareZLimits:
        return SoftwareZLimits(self.CurrentZRange)
        
    def UseExtendedZRange(self, value: float):
        #+/-value
        self._extendedZRangeCOM.SetValue(value * 2)
        self._setExtendedZRangeCOM.ExecuteTrigger()
        if self.CurrentZRange != value:
            raise ZAxisRangeChangeNoSuccessException()

    def UseDefaultZRange(self):
        self._setDefaultZRangeCOM.ExecuteTrigger()
        if self.CurrentZRange != 100:
            raise ZAxisRangeChangeNoSuccessException()

    def verifyInsideLimits(self, zPosition: float):
        limits = self.Limits
        if not limits.IsInRange(zPosition):
            raise ZAxisPositionOutOfLimitsException(zPosition, limits)
        

class ZAxis(SoftwareZConstraints):

# HardwarePosition is User position
# SamplePosition is Software position
# Be aware that altering the User position is possible without constraints. Try to use Software position.
# WITec is not responsible for any damages caused by using this SDK    
    
    def __init__(self, aCOMParameters: COMParameters):
        parampath = "MultiComm|MicroscopeControl|MotorizedXYZ|ZAxis|"
        self._ZAxisInUserSpaceCOM = aCOMParameters.GetBoolParameter(parampath + "ZAxisInUserSpace")
        self._StateCOM = aCOMParameters.GetStringParameter(parampath + "State")
        self._MoveAcceleratedCOM = aCOMParameters.GetBoolParameter(parampath + "MoveAcceleratedWithMaxSpeed")
        self._MinSpeedCOM = aCOMParameters.GetFloatParameter(parampath + "MinSpeed")
        self._MaxSpeedCOM = aCOMParameters.GetFloatParameter(parampath + "MaxSpeed")
        self._SpeedCOM = aCOMParameters.GetFloatParameter(parampath + "Speed")
        self._DesiredSamplePosCOM = aCOMParameters.GetFloatParameter(parampath + "DesiredSamplePosition")
        self._DesiredHardwarePosCOM = aCOMParameters.GetFloatParameter(parampath + "DesiredHardwarePosition")
        self._CurrentSamplePosCOM = aCOMParameters.GetFloatParameter(parampath + "CurrentSamplePosition")
        self._CurrentHardwarePosCOM = aCOMParameters.GetFloatParameter(parampath + "CurrentHardwarePosition")
        self._StopCOM = aCOMParameters.GetTriggerParameter(parampath + "Stop")
        self._MoveToDesiredSamplePosCOM = aCOMParameters.GetTriggerParameter(parampath + "MoveToDesiredSamplePosition")
        self._MoveToDesiredHardwarePosCOM = aCOMParameters.GetTriggerParameter(parampath + "MoveToDesiredHardwarePosition")
        self._zeroSamplePosCOM = aCOMParameters.GetTriggerParameter(parampath + "SetSamplePositionZToZero")
        self._zeroHardwarePosCOM = aCOMParameters.GetTriggerParameter(parampath + "SetHardwarePositionZToZero")
        super().__init__(aCOMParameters)

    @property
    def IsInUserSpace(self) -> bool:
        return self._ZAxisInUserSpaceCOM.GetValue()

    @IsInUserSpace.setter
    def IsInUserSpace(self, value: bool):
        self._ZAxisInUserSpaceCOM.SetValue(value)

    @property
    def State(self) -> str:
        return self._StateCOM.GetValue()

    @property
    def IsMoveAccelerated(self) -> bool:
        return self._MoveAcceleratedCOM.GetValue()

    @IsMoveAccelerated.setter
    def IsMoveAccelerated(self, value: bool):
        #always uses full speed
        self._MoveAcceleratedCOM.SetValue(value)

    @property
    def MinSpeed(self) -> float:
        #µm/s
        return self._MinSpeedCOM.GetValue()

    @property
    def MaxSpeed(self) -> float:
        #µm/s
        return self._MaxSpeedCOM.GetValue()

    @property
    def Speed(self) -> float:
        #µm/s
        return self._SpeedCOM.GetValue()

    @Speed.setter
    def Speed(self, value: float):
        #µm/s
        self._SpeedCOM.SetValue(value)

    @property
    def DesiredSoftwarePos(self) -> float:
        return self._DesiredSamplePosCOM.GetValue()

    @DesiredSoftwarePos.setter
    def DesiredSoftwarePos(self, value: float):
        limits = self.Limits
        if not limits.IsInRange(value):
            raise ZAxisPositionOutOfLimitsException(value, limits)
        
        self._DesiredSamplePosCOM.SetValue(value)

    @property
    def DesiredUserPos(self) -> float:
        return self._DesiredHardwarePosCOM.GetValue()

    @DesiredUserPos.setter
    def DesiredUserPos(self, value: float):
        self._DesiredHardwarePosCOM.SetValue(value)

    @property
    def CurrentSoftwarePos(self) -> float:
        return self._CurrentSamplePosCOM.GetValue()

    @property
    def CurrentUserPos(self) -> float:
        return self._CurrentHardwarePosCOM.GetValue()
    
    @property
    def IsNotMoving(self) -> bool:
        currentpos = self.CurrentUserPos
        tsleep(0.1)
        return currentpos == self.CurrentUserPos

    def Stop(self):
        self._StopCOM.ExecuteTrigger()

    def MoveToDesiredSoftwarePos(self):
        self._MoveToDesiredSamplePosCOM.ExecuteTrigger()
        self.verifyNotInUse()

    def MoveToDesiredUserPos(self):
        self._MoveToDesiredHardwarePosCOM.ExecuteTrigger()
        self.verifyNotInUse()

    def ZeroSoftwarePos(self):
        self._zeroSamplePosCOM.ExecuteTrigger()
        tsleep(0.1)
        if self.CurrentSoftwarePos != 0:
            raise ZAxisZeroNoSuccessException("Software")

    def ZeroUserPos(self):
        self._zeroHardwarePosCOM.ExecuteTrigger()
        tsleep(0.1)
        if self.CurrentUserPos != 0:
            raise ZAxisZeroNoSuccessException("User")

    def verifyNotInUse(self):
        if self.State ==  "Axis In Use":
            raise ZAxisInUseException()

    async def AwaitMoveToSoftwarePos(self, zPosition: float):
        self.DesiredSoftwarePos = zPosition
        self.MoveToDesiredSoftwarePos()
        await self.waitForMovingFinished(zPosition)

    async def AwaitMoveToUserPos(self, zPosition: float):
        self.DesiredUserPos = zPosition
        self.MoveToDesiredUserPos()
        await self.waitForMovingFinished(zPosition)

    async def AwaitNotMoving(self):
        while not self.IsNotMoving:
            await sleep(0.1)

    async def waitForMovingFinished(self, zPosition: float = 0):
        while True:
            zState = self.State

            if zState == "Desired Position Reached":
                break
            elif zState == "":
                break
            elif zState == "Manually Stopped":
                break
            elif zState == "Position not Reached":
                raise ZAxisPositionNotReachedException(zPosition)

            await sleep(0.1)


class ZStepper(SoftwareZConstraints):
    
    _currentPositionZCOM = None

    def __init__(self, aCOMParameters: COMParameters):
        self._positionMicroscopeZCOM = aCOMParameters.GetFloatParameter("UserParameters|ScanTable|PositionMicroscopeZ")
        self._CurrentHardwarePosCOM = aCOMParameters.GetFloatParameter("Status|Hardware|Controller|DataChannels|StepperMotorPosition")
        try:
            self._currentPositionZCOM = aCOMParameters.GetFloatParameter("Status|Software|SamplePositioner|CurrentPositionZ")
        except ParameterNotAvailableException:
            pass
        except Exception as e:
            raise e

        super().__init__(aCOMParameters)

    async def MoveTo(self, zPosition: float):
        self.verifyInsideLimits(zPosition)
        self._positionMicroscopeZCOM.SetValue(zPosition)
        await self.waitForMovingFinished(zPosition)

    async def waitForMovingFinished(self, zPosition: float):
        lastZ = self.GetCurrentZPosition()

        while True:
            await sleep(0.5)
            currentZ = self.GetCurrentZPosition()
            diff = abs(zPosition - currentZ)
            if diff <= 0.02:
                break
            
            if lastZ == currentZ:
                raise ZAxisPositionNotReachedException(zPosition)
            lastZ = currentZ
            
    def GetCurrentZPosition(self) -> float:
        if self._currentPositionZCOM is not None:
            return self._currentPositionZCOM.GetValue()
    
    @property
    def CurrentSoftwarePos(self) -> float:
        if self._currentPositionZCOM is not None:
            return self._currentPositionZCOM.GetValue()
    
    @property
    def CurrentUserPos(self) -> float:
        return self._CurrentHardwarePosCOM.GetValue()

class ZAxisPositionOutOfLimitsException(Exception):
    def __init__(self, requestedPosition: float, currentLimits: SoftwareZLimits):
        super().__init__(f"Requested z Position {requestedPosition:.2f} is out of limits [{currentLimits.Min:.2f},{currentLimits.Max:.2f}]")

class ZAxisPositionNotReachedException(Exception):
    def __init__(self, requestedPosition: float):
        super().__init__(f"Requested z Position {requestedPosition:.2f} not reached.")

class ZAxisInUseException(Exception):
    def __init__(self):
        super().__init__("Z axis already in use.")

class ZAxisZeroNoSuccessException(Exception):
    def __init__(self, axistype: str):
        super().__init__(axistype + " Z axis could not be set to zero.")

class ZAxisRangeChangeNoSuccessException(Exception):
    def __init__(self):
        super().__init__("Not possible to change Software Z range. Probably Z axis in use.")