
# Mobile Spare Parts Management System (MSPMS) #


## Project Description ##

The Mobile Spare Parts Management System (MSPMS) is a versatile and robust desktop application 
tailored to streamline the management of spare parts inventory, user roles, and business transactions. 
Built with Python as the core programming language, SPMS integrates seamlessly with both local (SQLite) 
and online (MySQL) databases, ensuring flexibility and scalability for businesses of varying sizes. 
The system provides role-based access for administrators and sales personnel, making it a secure and 
efficient tool for day-to-day operations.

The application features advanced reporting capabilities, generating professional PDF reports using 
the wkhtmltopdf library. It also simplifies database management through tools like SQLite DB Browser 
for local database viewing and XAMPP phpMyAdmin for managing MySQL databases. With its modular design 
and interactive user interface, SPMS offers an intuitive and user-friendly experience for both 
technical and non-technical users.


## Project Structure & Screenshots ##

![Project Structure Image ](https://github.com/user-attachments/assets/29fa6803-4293-461c-a143-afbf54e3bd8f)


## Project Features ##

1. Database Management:
* Local database: SQLite for offline data storage.
* Online database: MySQL for remote and multi-user access.
* Use of SQLite DB Browser for viewing and managing SQLite databases.
* Integration with XAMPP phpMyAdmin for managing MySQL databases.

2. User Authentication and Authorization:
* Secure login and signup functionalities.
* Role-based access control (Admin and Salesman roles).
* Assign, manage, and modify user roles and permissions.

3. Inventory and Spare Parts Management:
* Add, edit, delete, and view spare parts records.
* Maintain accurate inventory levels.

4. Transaction Management:
* Record and update sales and purchase transactions.
* Track and view historical transaction logs.

5. Reporting and Documentation:
* Generate detailed PDF reports using wkhtmltopdf.
* Utilize pre-designed HTML templates for consistent and professional report formatting.

6. Interactive Dashboards:
* Admin Dashboard: Manage users, roles, permissions, and inventory.
* Salesman Dashboard: Manage sales-related activities and transactions.

7. Development Utilities:
* Batch file (run_app.bat) for quick setup and launch.
* Modular code structure for easy maintenance and scalability.


## Project Tools ##

1. Python:
Backbone of the application for developing the user interface, logic, and database interactions.

2. wkhtmltopdf:
Converts HTML templates into professional PDF reports.

3. SQLite DB Browser:
A user-friendly tool for managing and viewing local SQLite databases.

4. XAMPP phpMyAdmin:
A web-based tool for managing MySQL databases hosted locally or remotely.


## Prerequisites ##

### 1. Install Python ###
1. Download and install Python from their original website:
   https://www.python.org/downloads/
2. Just Intall this software depedency in your pc any Local Disk you want. 
   But recommended is use default path of Local Disk C.
3. Install it for all users and Tick the add pip library during install.
4. NOTE: Must Check the box 'add to path' during installaton.

### 2. Install PIP (Python Package Manager) ###
1. Ensure PIP is installed with Python for managing project dependencies.

### 3. Install wkhtmltopdf (makes html template to a pdf report files) ###
1. Download the wkhtmltopdf spftware from their original website:
   https://wkhtmltopdf.org/
2. Intall this software depedency in the folder 'dependency' of project folder like this:
   Mobile Spare Parts Management System MSPMS/dependency/wkhtmltopdf


## Setting Up the Project ##

### Step 1: Create & Activate a Virtual Environment ###
1. Open your terminal or command prompt (CMD) in the project directory.
2. Run the following command to create a virtual environment:
   python -m venv venv
3. Activate this ceated virtual environment by following commnd in already opend CMD:
   venv\Scripts\activate

### Step 2: Install Required Packages ###
1. Create or If Already Created Run, a requirements.txt file in the project's root directory 
   with the following content (one package name per line):
   mysql-connector-python
   tk
   etc...
2. Run the following command to install these packages:
   pip install -r requirements.txt


## Usage Instructions ##

### Step 1: Create Databases ###
1. Run the database.py file to set up databases.
2. It will create a local SQLite database in the local_database folder.
3. It will also create a MySQL database in your localhost's phpMyAdmin.

### Step 2: Insert Initial Data ###
1. (Optional but recommended for development and testing)
2. Add initial data to the databases as needed.

### Step 3: Start the Application ###
1. Run the application using the main.py file by using CMD command:
   python main.py
2. Alternatively, you can Run the batch file:
   run_with_batch.bat
3. Recommended method is Point 2 to run application.


## Login Credentials (Initial Dummy Data) ##

1. Admin
   Username: admin
   Password: Admin@123

2. Salesman
   Username: salesman
   Password: Salesman@123


## Note ##

1. Ensure Python and its libraries are correctly installed, as the application 
   will not function otherwise.
2. Follow the setup steps precisely to avoid errors.




