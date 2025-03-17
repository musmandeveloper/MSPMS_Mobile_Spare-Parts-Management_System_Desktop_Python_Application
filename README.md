

# Mobile Spare Parts Management System (MSPMS)


## 👋 Introduction:

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


## 📸 Screenshots:
Below are the following screenshots (SS) of the project:

Image 01 - Project Folder Structure: 
<center><img src="https://github.com/user-attachments/assets/29fa6803-4293-461c-a143-afbf54e3bd8f" alt="MSPMS-Project Folder Structure" /></center>

Image 02:

## 📸 Screenshots Gallery:
Below is the gallery/slider of the screenshots (SS) of the project:

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/29fa6803-4293-461c-a143-afbf54e3bd8f" alt="MSPMS-Project Folder Structure"  width='500' /></td>
    <td><img src="data:image/jpeg;base64,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"  width='200' /></td>
    <td><img src="https://github.com/user-attachments/assets/29fa6803-4293-461c-a143-afbf54e3bd8f" alt="MSPMS-Project Folder Structure"  width='500' /></td>
  </tr>
</table>

## 🎥 Videos:
Below are the videos of the project:

[Demo Video of MSPMS Project](https://github.com/user-attachments/assets/e653a4eb-aca6-4dd8-a0a9-87f2f55ae5e7)

## 🚀 Features:
The project have following features:

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


## 🔧 Technologies & Tools:
Following technologies and tools were used in this project:

1. Python:
Backbone of the application for developing the user interface, logic, and database interactions.

2. wkhtmltopdf:
Converts HTML templates into professional PDF reports.

3. SQLite DB Browser:
A user-friendly tool for managing and viewing local SQLite databases.

4. XAMPP phpMyAdmin:
A web-based tool for managing MySQL databases hosted locally or remotely.


## 🌐 Live Demo:
To get live demo, visit the below platform:




## 🛠️ Installation:
To download and install or customize follow below steps:

### Step 1: Download the project ###
1. Clone the repository to download project.

### Step 2: Create & Activate a Virtual Environment ###
1. Open your terminal or command prompt (CMD) in the project directory.
2. Run the following command to create a virtual environment:
   python -m venv venv
3. Activate this ceated virtual environment by following commnd in already opend CMD:
   venv\Scripts\activate

### Step 3: Install Required Packages ###
1. Create or If Already Created Run, a requirements.txt file in the project's root directory 
   with the following content (one package name per line):

   mysql-connector-python
   tk
   etc...

2. Run the following command to install these packages:
   pip install -r requirements.txt
   
### Step 4 : Install all required dependecies ###
Enusre you must have install these Prerequisites dependencies/softwares to install & run the project successfully:

#### 1. Install Python ####
1. Download and install Python from their original website:
   https://www.python.org/downloads/
2. Just Intall this software depedency in your pc any Local Disk you want. 
   But recommended is use default path of Local Disk C.
3. Install it for all users and Tick the add pip library during install.
4. NOTE: Must Check the box 'add to path' during installaton.

#### 2. Install PIP (Python Package Manager) ####
1. Ensure PIP is installed with Python for managing project dependencies.

#### 3. Install wkhtmltopdf (makes html template to a pdf report files) ####
1. Download the wkhtmltopdf spftware from their original website:
   https://wkhtmltopdf.org/
2. Intall this software depedency in the folder 'dependency' of project folder like this:
   Mobile Spare Parts Management System MSPMS/dependency/wkhtmltopdf


## 📄 Usage ##
Follow below insructions to use & run the project:

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

### Step 4: Default Login Credentials (Initial Dummy Data) ###

1. Admin
   Username: admin
   Password: Admin@123

2. Salesman
   Username: salesman
   Password: Salesman@123

### Note ###

1. Ensure Python and its libraries are correctly installed, as the application 
   will not function otherwise.
2. Follow the setup steps precisely to avoid errors.


## 💬 Contact:
You can contact me using below methods:

1. [Email - usmanedu8250998@gmail.com](mailto:usmanedu8250998@gmail.com)
2. [Linkedin - musmandeveloper](https://www.linkedin.com/in/musmandeveloper)
3. [GitHub - musmandeveloper](https://github.com/musmandeveloper)
4. [Portfolio Website - musmandeveloper.vercel.app](https://musmandeveloper.vercel.app)


## 👨‍💻 Contribution ##
We warmly welcome contributions to improve this project! If you discover any issues, have suggestions for enhancements, or would like to add new features, please follow the steps below to contribute:

### Step 1. Fork the Repository ###
Click the "Fork" button at the top-right corner of this repository to create your own copy.

### Step 2. Clone Your Fork ###
Clone your forked repository to your local machine using the following command:
**git clone https://github.com/<your-username>/<repository-name>.git**  

### Step 3. Create a New Branch ###
Create a branch for your changes to keep the main branch clean and organized. Use below command:
**git checkout -b <branch-name>**  

### Step 4. Make Your Changes ###
Improve the project by fixing bugs, adding new features, or refining the documentation.

### Step 5. Test Your Changes ###
Ensure your changes work as expected and don’t break existing functionality.

### Step 6. Commit Your Changes ###
Commit your changes with a descriptive message:
**git commit -m "Descriptive message about the changes" ** 

### Step 7. Push Your Changes ###
Push your changes to your forked repository:
**git push origin <branch-name>  **

### Step 8. Submit a Pull Request (PR) ###
Go to the original repository on GitHub and click on the “Pull Requests” tab.
Click “New Pull Request” and follow the instructions to submit your PR.
Ensure you describe the changes you made and why they improve the project.

Guidelines to be must followed during contribution:
1. Follow the project’s coding style and conventions.
2. Keep your changes focused and avoid unrelated updates.
3. Include clear and concise documentation for any new features.
4. Be respectful and constructive when discussing issues or reviewing PRs.

Your contributions make this project better and more impactful. Thank you for taking the time to contribute! 🙌


## 📜 License:
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute the code as per the terms of the license.

### What This Means for You ###

**1. Free Use:** You can use this project for personal or commercial purposes without restrictions.

**2. Modification and Distribution:** You are allowed to modify the code and distribute your versions, provided you include the original license.

**3. Attribution:** Kindly credit the original author by including a link to this repository or mentioning the project.

**4. No Warranty:** This software is provided "as is," without any warranty of any kind. Use it at your own risk.

### Full License Text ###
The complete license details can be found in the [LICENSE](LICENSE) file in the root of this repository.

### Contribution and Licensing ###
By contributing to this repository, you agree that your contributions will also be licensed under the MIT License.

   

