# Vault
![Logo2](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/2ecf3cac-221b-4db0-b4a9-5885f2fc2cd6)

Vault (I nick-named FireFly) is an inventory management system designed to pull away from a very large Excel file that held all Student and Staff data which always got overwhelmed by many different local copies and update issues. 
Offers a sleek, user-friendly experience with a dark and red-themed GUI. All webpages are dynamic and work on mobile. The system allows for comprehensive management of devices, personnel, and repairs, along with file handling and custom settings.

## Section Links
- [Login Page](#login-page)
- [Register Page](#register-page)
- [Homepage](#homepage)
- [Settings Page](#settings-page)
- [Device Management](#device-management)
- [Repair Management](#repair-management)
- [Webfiles](#webfiles)
  # For detailed information on specific security features, refer to the sections below:
- [Configuration](#configuration-configpy)
- [Models](#models-modelspy)
- [Forms](#forms-formspy)
- [Routes](#routes-routespy)
- [Specific Security Implementations](#specific-security-implementations)

## OVERVIEW
- **User Management**: Classify users as normal users or admins during registration based on a unique registration code. 
- **Device Management**: Add, edit, view, and delete devices within the inventory.
- **Personnel Management**: Manage personnel details with the ability to add, edit, and view personnel information.
- **Repair Management**: Track and manage repair details for devices, including adding and editing repair records.
- **Settings Page**: Users can view their account type and admins can manage user accounts.
- **File Explorer**: A custom file explorer to manage files and folders with functionalities such as rename, add subfolder, delete, and drag-and-drop for file uploads.
- **Backup and Restore**: Maintain backups of the database for easy restoration.
- **Password Reset**: Functionality for users to reset their passwords and for admins to reset passwords for other users.

## Directory Structure
![image](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/b93c9e38-8356-4c2d-a109-21403aa6b8fa)

## Login Page
The login page allows users to authenticate themselves to gain access to the system. Users need to provide their username and password.
![image](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/e98834f5-03b0-4ff9-8c45-81b44f4fb4ed)

## Register Page
The register page is where new users can create an account. There are different types of registration codes to determine privilages and account types.
![image](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/6b11a006-3f41-4c0c-967b-66f7c66b39e6)

## Homepage
The homepage provides an overview of the system and quick access to various functionalities. 
![image](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/d34cab21-63f2-4a77-aa66-9ccfc58bbb36)

## Settings Page
The settings page allows users to view their account type and update their personal settings. Admins have additional privileges to manage user accounts, including viewing all registered users, updating user roles, and resetting passwords etc..
![image](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/e6b5e438-0281-40a8-a153-1fd017aa4404)

## Device Management
Device management allows users to add, update, and remove devices from the inventory. It includes functionalities to track device details, status, and device logs.
![image](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/5237e3fb-5772-4229-8f33-0526f665655c)
https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/2ac32dae-5de9-4c17-8dd6-d221341463b9

## Repair Management
The repair management section is dedicated to handling repair details of devices. Users can log repair requests, track the status of ongoing repairs, and view repair history. This section helps ensure timely maintenance and repair of devices in the inventory.
![image](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/1e20487e-8b7f-401e-93de-161656df80fd)
![image](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/3d98df16-9317-424a-9d80-92b1dd8c7bbd)
![image](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/c800b4be-df22-44b9-9e06-37b042b60181)

## Webfiles
The webfiles section is a custom file explorer that allows users to manage files within the `miniRoot` directory. Key features include:
- Right-click functionality for folder-specific actions like rename, add subfolder, download, and delete.
- Right-click functionality for files to download, delete, and move to the parent directory.
- Drag and drop box for adding files.
- Options to move folders and files to child directories.
![image](https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/25faf9c9-dcaa-4897-b775-b8115737c716)
https://github.com/DomMinnich/InventorySys_experimental/assets/113619219/1cb0eab2-38cc-4cf9-afe3-c96cb517e317

# For detailed information on specific security features, refer to the sections below:

- [Configuration](#configuration-configpy)
- [Models](#models-modelspy)
- [Forms](#forms-formspy)
- [Routes](#routes-routespy)
- [Specific Security Implementations](#specific-security-implementations)

## Security Features

### Configuration (`config.py`)
The configuration file typically contains important settings for the Flask application, such as secret keys, database URIs, and other configurations. Security aspects in this file include:
- **Secret Key**: Crucial for session management and preventing CSRF attacks.
- **Database URI**: Secure connection strings for database access.

### Models (`models.py`)
This file defines the database schema using SQLAlchemy, which provides an ORM layer to prevent SQL injection attacks. Security considerations here include:
- **Data Validation**: Ensuring that inputs are properly sanitized and validated.
- **Relationships and Constraints**: Properly defined relationships and constraints to maintain data integrity.

### Forms (`forms.py`)
This file handles the creation and validation of web forms using Flask-WTF. Key security aspects include:
- **CSRF Protection**: Enabled by default with Flask-WTF, protecting against Cross-Site Request Forgery attacks.
- **Input Validation**: Ensures that data submitted via forms is properly validated and sanitized.

### Routes (`routes.py`)
This file defines the URL routes and associated view functions. It contains several security measures:
- **Authentication and Authorization**: The use of `@login_required` decorator to ensure that certain routes can only be accessed by authenticated users.
- **Admin Checks**: Ensuring that certain actions can only be performed by admin users, as indicated by checks like `if not current_user.is_admin`.
- **File Handling**: Secure handling of file uploads and downloads, including path validation to prevent directory traversal attacks.

## Specific Security Implementations

1. **User Authentication and Authorization**:
   - Routes are protected with the `@login_required` decorator to ensure that only authenticated users can access them.
   - Additional checks are in place to ensure that only admin users can perform certain actions, such as deleting users or staff.

2. **CSRF Protection**:
   - Flask-WTF forms include CSRF tokens by default, protecting the application from CSRF attacks.

3. **Input Validation**:
   - Forms are validated using Flask-WTF, ensuring that data submitted by users is properly sanitized and validated before processing.

4. **Database Security**:
   - SQLAlchemy ORM is used to interact with the database, which helps prevent SQL injection attacks by using parameterized queries.
   - Proper schema definitions and relationships maintain data integrity.

5. **File Handling Security**:
   - Secure file handling mechanisms are in place, such as validating file paths with `is_safe_path` to prevent directory traversal attacks.
   - Uploaded files are handled carefully, with checks to ensure that only allowed file types are processed.

6. **Flash Messages**:
   - Use of flash messages for user feedback, which helps in preventing certain types of attacks like phishing by ensuring users are aware of actions taken.

