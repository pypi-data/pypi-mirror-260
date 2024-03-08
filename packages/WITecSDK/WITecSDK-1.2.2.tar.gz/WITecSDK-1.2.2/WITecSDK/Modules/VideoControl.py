from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules.BeamPath import AutomatedCoupler
from asyncio import sleep
import tempfile

class ObjectiveInformation:
    def __init__(self, aFocusDepth: float, aMagnification: float, aInformation: str):
        self.FocusDepth = aFocusDepth
        self.Magnification = aMagnification
        self.Information = aInformation
        
class CalibrationData:
    def __init__(self, aWidth: float, aHeight: float, aRotation: float):
        self.Width = aWidth
        self.Height = aHeight
        self.Rotation = aRotation

class VideoControlBase:

    _videopath = "MultiComm|MicroscopeControl|Video|"
    _tempImagePath = tempfile.gettempdir() + "\\WITec\\temp.png"
    _videoImageFileNameCOM = None
    _saveVideoImageToFileCOM = None
    _acquireVideoImageCOM = None
    VideoCameraCoupler = None

    def __init__(self, aCOMParameters: COMParameters):
        objectivepath = "MultiComm|MicroscopeControl|Objective|"
        self._rotationDegreesCOM = aCOMParameters.GetFloatParameter(self._videopath + "Calibration|RotationDegrees")
        self._imageWidthMicronsCOM = aCOMParameters.GetFloatParameter(self._videopath + "Calibration|ImageWidthMicrons")
        self._imageHeightMicronsCOM = aCOMParameters.GetFloatParameter(self._videopath + "Calibration|ImageHeightMicrons")
        self._focusDepthCOM = aCOMParameters.GetFloatParameter(objectivepath + "SelectedTop|FocusDepth")
        self._informationCOM = aCOMParameters.GetStringParameter(objectivepath + "SelectedTop|Information")
        self._magnificationCOM = aCOMParameters.GetFloatParameter(objectivepath + "SelectedTop|Magnification")
        self._probePositionXCOM = aCOMParameters.GetFloatParameter(self._videopath + "ProbePosition|RelativeX")
        self._probePositionYCOM = aCOMParameters.GetFloatParameter(self._videopath + "ProbePosition|RelativeY")
        self._executeAutoBrightnessCOM = aCOMParameters.GetTriggerParameter(self._videopath + "AutoBrightness|Execute")
        self._selectedCameraCOM = aCOMParameters.GetStringParameter(self._videopath + "SelectedCameraName")
        self._selectTopCameraCOM = aCOMParameters.GetTriggerParameter(self._videopath + "SelectTopCamera")
        self.VideoCameraCoupler = AutomatedCoupler(aCOMParameters, self._videopath + "VideoCameraCoupler")
            
    async def ExecuteAutoBrightness(self) -> bool:
        self._executeAutoBrightnessCOM.ExecuteTrigger()  
        return await self._waitForAutoBrightness()
        
    async def _waitForAutoBrightness(self) -> bool:
        await sleep(1)
        return True
        
    async def AcquireVideoImageToFile(self, imagepath: str = None) -> str:
        if imagepath is None:
            imagepath = self._tempImagePath
        self._videoImageFileNameCOM.SetValue(imagepath)
        self._saveVideoImageToFileCOM.ExecuteTrigger()
        await sleep(1)
        return imagepath

    async def AcquireVideoImage(self):
        self._acquireVideoImageCOM.ExecuteTrigger()
        await sleep(1)
        return

    @property
    def SelectedCameraName(self) -> str:
        return self._selectedCameraCOM.GetValue()
    
    @SelectedCameraName.setter
    def SelectedCameraName(self, name: str):
        self._selectedCameraCOM.SetValue(name)

    def SelectTopCamera(self):
        self._selectTopCameraCOM.ExecuteTrigger()

    def GetCalibrationData(self) -> CalibrationData:
        rotation = self._rotationDegreesCOM.GetValue()
        width = self._imageWidthMicronsCOM.GetValue()
        height = self._imageHeightMicronsCOM.GetValue()
        return CalibrationData(width, height, rotation)

    def GetObjectiveInformation(self) -> ObjectiveInformation:
        focusDepth = self._focusDepthCOM.GetValue()
        magnification = self._magnificationCOM.GetValue()
        information = self._informationCOM.GetValue()
        return ObjectiveInformation(focusDepth, magnification, information)
    
    @property
    def ProbePosition(self) -> tuple[float,float]:
        probeX = self._probePositionXCOM.GetValue()
        probeY = self._probePositionYCOM.GetValue()
        return (probeX, probeY)


class VideoControl50(VideoControlBase):
    
    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._videoImageFileNameCOM = aCOMParameters.GetStringParameter("MultiComm|MultiCommVideoSystem|BitmapFileName")
        self._saveVideoImageToFileCOM = aCOMParameters.GetTriggerParameter("MultiComm|MultiCommVideoSystem|SaveColorBitmapToFile")
        self._acquireVideoImageCOM = aCOMParameters.GetTriggerParameter("UserParameters|VideoSystem|Start")


class VideoControl51(VideoControlBase):
    
    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        self._videoImageFileNameCOM = aCOMParameters.GetStringParameter(self._videopath + "VideoImageFileName")
        self._saveVideoImageToFileCOM = aCOMParameters.GetTriggerParameter(self._videopath + "AcquireVideoImageToFile")
        self._acquireVideoImageCOM = aCOMParameters.GetTriggerParameter(self._videopath + "AcquireVideoImage")


class VideoControl61(VideoControl51):
    
    def __init__(self, aCOMParameters: COMParameters):
        super().__init__(aCOMParameters)
        whitelightpath = "MultiComm|MicroscopeControl|WhiteLight|"
        self._smartBrightnessFactorCOM = aCOMParameters.GetFloatParameter(whitelightpath + "SmartBrightnessFactor")
        self._smartBrightnessFactorMaxCOM = aCOMParameters.GetFloatParameter(whitelightpath + "SmartBrightnessFactorMax")
        self._smartBrightnessPercentageCOM = aCOMParameters.GetFloatParameter(whitelightpath + "SmartBrightnessPercentage")
        self._statusAutoBrightnessCOM = aCOMParameters.GetEnumParameter(self._videopath + "AutoBrightness|Status")

    @property
    def SmartBrightnessFactor(self) -> float:
        return self._smartBrightnessFactorCOM.GetValue()
    
    @SmartBrightnessFactor.setter
    def SmartBrightnessFactor(self, value: float):
        self._smartBrightnessFactorCOM.SetValue(value)

    @property
    def SmartBrightnessFactorMax(self) -> float:
        return self._smartBrightnessFactorMaxCOM.GetValue()

    @property
    def SmartBrightnessPercentage(self) -> float:
        return self._smartBrightnessPercentageCOM.GetValue()
    
    @SmartBrightnessPercentage.setter
    def SmartBrightnessPercentage(self, value: float):
        self._smartBrightnessPercentageCOM.SetValue(value)
    
    async def _waitForAutoBrightness(self) -> bool:
        abstate: int = 0
        while abstate == 0:
            await sleep(0.1)
            abstate = self._statusAutoBrightnessCOM.GetValue()
            #"Running", "LastSucceeded", "LastFailed"
        return abstate == 1
