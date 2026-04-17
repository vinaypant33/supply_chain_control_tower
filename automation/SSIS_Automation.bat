@echo off
echo Starting SSIS Package Execution...

dtexec /FILE "C:\Users\vinay\Downloads\Data Analytics Projects Final Ones\Supply Chain Control Tower\supply_chain_control_tower\etl\ssis\packages\SSIS_Full_ETL_Pipeline.dtsx"

echo SSIS Package Completed
pause