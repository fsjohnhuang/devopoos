wmic ENVIRONMENT create name="DEVOPOOS_BAT",username="<system>",VariableValue="%~dp0bat"
wmic ENVIRONMENT set name="PATH",username="<system>",VariableValue="%Path%;%~dp0bat"
