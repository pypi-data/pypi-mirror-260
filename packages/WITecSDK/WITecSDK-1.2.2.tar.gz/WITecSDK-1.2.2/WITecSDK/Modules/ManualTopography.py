from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules import XYAxes, ZAxis, SpectralAutofocus, ActiveSequencer
from WITecSDK.Modules.HelperStructs import XYZPosition
from asyncio import sleep
from collections.abc import Callable

class ManualTopography:

    def __init__(self, aCOMParameters: COMParameters, xyaxes: XYAxes, zaxis: ZAxis, specaf: SpectralAutofocus, actsequ: ActiveSequencer):
        self._xyaxes = xyaxes
        self._zaxis = zaxis
        self._specaf = specaf
        self._actsequ = actsequ
        parampath = "UserParameters|SequencerTrueSurface|ManualLearning|"
        self._learnPlaneCOM = aCOMParameters.GetTriggerParameter(parampath + "Learn3PointPlane")
        self._learnSurfaceCOM = aCOMParameters.GetTriggerParameter(parampath + "Learn5x5Surface")
        self._nextStepCOM = aCOMParameters.GetTriggerParameter(parampath + "NextStep")
        self._LASurfaceCorrectionCOM = aCOMParameters.GetEnumParameter("UserParameters|SequencerLargeScaleImaging|SurfaceCorrection")

    def LearnPlane(self):
        self._learnPlaneCOM.ExecuteTrigger()

    def LearnSurface(self):
        self._learnSurfaceCOM.ExecuteTrigger()

    def NextStep(self):
        self._nextStepCOM.ExecuteTrigger()

    async def AutomatePlane(self) -> list[bool]:
        return await self._automate(self.LearnPlane, 3)

    async def AutomateSurface(self) -> list[bool]:
        return await self._automate(self.LearnSurface, 25)

    async def _automate(self, learntrigger: Callable[[], None], no: int) -> list[bool]:
        positionlist = []
        successlist = []
        
        # Read xy positions
        learntrigger()
        await sleep(1)
        print("Learn positions")
        for i in range(no):
            await self._xyaxes.AwaitNotMoving()
            await sleep(2)
            xypos = self._xyaxes.CurrentSoftwarePos
            positionlist.append(XYZPosition(xypos.X, xypos.Y, 0))
            self.NextStep()
        await self._actsequ.WaitActiveSequencerFinished()
        
        # Do Autofocus on postions
        print("Autofocus")
        for i in range(no):
            await self._xyaxes.AwaitMoveToSoftwarePos(positionlist[i].SamplePosition)
            self._specaf.Start()
            await self._actsequ.WaitActiveSequencerFinished()
            stat, res = self._actsequ.StatusAndResult
            successlist.append(stat == "Finished")
            positionlist[i].Z = self._zaxis.CurrentSoftwarePos
            print(positionlist[i].Z)

        # Teach z coordinates
        print("Teach z")
        learntrigger()
        await sleep(1)
        for i in range(no):
            await self._xyaxes.AwaitNotMoving()
            await sleep(2)
            await self._zaxis.AwaitMoveToSoftwarePos(positionlist[i].Z)
            self.NextStep()
        await self._actsequ.WaitActiveSequencerFinished()
        self._LASurfaceCorrectionCOM.SetValue(1)