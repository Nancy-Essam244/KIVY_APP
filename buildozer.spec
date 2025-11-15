[app]

# (str) Title of your application
title = Healthy Chicken

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code directory
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
requirements = python3==3.10, kivy, kivymd, pyjnius

# (str) Presplash of the application
presplash.filename = %(source.dir)s/splash_chicken_chef.png

# (str) Icon of the application
icon.filename = %(source.dir)s/chicken_chef_cooking.png

# (list) Supported orientations
orientation = portrait

# (bool) Fullscreen
fullscreen = 0

# (str) Android entry point (main file)
android.entrypoint = newapp.py

#
# Android specific
#

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup
android.allow_backup = True

# (bool) Copy libraries instead of making a libpymodules.so
android.copy_libs = 1

#
# Buildozer
#

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
