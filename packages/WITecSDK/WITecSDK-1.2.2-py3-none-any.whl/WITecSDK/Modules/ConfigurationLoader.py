from WITecSDK.Parameters import COMParameters

class ConfigurationLoader:

    def __init__(self, aCOMParameters: COMParameters):
        self._loadConfigurationCOM = aCOMParameters.GetStringParameter("ApplicationControl|LoadConfiguration")

    @property
    def Configuration(self) -> str:
        return self._loadConfigurationCOM.GetValue()

    @Configuration.setter
    def Configuration(self, configurationName):
        self._loadConfigurationCOM.SetValue(configurationName)