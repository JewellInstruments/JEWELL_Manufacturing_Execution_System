@echo off
echo Updating UI File
pyside6-uic RUBY.ui -o RUBY_UI.py
pyside6-uic LoginPopup.ui -o LoginPopup.py
pause