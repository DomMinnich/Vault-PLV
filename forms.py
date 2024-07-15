# Dev Dominic Minnich 2024
# forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    DateField,
    SelectField,
    BooleanField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from models import User
from __init__ import db


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=6, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    registration_code = StringField("Registration Code", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=6, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class DeviceForm(FlaskForm):
    model_name = StringField("Type", validators=[DataRequired()])
    asset_number = StringField("Asset Number", validators=[DataRequired()])
    serial_number = StringField("Serial Number", validators=[DataRequired()])
    manufacturer = StringField("Manufacturer", validators=[DataRequired()])
    purchase_date = DateField(
        "Purchase Date", validators=[DataRequired()], format="%Y-%m-%d"
    )
    warranty_info = StringField("Warranty Information")
    assigned_user = StringField("Assigned User")
    status = SelectField(
        "Status",
        choices=[
            ("Available", "Available"),
            ("In Use", "In Use"),
            ("In Repair", "In Repair"),
        ],
    )
    submit = SubmitField("Submit")


class PersonnelForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    laptop_username = StringField("Laptop Username", validators=[DataRequired()])
    laptop_password = StringField("Laptop Password", validators=[DataRequired()])
    microsoft_email = StringField("Microsoft Email", validators=[DataRequired()])
    microsoft_password = StringField("Microsoft Password", validators=[DataRequired()])
    google_email = StringField("Google Email")
    google_password = StringField("Google Password")
    clever_email = StringField("Clever Email")
    clever_password = StringField("Clever Password")
    powerschool_email = StringField("Powerschool Email")
    powerschool_password = StringField("Powerschool Password")
    device_id = StringField("Device Asset")
    powercord_id = StringField("Power Cord ID")
    submit = SubmitField("Submit")


class StaffForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    laptop_username = StringField("Laptop Username", validators=[DataRequired()])
    laptop_password = StringField("Laptop Password", validators=[DataRequired()])
    microsoft_password = StringField("Microsoft Password", validators=[DataRequired()])
    google_password = StringField("Google Password", validators=[DataRequired()])
    xmedius_password = StringField("Xmedius Password", validators=[DataRequired()])
    pin_code_number = StringField("Pin Code Number", validators=[DataRequired()])
    keri_card_number = StringField("Keri Card Number", validators=[DataRequired()])
    apple = StringField("Apple", validators=[DataRequired()])
    device_id = StringField("PC Asset Number", validators=[DataRequired()])
    powercord_id = StringField("Power Cord Asset Number", validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class AddRepairForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    original_damage = TextAreaField('Original Damage')
    asset_id = StringField('Asset ID', validators=[DataRequired()])
    loaner_id = StringField('Loaner ID', default='')
    loaner_damage = TextAreaField('Loaner Damage', default='')
    slip_picture = FileField('Slip Picture', validators=[FileAllowed(['jpg', 'png'])])
    original_computer_damage_picture = FileField('Original Computer Damage Picture', validators=[FileAllowed(['jpg', 'png'])])
    status = SelectField('Status', choices=[('repair_pending', 'Repair Pending'), ('repair_inprogress', 'Repair In Progress'), ('repair_completed', 'Repair Completed'), ('repair_impossible', 'Repair Impossible')])
    new_computer = db.Column(db.String(50), nullable=True)  #doesn't get used
    new_computer_asset_id = StringField('New Computer Asset ID', default='')
    new_computer_damages = StringField('New Computer Damages', default='')
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Repair')

class EditRepairForm(AddRepairForm):
    submit = SubmitField('Update Repair')



class ImportDevicesForm(FlaskForm):
    file = FileField(
        "CSV File", validators=[FileRequired(), FileAllowed(["csv"], "CSV files only!")]
    )
    submit = SubmitField("Upload")


class ImportPersonnelForm(FlaskForm):
    file = FileField(
        "CSV File", validators=[FileRequired(), FileAllowed(["csv"], "CSV files only!")]
    )
    submit = SubmitField("Upload")


class ImportStaffForm(FlaskForm):
    file = FileField(
        "CSV File", validators=[FileRequired(), FileAllowed(["csv"], "CSV files only!")]
    )
    submit = SubmitField("Upload")


class UpdateAccountTypeForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    is_admin = BooleanField("Admin")
    submit = SubmitField("Update Account Type")


class DeleteAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Delete Account")


class PasswordResetForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password", validators=[DataRequired(), Length(min=6, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm New Password", validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField("Change Password")


class AdminPasswordResetForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password", validators=[DataRequired(), Length(min=6, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm New Password", validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField("Change Password")
