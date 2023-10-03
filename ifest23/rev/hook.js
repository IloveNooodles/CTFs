Java.perform(function () {
  var a = Java.use('com.ifest.passmanager.detectors.EmulatorDetection');
  a.isEmulator.implementation = function () {
    return false;
  };

  var b = Java.use('com.ifest.passmanager.detectors.RootDetection');
  b.isDeviceRooted.implementation = function () {
    return false;
  };
});
