# WITecSDK package

## Changes in 1.2.0

- New WITec Control 6.2 features implemented (for LineScan, LargeAreaScan, ActiveSequencer, TrueSurface)
- docstrings added
- compatibility down to WITec Control 5.0 added
- New class LaserPowerSeries
- New structure for Polarization class
- CalibrationLamp and AdjustmentSampleCoupler added to BeamPath
- LineScan has own Integration time and Accumulation property
- LaserManager gives the corrected laser power by default (old property removed)
- New property Unit for Spectrograph

## Changes in 1.1.2

- New property HideViewers for the ActiveSequencer
- New property WriteAccess in the COMClient replacing old implemantation
- New property ReadAccess for the COMClient and HasReadAccess for the main class
- Improved error handling in __del__ of COMClient

## Changes in 1.1.1

- Bug in ProjectCreatorSaver module corrected
- property ExtraDirectory renamed to SubDirectory (read-only) and method DefineSubDirectory()

## Changes in 1.1.0

- New class AutomatedCoupler attached to TopIllumination and VideoControl, if automated
- New classes inheriting from its main class to implement versiongreater61 features
- New class DetectorOutput for internal use
- __del__ removed from all modules