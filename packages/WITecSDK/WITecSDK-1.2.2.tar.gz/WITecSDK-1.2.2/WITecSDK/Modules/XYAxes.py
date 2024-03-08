from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules.HelperStructs import SamplePositionerPosition
from asyncio import sleep
from time import sleep as tsleep

class XYAxes:   
    
    def __init__(self, aCOMParameters: COMParameters):
        parampath = "MultiComm|MicroscopeControl|MotorizedXYZ|XYAxes|"
        self._StateCOM = aCOMParameters.GetStringParameter(parampath + "State")
        self._MoveAcceleratedCOM = aCOMParameters.GetBoolParameter(parampath + "MoveAcceleratedWithMaxSpeed")
        self._MinSpeedCOM = aCOMParameters.GetFloatParameter(parampath + "MinSpeed")
        self._MaxSpeedCOM = aCOMParameters.GetFloatParameter(parampath + "MaxSpeed")
        self._MinSpeedLimitCOM = aCOMParameters.GetFloatParameter(parampath + "MinSpeedLimit")
        self._MaxSpeedLimitCOM = aCOMParameters.GetFloatParameter(parampath + "MaxSpeedLimit")
        self._UseSpeedLimitCOM = aCOMParameters.GetBoolParameter(parampath + "UseSpeedLimit")
        self._SpeedCOM = aCOMParameters.GetFloatParameter(parampath + "Speed")
        self._DesiredSamplePosXCOM = aCOMParameters.GetFloatParameter(parampath + "DesiredSamplePositionX")
        self._DesiredSamplePosYCOM = aCOMParameters.GetFloatParameter(parampath + "DesiredSamplePositionY")
        self._CurrentSamplePosXCOM = aCOMParameters.GetFloatParameter(parampath + "CurrentSamplePositionX")
        self._CurrentSamplePosYCOM = aCOMParameters.GetFloatParameter(parampath + "CurrentSamplePositionY")
        self._StopCOM = aCOMParameters.GetTriggerParameter(parampath + "Stop")
        self._MoveToDesiredSamplePosCOM = aCOMParameters.GetTriggerParameter(parampath + "MoveToDesiredSamplePosition")
        self._zeroSamplePosCOM = aCOMParameters.GetTriggerParameter(parampath + "SetSamplePositionToZero")
        self._MoveToCalibrationPosCOM = aCOMParameters.GetTriggerParameter(parampath + "MoveToCalibrationPosition")
        self._ResetCoordinateSysCOM = aCOMParameters.GetTriggerParameter(parampath + "ResetCoordinateSystem")

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
    def MinSpeedLimit(self) -> float:
        #µm/s
        return self._MinSpeedLimitCOM.GetValue()

    @property
    def MaxSpeedLimit(self) -> float:
        #µm/s
        return self._MaxSpeedLimitCOM.GetValue()

    @property
    def Speed(self) -> float:
        #µm/s
        return self._SpeedCOM.GetValue()

    @Speed.setter
    def Speed(self, value: float):
        #µm/s
        self._SpeedCOM.SetValue(value)

    @property
    def DesiredSoftwarePos(self) -> SamplePositionerPosition:
        return SamplePositionerPosition(self._DesiredSamplePosXCOM.GetValue(), self._DesiredSamplePosYCOM.GetValue())

    @DesiredSoftwarePos.setter
    def DesiredSoftwarePos(self, xy: SamplePositionerPosition):
        self._DesiredSamplePosXCOM.SetValue(xy.X)
        self._DesiredSamplePosYCOM.SetValue(xy.Y)

    @property
    def CurrentSoftwarePos(self) -> SamplePositionerPosition:
        return SamplePositionerPosition(self._CurrentSamplePosXCOM.GetValue(), self._CurrentSamplePosYCOM.GetValue())
    
    @property
    def IsNotMoving(self) -> bool:
        currentpos = self.CurrentSoftwarePos
        tsleep(0.1)
        return currentpos == self.CurrentSoftwarePos

    def Stop(self):
        self._StopCOM.ExecuteTrigger()

    def MoveToDesiredSoftwarePos(self):
        self._MoveToDesiredSamplePosCOM.ExecuteTrigger()
        self.verifyNotInUse()

    def ZeroSoftwarePos(self):
        self._zeroSamplePosCOM.ExecuteTrigger()
        tsleep(0.1)
        currentXY = self.CurrentSoftwarePos
        if currentXY.X != 0 or currentXY.Y != 0:
            raise XYAxesZeroNoSuccessException()
        
    def MoveToCalibrationPosition(self):
        self._MoveToCalibrationPosCOM.ExecuteTrigger()

    def ResetCoordinateSystem(self):
        self._ResetCoordinateSysCOM.ExecuteTrigger()

    def verifyNotInUse(self):
        if self.State ==  "Axis In Use":
            raise XYAxesInUseException()

    async def AwaitMoveToSoftwarePos(self, xy: SamplePositionerPosition):
        self.DesiredSoftwarePos = xy
        self.MoveToDesiredSoftwarePos()
        await self.waitForMovingFinished(xy)

    async def AwaitNotMoving(self):
        while not self.IsNotMoving:
            await sleep(0.1)

    async def waitForMovingFinished(self, xy: SamplePositionerPosition = SamplePositionerPosition()):
        while True:
            xyState = self.State

            if xyState == "Desired Position Reached":
                break
            elif xyState == "":
                break
            elif xyState == "Manually Stopped":
                break
            elif xyState == "Position not Reached":
                raise XYAxesPositionNotReachedException(xy)

            await sleep(0.1)
        

class XYAxesPositionNotReachedException(Exception):
    def __init__(self, xy: SamplePositionerPosition):
        super().__init__("Requested Position " + str(xy) + " not reached.")

class XYAxesInUseException(Exception):
    def __init__(self):
        super().__init__("XY axes already in use.")

class XYAxesZeroNoSuccessException(Exception):
    def __init__(self):
        super().__init__("XY axes could not be set to zero.")
