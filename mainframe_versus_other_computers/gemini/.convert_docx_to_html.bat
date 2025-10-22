@echo on
"C:\Program Files\LibreOffice\program\swriter.exe" --headless --convert-to html --outdir ./gemini_html/ ./*.docx
@echo off
if not %errorlevel%==0 (
   echo Conversion docx to html failed with errorlevel %errorlevel%
   timeout /T -1
   exit /B %errorlevel%
)

@echo on
py .update_gemini_html.py
@echo off
if not %errorlevel%==0 (
   echo update_gemini_html failed with errorlevel %errorlevel%
   timeout /T -1
   exit /B %errorlevel%
)

@echo on
move ./*docx ./converted/.
@echo off
if not %errorlevel%==0 (
   echo move converted failed with errorlevel %errorlevel%
   timeout /T -1
   exit /B %errorlevel%
)

echo conversion successful
timeout /T -1
exit /B 0