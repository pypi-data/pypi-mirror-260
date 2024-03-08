from WITecSDK.Parameters import COMParameters
from datetime import date
from _ctypes import COMError

class ProjectCreatorSaver:

    def __init__(self, aCOMParameters: COMParameters):
        parampath = "UserParameters|AutoSaveProject|"
        self._storeProjectCOM = aCOMParameters.GetTriggerParameter(parampath + "StoreProject")
        self._startDirectoryCOM = aCOMParameters.GetStringParameter(parampath + "StartDirectory")
        self._extraDirectoryCOM = aCOMParameters.GetStringParameter(parampath + "ExtraDirectory")
        self._fileNameCOM = aCOMParameters.GetStringParameter(parampath + "FileName")
        self._fileNumberCOM = aCOMParameters.GetIntParameter(parampath + "FileNumber")
        self._directoryModeCOM = aCOMParameters.GetEnumParameter(parampath + "DirectoryMode")
        self._storeModeCOM = aCOMParameters.GetEnumParameter(parampath + "StoreMode")
        self._overwriteModeCOM = aCOMParameters.GetEnumParameter(parampath + "OverwriteMode")
        self._newProjectCOM = aCOMParameters.GetTriggerParameter("ApplicationControl|NewProject")
        self._appendProjectCOM = aCOMParameters.GetStringParameter("ApplicationControl|FileNameToAppendToProject")
        self._currentProjectNameCOM = aCOMParameters.GetStringParameter("Status|Software|Application|CurrentFileName")

    #Saves project in the start directory

    def SaveProject(self, fileName: str, directory = None):
        if directory is not None:
            initialDirectoryMode = self._directoryModeCOM.GetValue()
            initialStartDirectory = self.StartDirectory

            self.StartDirectory = directory
            self._directoryModeCOM.SetValue(0)
        
        self.ClearAfterStore = True
        self.OverwriteExisting = False
        self.FileName = fileName
        self.AutoSave()
        
        if directory is not None:
            self.StartDirectory = initialStartDirectory
            self._directoryModeCOM.SetValue(initialDirectoryMode)

    def AppendProject(self, fileName: str):
        self._appendProjectCOM.SetValue(fileName)

    def CreateNewProject(self):
        self._newProjectCOM.ExecuteTrigger()

    def AutoSave(self):
        self._storeProjectCOM.ExecuteTrigger()

    @property
    def CurrentProjectName(self) -> str:
        val = None
        try:
            val = self._currentProjectNameCOM.GetValue()
        except COMError as e:
            # Throws an exception, if project is not saved yet. 
            if e.hresult != -2147467263: #NotImplemented
                raise e
        except Exception as e:
            raise e
        return val
    
    @property
    def StartDirectory(self) -> str:
        return self._startDirectoryCOM.GetValue()

    @StartDirectory.setter
    def StartDirectory(self, value: str):
        self._startDirectoryCOM.SetValue(value)
        
    @property
    def SubDirectory(self) -> str:
        dirmode = self._directoryModeCOM.GetValue()
        extradir = self._extraDirectoryCOM.GetValue()
        datestr = date.today().strftime("%Y%m%d")
        if dirmode == 0:
            return ""
        elif dirmode == 1:
            return extradir
        elif dirmode == 2:
            return datestr
        elif dirmode == 3:
            return extradir + "\\" + datestr
        elif dirmode == 4:
            return datestr + "\\" + extradir

    def DefineSubDirectory(self, value: str, useDate: bool = False, putDateFirst: bool = False):
        if value is None or value == "":
            if useDate:
                self._directoryModeCOM.SetValue(2)
            else:
                self._directoryModeCOM.SetValue(0)
        else:
            self._extraDirectoryCOM.SetValue(value)
            if useDate:
                if putDateFirst:
                    self._directoryModeCOM.SetValue(4)
                else:
                    self._directoryModeCOM.SetValue(3)
            else:
                self._directoryModeCOM.SetValue(1)
        
    @property
    def FileName(self) -> str:
        return self._fileNameCOM.GetValue()

    @FileName.setter
    def FileName(self, value: str):
        self._fileNameCOM.SetValue(value)
        
    @property
    def FileNumber(self) -> int:
        return self._fileNumberCOM.GetValue()

    @FileNumber.setter
    def FileNumber(self, value: int):
        self._fileNumberCOM.SetValue(value)

    @property
    def ClearAfterStore(self) -> bool:
        return bool(self._storeModeCOM.GetValue())

    @ClearAfterStore.setter
    def ClearAfterStore(self, value: bool):
        self._storeModeCOM.SetValue(int(value))
        
    @property
    def OverwriteExisting(self) -> bool:
        return bool(self._overwriteModeCOM.GetValue())

    @OverwriteExisting.setter
    def OverwriteExisting(self, value: bool):
        self._overwriteModeCOM.SetValue(int(value))