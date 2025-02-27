cd %~dp0%
pyinstaller --onefile --uac-admin --windowed --add-data "icon.ico:." --add-data "bg1.png:." --add-data "bg2.png:." --add-data "background.png:." -i "icon.ico" study_timer.py