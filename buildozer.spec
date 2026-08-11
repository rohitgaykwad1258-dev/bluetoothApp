[app]
title = Bluetooth Scanner
package.name = bluetoothapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,kivymd,bleak,android
orientation = portrait
android.permissions = ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, BLUETOOTH_SCAN, BLUETOOTH_CONNECT
android.api = 35
android.minapi = 21
android.archs = arm64-v8a
