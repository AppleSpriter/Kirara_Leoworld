if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~fnx0"" h",0)(window.close)&&exit
:begin
pythonw kirara_mean.py