@echo off

SET LIB_NAME=tensorflow

SET CALL_DIR=%CD%
SET PROJECT_DIR=%~dp0..\tensorflow
SET OUTPUT_HEADER=%IGE_LIBS%\%LIB_NAME%

echo Fetching %LIB_NAME% headers...

if exist "%OUTPUT_HEADER%\include" (
	rmdir /s /q %OUTPUT_HEADER%\include
)
if not exist "%OUTPUT_HEADER%\include\tensorflow" (
    mkdir %OUTPUT_HEADER%\include\tensorflow
)

xcopy /q /s /y %PROJECT_DIR%\*.h?? %OUTPUT_HEADER%\include\tensorflow

cd %CALL_DIR%
echo Fetching %LIB_NAME% headers DONE!