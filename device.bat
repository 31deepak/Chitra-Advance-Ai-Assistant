@echo off
echo Disconnecting old connections...
adb disconnect

echo Setting up connected device...
adb tcpip 5555

echo Waiting for device to initialize...
timeout 3

rem Retrieve device IP address
FOR /F "tokens=2" %%G IN ('adb shell ip addr show wlan0 ^| find "inet "') DO set ipfull=%%G
FOR /F "tokens=1 delims=/" %%G in ("%ipfull%") DO set ip=%%G

echo Connecting to device with IP %ip%...
adb connect %ip%

rem Set the IP address of your Android device
set DEVICE_IP=192.0.0.4

rem Set the port number for ADB
set ADB_PORT=5555

rem Set the path to the ADB executable (Update this path)
set ADB_PATH="C:\Users\Dell\Downloads\platform-tools-latest-windows\platform-tools\adb"

rem Restart the ADB server
%ADB_PATH% kill-server
%ADB_PATH% start-server

rem Connect to the Android device over Wi-Fi
%ADB_PATH% connect %DEVICE_IP%:%ADB_PORT%



