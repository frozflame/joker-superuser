set "prefix=%~1"

if not exist "%prefix%" mkdir "%prefix%"
if not exist "%prefix%" exit

REM if exist "%userprofile%\Documents" robocopy "%userprofile%\Documents" "%prefix%\Documents" /E /XJ /MOVE
REM if not exist "%userprofile%\Documents" mklink /J "%userprofile%\Documents" "%prefix%\Documents"

for %%X in (Contacts Desktop Documents Downloads Favorites Links Music Pictures "Saved Games" Searches Videos) do (
    if exist "%userprofile%\%%~X" robocopy "%userprofile%\%%~X" "%prefix%\%%~X" /E /XJ /MOVE
    if not exist "%userprofile%\%%~X" mklink /J "%userprofile%\%%~X" "%prefix%\%%~X"
    )

REM pause

call :regadd_sf "{374DE290-123F-4565-9164-39C4925E467B}" Downloads
call :regadd_sf "{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}" "Saved Games"
call :regadd_sf "{56784854-C6CB-462B-8169-88E350ACB882}" Contacts
call :regadd_sf "{7D1D3A04-DEBB-4115-95CF-2F29DA2920DA}" Searches
call :regadd_sf "{BFB9D5E0-C6A9-404C-B2B2-AE6DB6AF4968}" Links
call :regadd_sf Desktop Desktop
call :regadd_sf Favorites Favorites
call :regadd_sf "My Music" Music
call :regadd_sf "My Pictures" Pictures
call :regadd_sf "My Video" Videos
call :regadd_sf Personal Documents

call :regadd_usf "{0DDD015D-B06C-45D5-8C4C-F59713854639}" "Pictures"
call :regadd_usf "{35286A68-3C57-41A1-BBB1-0EAE73D76C95}" "Videos"
call :regadd_usf "{374DE290-123F-4565-9164-39C4925E467B}" "Downloads"
call :regadd_usf "{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}" "Saved Games"
call :regadd_usf "{56784854-C6CB-462B-8169-88E350ACB882}" "Contacts"
call :regadd_usf "{754AC886-DF64-4CBA-86B5-F7FBF4FBCEF5}" "Desktop"
call :regadd_usf "{7D1D3A04-DEBB-4115-95CF-2F29DA2920DA}" "Searches"
call :regadd_usf "{7D83EE9B-2244-4E70-B1F5-5393042AF1E4}" "Downloads"
call :regadd_usf "{A0C69A99-21C8-4671-8703-7934162FCF1D}" "Music"
call :regadd_usf "{BFB9D5E0-C6A9-404C-B2B2-AE6DB6AF4968}" "Links"
call :regadd_usf "{F42EE2D3-909F-4907-8871-4C22FC0BF756}" "Documents"
call :regadd_usf "Desktop" "Desktop"
call :regadd_usf "Favorites" "Favorites"
call :regadd_usf "My Music" "Music"
call :regadd_usf "My Pictures" "Pictures"
call :regadd_usf "My Video" "Videos"
call :regadd_usf "Personal" "Documents"

REM pause

rmdir "%userprofile%\Documents\My Pictures"
rmdir "%userprofile%\Documents\My Videos"
rmdir "%userprofile%\Documents\My Music"
rmdir "%userprofile%\Documents"
mklink /J "%userprofile%\Documents" "%prefix%\Documents"

exit /b

:regadd_sf
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v "%~1" /t REG_EXPAND_SZ /d "%prefix%\%~2" /f
exit /b

:regadd_usf
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v "%~1" /t REG_EXPAND_SZ /d "%prefix%\%~2" /f
exit /b

