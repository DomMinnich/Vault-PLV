# Vault
![1](https://github.com/DomMinnich/Vault-PLV/assets/113619219/a0ff1de3-3da8-402b-90b8-c3e69824810c)

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
![2](https://github.com/DomMinnich/Vault-PLV/assets/113619219/17f7fec3-3aab-4851-a425-8121d978d3f7)

## Login Page
The login page allows users to authenticate themselves to gain access to the system. Users need to provide their username and password.
![3](https://github.com/DomMinnich/Vault-PLV/assets/113619219/9d40b49d-28d7-42b6-8287-0621569eaf4e)

## Register Page
The register page is where new users can create an account. There are different types of registration codes to determine privilages and account types.
![4](https://github.com/DomMinnich/Vault-PLV/assets/113619219/6eae3889-b3d5-443c-bfee-ca32464330ea)

## Homepage
The homepage provides an overview of the system and quick access to various functionalities. 
![5](https://github.com/DomMinnich/Vault-PLV/assets/113619219/7130b11a-41dc-418b-920f-43de62ca6d95)

## Settings Page
The settings page allows users to view their account type and update their personal settings. Admins have additional privileges to manage user accounts, including viewing all registered users, updating user roles, and resetting passwords etc..
![6](https://github.com/DomMinnich/Vault-PLV/assets/113619219/92d50c13-52a2-4600-a284-2771dc13b068)

## Device Management
Device management allows users to add, update, and remove devices from the inventory. It includes functionalities to track device details, status, and device logs.
![7](https://github.com/DomMinnich/Vault-PLV/assets/113619219/5bc5c2d3-ae46-450a-8e26-d77d73b748de)

https://github.com/DomMinnich/Vault-PLV/assets/113619219/e9ed5ae3-9e89-491e-b1eb-90daa364f366

## Repair Management
The repair management section is dedicated to handling repair details of devices. Users can log repair requests, track the status of ongoing repairs, and view repair history. This section helps ensure timely maintenance and repair of devices in the inventory.
![20](https://github.com/DomMinnich/Vault-PLV/assets/113619219/760cb804-e57d-416a-9067-c0259acd290d)
![21](https://github.com/DomMinnich/Vault-PLV/assets/113619219/24a5fe34-1aed-4325-9c68-cb7982e89978)
![22](https://github.com/DomMinnich/Vault-PLV/assets/113619219/dc72b6fa-d560-4c61-b24d-487eb4fc41e0)

## Webfiles
The webfiles section is a custom file explorer that allows users to manage files within the `miniRoot` directory. Key features include:
- Right-click functionality for folder-specific actions like rename, add subfolder, download, and delete.
- Right-click functionality for files to download, delete, and move to the parent directory.
- Drag and drop box for adding files.
- Options to move folders and files to child directories.
![24](https://github.com/DomMinnich/Vault-PLV/assets/113619219/a4a6a50f-a6bd-48f4-a228-46d1aaadb4f8)
https://github.com/DomMinnich/Vault-PLV/assets/113619219/ae1c0c66-95a4-4849-b635-ebdaeaacd541

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

