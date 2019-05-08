
Instructions Before Running Scripts:
- Before running "db_create.py" it assumed that "inspections.xlsx" 
  "violations.xlsx" are both located in a folder called "data" within
  the same directory as the "db_create.py" script.

- Script "db_create.py" MUST be run before any other script.

- Scripts can be run multiple times however they will delete the existing
  data and replace the files or database tables with the data set present
  at the time of running the scripts. 

Software Requirements:
- python3 must be installed on your machine to run the scripts. For 
  instructions on how to install python3 visit the python website at
  "https://www.python.org/".

- sqlite3 must be installed on your machine to run the scripts. For
  instructions on how to install sqlite3 visit the sqlite website at
  "https://www.sqlite.org/index.html". 

Package Requirements:
- python sqlite3 is required to run all scripts. To install python sqlite3 
  package enter "pip install pysqlite3" in the command line.
  
- openpyxl is required to run "db_create.py" and "excel_food.py". To
  install openpyxl eneter "pip install openpyxl" in the command line.

- numpy and matplotlib are both required to run "numpy_food.py". To install
  numpy run "pip install numpy" in the command line. To insall matplotlib
  run "pip install matplotlib" in the command line.