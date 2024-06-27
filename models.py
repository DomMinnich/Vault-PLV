# Dev Dominic Minnich 2024
# models.py

from datetime import datetime, timedelta

from wtforms import SelectField
from __init__ import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_theresa = db.Column(db.Boolean, nullable=False, default=False) # same as normal but can access repairs

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2:sha256")


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(150), nullable=False)
    asset_number = db.Column(db.String(150), nullable=False, unique=True)
    serial_number = db.Column(db.String(150), nullable=False, unique=True)
    manufacturer = db.Column(db.String(150), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    warranty_info = db.Column(db.String(300), nullable=True)
    assigned_user = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Available")

    logs = db.relationship("DeviceLog", cascade="all, delete-orphan", backref="device")


class Personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    laptop_username = db.Column(db.String(150), nullable=False)
    laptop_password = db.Column(db.String(150), nullable=False)
    microsoft_email = db.Column(db.String(150), nullable=False)
    microsoft_password = db.Column(db.String(150), nullable=False)
    google_email = db.Column(db.String(150), nullable=False)
    google_password = db.Column(db.String(150), nullable=False)
    clever_email = db.Column(db.String(150), nullable=False)
    clever_password = db.Column(db.String(150), nullable=False)
    powerschool_email = db.Column(db.String(150), nullable=False)
    powerschool_password = db.Column(db.String(150), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=True)
    powercord_id = db.Column(db.Integer, nullable=True)

    logs = db.relationship(
        "PersonnelLog", cascade="all, delete-orphan", backref="logged_personnel"
    )


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    laptop_username = db.Column(db.String(150), nullable=False)
    laptop_password = db.Column(db.String(150), nullable=False)
    microsoft_password = db.Column(db.String(150), nullable=False)
    google_password = db.Column(db.String(150), nullable=False)
    xmedius_password = db.Column(db.String(150), nullable=False)
    pin_code_number = db.Column(db.String(150), nullable=False)
    keri_card_number = db.Column(db.String(150), nullable=False)
    apple = db.Column(db.String(150), nullable=False)
    device_id = db.Column(db.String(150), nullable=False)
    powercord_id = db.Column(db.String(150), nullable=False)
    notes = db.Column(db.String(150), nullable=False)

    logs = db.relationship(
        "StaffLog", cascade="all, delete-orphan", backref="logged_staff"
    )


class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    original_damage = db.Column(db.Text, nullable=True)
    asset_id = db.Column(db.String(100), nullable=False)
    loaner_id = db.Column(db.String(100), nullable=True)
    loaner_damage = db.Column(db.Text, nullable=True)
    slip_picture = db.Column(db.String(120), nullable=True)
    original_computer_damage_picture = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="repair_pending")
    new_computer_asset_id = db.Column(db.String(100), nullable=True)
    new_computer_damages = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    logs = db.relationship(
        "RepairLog", cascade="all, delete-orphan", backref="logged_repair"
    )


class DeviceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    change_description = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() - timedelta(hours=4)
    )  # does not account for daylight savings
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user = db.relationship("User")


class PersonnelLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personnel_id = db.Column(db.Integer, db.ForeignKey("personnel.id"), nullable=False)
    change_description = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() - timedelta(hours=4)
    )  # does not account for daylight savings
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user = db.relationship("User")


class StaffLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)
    change_description = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() - timedelta(hours=4)
    )  # does not account for daylight savings
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user = db.relationship("User")


class RepairLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repair_id = db.Column(db.Integer, db.ForeignKey("repair.id"), nullable=False)
    change_description = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() - timedelta(hours=4)
    )  # does not account for daylight savings
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user = db.relationship("User")
