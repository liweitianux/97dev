@echo off

REM Launch Ruby Compass SASS Compiler
PUSHD %~dp0

PATH %PATH%;%RUBY%\..\
%RUBY%\..\compass watch

pause

