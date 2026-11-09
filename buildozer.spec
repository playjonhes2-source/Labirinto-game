[app]
title = Labirinto
package.name = labirinto
package.domain = org.exemplo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions =
android.api =  beta
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True
