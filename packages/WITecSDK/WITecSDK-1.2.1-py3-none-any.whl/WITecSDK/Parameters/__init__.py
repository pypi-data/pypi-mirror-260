"""Handles the different parameter types used by WITec Control"""

from WITecSDK.Parameters.COMParameter import (COMBoolParameter, COMStringParameter, COMTriggerParameter)
from WITecSDK.Parameters.COMEnumParameter import COMEnumParameter
from WITecSDK.Parameters.COMFloatParameter import COMFloatParameter
from WITecSDK.Parameters.COMIntParameter import COMIntParameter
from WITecSDK.Parameters.COMStatusParameter import (COMIntStatusParameter, COMBoolStatusParameter, COMFloatStatusParameter,
                                                    COMStringStatusParameter, COMArrayStatusParameter)
from WITecSDK.Parameters.COMFillStatusParameter import COMStringFillStatusParameter, COMFloatFillStatusParameter
from WITecSDK.Parameters.COMParameterBase import ParameterNotAvailableException
from WITecSDK import COMClient
from enum import Enum

class WITecParameterType(Enum):
    """Enumeration defining the parameters data type"""

    Bool = 0
    String = 1
    Float = 2
    Int = 3
    Enum = 4
    Trigger = 5
    Array = 6

stringToParameterType = {
    "int": WITecParameterType.Int,
    "bool": WITecParameterType.Bool,
    "float": WITecParameterType.Float,
    "trigger": WITecParameterType.Trigger,
    "string": WITecParameterType.String,
    "enum": WITecParameterType.Enum,
    "uint[2]": WITecParameterType.Array
}

class COMParameters:
    """Creates the different parameter types and checks type and existence"""

    def __init__(self, aClient: COMClient):
        """Creates and stores a dictonary with all available parameters"""
        self._client = aClient
        self._comParameterDescriptions = self.GetAllParameterDescriptions()

    def GetIntParameter(self, aParameter: str) -> COMIntStatusParameter|COMIntParameter:
        """Creates a parameter or status parameter of type integer"""
        
        self._throwIfWrongParameterType(WITecParameterType.Int, aParameter)
        if self._isStatusContainer(aParameter):
            return COMIntStatusParameter(aParameter, self._client)
        else:
            return COMIntParameter(aParameter, self._client)

    def GetBoolParameter(self, aParameter: str) -> COMBoolStatusParameter|COMBoolParameter:
        """Creates a parameter or status parameter of type boolean"""
        
        self._throwIfWrongParameterType(WITecParameterType.Bool, aParameter)
        if self._isStatusContainer(aParameter):
            return COMBoolStatusParameter(aParameter, self._client)
        else:
            return COMBoolParameter(aParameter, self._client)

    def GetFloatParameter(self, aParameter: str) -> COMFloatStatusParameter|COMFloatParameter:
        """Creates a parameter or status parameter of type floating point"""
        
        self._throwIfWrongParameterType(WITecParameterType.Float, aParameter)
        if self._isStatusContainer(aParameter):
            return COMFloatStatusParameter(aParameter, self._client)
        else:
            return COMFloatParameter(aParameter, self._client)

    def GetStringParameter(self, aParameter: str) -> COMStringStatusParameter|COMStringParameter:
        """Creates a parameter or status parameter of type string"""
        
        self._throwIfWrongParameterType(WITecParameterType.String, aParameter)
        if self._isStatusContainer(aParameter):
            return COMStringStatusParameter(aParameter, self._client)
        else:
            return COMStringParameter(aParameter, self._client)

    def GetEnumParameter(self, aParameter: str) -> COMEnumParameter:
        """Creates a parameter of type enumeration"""
        
        self._throwIfWrongParameterType(WITecParameterType.Enum, aParameter)
        return COMEnumParameter(aParameter, self._client)

    def GetTriggerParameter(self, aParameter: str) -> COMTriggerParameter:
        """Creates a parameter of type trigger"""
        
        self._throwIfWrongParameterType(WITecParameterType.Trigger, aParameter)
        return COMTriggerParameter(aParameter, self._client)
    
    def GetArrayStatusParameter(self, aParameter: str) -> COMArrayStatusParameter:
        """Creates a array status parameter"""
        
        self._throwIfWrongParameterType(WITecParameterType.Array, aParameter)
        return COMArrayStatusParameter(aParameter, self._client)

    def GetStringFillStatusParameter(self, aParameter: str) -> COMStringFillStatusParameter:
        """Creates a fill status parameter of type string"""
        
        self._throwIfWrongParameterType(WITecParameterType.String, aParameter)
        return COMStringFillStatusParameter(aParameter, self._client)
    
    def GetFloatFillStatusParameter(self, aParameter: str) -> COMFloatFillStatusParameter:
        """Creates a fill status parameter of type floating point"""
        
        self._throwIfWrongParameterType(WITecParameterType.Float, aParameter)
        return COMFloatFillStatusParameter(aParameter, self._client)

    def _throwIfWrongParameterType(self, expected: WITecParameterType, aParameter: str):
        paramtype = self._comParameterDescriptions.get(aParameter)
        if paramtype is None:
            raise ParameterNotAvailableException(f"The COM-Parameter {aParameter} is not available.")
        if paramtype != expected:
            raise ParameterWrongTypeException(f"The COM-Parameter {aParameter} is of type {paramtype}. Please use the appropriate COM-Parameter class.")
        
    def GetAllParameterDescriptions(self) -> dict[str, WITecParameterType]:
        """Creates a dictonary with all available parameters"""

        subSystems = self._getAllSubSystemNames()
        subsysparamlist = {}
        for name in subSystems:
            subsysparamlist.update(self._getSubsystemParameterList(name))
        return subsysparamlist

    def _getAllSubSystemNames(self) -> list[str]:
        subSystemNames = []
        subSystemList = self._client.GetSubSystemsList(None, 0)
        numberOfSystems = subSystemList.GetNumberOfSystems()
        for i in range(numberOfSystems):
            name = subSystemList.GetSubSystemName(i)
            subSystemNames.append(name)
        return subSystemNames

    def _getSubsystemParameterList(self, name: str) -> dict[str, WITecParameterType]:
        subSystemList = {}
        subsyslist = self._client.GetSubSystemsList(name, 10)
        number = subsyslist.GetNumberOfSystems()

        for j in range(number):
            subSystemName = subsyslist.GetSubSystemName(j)
            typeString, parameterName = self._getTypeAndName(subSystemName)
            partype = stringToParameterType.get(typeString)
            if partype == None:
                continue
            subSystemList[parameterName] = partype
        return subSystemList

    @classmethod
    def _getTypeAndName(cls, parameterDescription: str) -> tuple[str, str]:
        res = parameterDescription.split(':', 1)
        typeString = res[0].lower()
        parameterName = res[1]

        return (typeString, parameterName)
    
    @classmethod
    def _isStatusContainer(cls, aParameterName: str) -> bool:
        return aParameterName.lower().startswith("status")

class ParameterWrongTypeException(Exception):
    pass