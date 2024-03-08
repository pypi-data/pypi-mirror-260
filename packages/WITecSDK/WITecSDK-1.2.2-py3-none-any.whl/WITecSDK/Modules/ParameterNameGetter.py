from WITecSDK.Parameters import COMParameters, stringToParameterType

class ParameterNameGetter:

    def __init__(self, aParameters: COMParameters):
        self._parameters = aParameters
        self._typeToString = {}
        for key, value in stringToParameterType.items():
            self._typeToString[value] = key

    def GetNamesOfAvailableParameters(self) -> list[str]:
        parameterNames = []
        for key, value in self._parameters._comParameterDescriptions.items():
            typeString = self._typeToString[value]
            parameterNames.append(typeString + ':' + key)
        return parameterNames
    
    def GetNamesOfAvailableDataChannels(self) -> list[str]:
        channelNames = []
        for key in self._parameters._comParameterDescriptions.items():
            if key.startswith("Status|Hardware|Controller|DataChannels|"):
                channelNames.append(key)
        return channelNames

    def WriteParameterNamesToFile(self, filePath: str):
        self._writeListToFile(filePath, self.GetNamesOfAvailableParameters())
    
    def WriteDataChannelsToFile(self, filePath: str):
        self._writeListToFile(filePath, self.GetNamesOfAvailableDataChannels())

    @classmethod
    def _writeListToFile(cls, filePath: str, paramlist: list[str]):
        with open(filePath, 'w') as f:
            f.write('\n'.join(x for x in paramlist))
