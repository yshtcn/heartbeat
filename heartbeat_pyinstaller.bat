@echo off
title "AutoPyInstaller����װ����pyinstaller"
:: ��װ/����pyinstaller(ע�⣺��ϣ���Զ���װ/����pyinstaller�ǵ�ע�͵���
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple


:: ���±���
title "AutoPyInstaller����ʼ��"

:: ����������һЩ��Ϣ
set "ProductName=heartbeat"
set "InternalName=yshtcn"
set "Comments=GitHub: https://github.com/yshtcn/heartbeat"


:: �������������ڵ�Ŀ¼
cd /d %~dp0



:: ���±���
title "AutoPyInstaller�����ɰ汾�ļ�"



:: ʹ��WMIC��ȡ��ǰ����
for /f "delims=" %%a in ('wmic os get localdatetime ^| find "."') do set datetime=%%a


:: �ֽ�����ʱ���ַ���
set "year=%datetime:~0,4%"
set "month=%datetime:~4,2%"
set "day=%datetime:~6,2%"

:: ��ȡ�汾�����һλ
set /p "revision=���������İ汾��:(%year%, %month%, %day%,[?]):"

:: ��ǰ�汾Ŀ¼��δȥ���ȵ�0��
set "versionFolder=%year%_%month%_%day%_%revision%"

:: ȥ���º��յ�ǰ���㣨����У�
set /a "month=1%month%-100"
set /a "day=1%day%-100"

:: ��ʼ����ʱ�ļ�
set "tempFile=temp.txt"

:: ��ջ򴴽���ʱ�ļ�
echo. > %tempFile%

:: ����д����ʱ�ļ�
echo # version_info.txt >> %tempFile%
echo VSVersionInfo( >> %tempFile%
echo   ffi=FixedFileInfo( >> %tempFile%
echo     filevers=(%year%, %month%, %day%, %revision%), >> %tempFile%
echo     prodvers=(%year%, %month%, %day%, %revision%), >> %tempFile%
echo     mask=0x3f, >> %tempFile%
echo     flags=0x0, >> %tempFile%
echo     OS=0x4, >> %tempFile%
echo     fileType=0x1, >> %tempFile%
echo     subtype=0x0, >> %tempFile%
echo     date=(0, 0) >> %tempFile%
echo   ), >> %tempFile%
echo   kids=[ >> %tempFile%
echo     StringFileInfo( >> %tempFile%
echo       [ >> %tempFile%
echo       StringTable( >> %tempFile%
echo         '040904B0', >> %tempFile%
echo         [StringStruct('ProductName', '%ProductName%'), >> %tempFile%
echo         StringStruct('ProductVersion', '%year%, %month%, %day%, %revision%'), >> %tempFile%
echo         StringStruct('InternalName', '%InternalName%'), >> %tempFile%
echo         StringStruct('CompanyName', 'ysht.me - %Comments%'), >> %tempFile%
echo         StringStruct('Comments', '%Comments%'), >> %tempFile%
echo         StringStruct('LegalCopyright', 'Apache-2.0 license - %Comments%'), >> %tempFile%
echo         ] >> %tempFile%
echo       ), >> %tempFile%
echo       ] >> %tempFile%
echo     ), >> %tempFile%
echo     VarFileInfo([VarStruct('Translation', [0x804, 1200])]) >> %tempFile%
echo   ] >> %tempFile%
echo ) >> %tempFile%

:: ����ʱ�ļ������ƶ������յ� version_info.txt
move /Y %tempFile% version_info.txt

:: ��������Ϣ
echo �汾��Ϣ�ѳɹ����ɡ�

::���±���
title "AutoPyInstaller����ʼ���"

:: �������Ŀ¼����������ڣ�
md build
:: ɾ�����Ŀ¼��ͬ�汾�ŵ��ļ���
rd /S /Q %~dp0\build\%versionFolder%

:: ɾ�����Ŀ¼�����Ĺ����ļ�
del /q %~dp0\build\heartbeat.spec
rd /S /Q %~dp0\build\build

:: ������Ŀ¼����ʼ���
cd /d %~dp0\build
pyinstaller --onefile --noconsole --version-file %~dp0\version_info.txt --add-data "%~dp0\config.Exsample.ini;." %~dp0\heartbeat.py

::���±���
title "AutoPyInstaller�������ϣ�����һЩ��β����"
:: ���ٴΣ�ɾ�����Ŀ¼��ͬ�汾�ŵ��ļ���
rd /S /Q %~dp0\build\%versionFolder%
:: ���ٴΣ�ɾ�����Ŀ¼�����Ĺ����ļ�
del /q %~dp0\build\heartbeat.spec
rd /S /Q %~dp0\build\build

:: �����ɴ����Ŀ¼�԰汾��������
rename dist %versionFolder%

:: �����Ҫһ�������ļ�
copy %~dp0\config.Exsample.ini %~dp0\build\%versionFolder%\
copy %~dp0\README.md %~dp0\build\%versionFolder%\