## Required packages
Python 3.13.2 
Selenium 4.29.0
Behave 1.2.6(BDD framework for python)

## How to run the tests???

- To run the test with the default input/output files(from the behave.ini file)
C:\Users\YS007\test> python -m behave .\feature\car_details_validate.feature

- To run the test to include user defined input/output files
python -m behave .\feature\car_details_validate.feature -D input_file="./car_input_1.txt" -D output_file="./car_output_1.txt"

## Logging???
- Behave framework allows to enable JSON output and also the framework by default provides the XML logging along with the debug logs.
refer ./reports for XML/debug logs
refer ./json.pretty.output for JSOM dump

## Notes 
- feature file resides in the /test/features/*
- python step definition file stays in the /test/steps/*
- /test/lib contains the helper files to run the suite
- environment.py is to define the fixtures for the suite.