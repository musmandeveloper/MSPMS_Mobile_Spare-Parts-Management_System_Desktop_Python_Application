
README File of Project

NOTE: First of all you must install python and its librariries pip. 
      Otherwise you cannot run your project.



### Download and Install Python:

Download and install Python from website "https://python.org"



### Create a Virtual Environment inside Project Directory:
Open your terminal or command prompt (cmd) from project directory.


To Create a virtual environment type below command:
python -m venv venv

Now to Activate this created Virtual Environment, type below command:
venv\Scripts\activate



### Install the Required Packages:

First Create a requirements.txt file in home directory of project with the following content each package on new line like below:
mysql-connector-python
tk
etc

Install these mentioned packages useing below command in command prompt from project directory:
pip install -r requirements.txt





1. First of all create Databases you want. So run the database.py file.
   Which will create offline local SQLite database in folder 'local_database"
   and online MySQL database in the localhost phpmyadmin. 

2. Then insert the intial data into databases if you want (Must during development or testing stages)

3. Run your application main file, either directly by main.py file or using batch by run_with_batch.bat file


NOTE:

Intial Dummy Users to Login:

Admin:
username: admin
password: Admin@123

Salesman:
username: salesman
password: Salesman@123


