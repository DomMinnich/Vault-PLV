# Dev Dominic Minnich 2024
# routes.py


#||||||||||||||||||||||||||||||||||||||||||||||||

# Imports                   Line 15
# Blueprint                 Line 73
# Routes            A -> Z  Line 89
# Web File Explorer A -> Z  Line 1593


#|||||||||||||||||||||||||||||||||||||||||||||||||

# Imports 

import datetime
import secrets
import shutil
from PIL import Image
from docx import Document
from flask import (
    Blueprint,
    Response,
    abort,
    app,
    current_app,
    jsonify,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    send_from_directory,
    make_response,
    send_file,
)
from __init__ import db, login_manager
from models import (
    DeviceLog,
    Repair,
    RepairLog,
    User,
    Device,
    Personnel,
    PersonnelLog,
    Staff,
    StaffLog,
)
from forms import (
    AddRepairForm,
    EditRepairForm,
    RegistrationForm,
    LoginForm,
    DeviceForm,
    ImportDevicesForm,
    PersonnelForm,
    ImportPersonnelForm,
    UpdateAccountTypeForm,
    DeleteAccountForm,
    StaffForm,
    ImportStaffForm,
    PasswordResetForm,
    AdminPasswordResetForm,
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import csv
from io import BytesIO, StringIO

# Blueprint 

main = Blueprint("main", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    # Redirects user to login page if they try to access a page requiring login without being logged in
    return redirect(url_for("main.login"))



#________________________________
#       ROUTES A -> Z
#________________________________

@main.route("/")
def home():
    return redirect(url_for("main.login"))

@main.route("/add_device", methods=["GET", "POST"])
@login_required
def add_device():
    form = DeviceForm()
    if form.validate_on_submit():
        new_device = Device(
            model_name=form.model_name.data,
            asset_number=form.asset_number.data,
            serial_number=form.serial_number.data,
            manufacturer=form.manufacturer.data,
            purchase_date=form.purchase_date.data,
            warranty_info=form.warranty_info.data,
            assigned_user=form.assigned_user.data,
            status=form.status.data,
        )
        db.session.add(new_device)
        db.session.commit()
        flash("Device added successfully!", "success")
        return redirect(url_for("main.manage_devices"))
    return render_template("add_device.html", form=form)

@main.route("/add_personnel", methods=["GET", "POST"])
@login_required
def add_personnel():
    form = PersonnelForm()
    if form.validate_on_submit():
        new_personnel = Personnel(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            laptop_username=form.laptop_username.data,
            laptop_password=form.laptop_password.data,
            microsoft_email=form.microsoft_email.data,
            microsoft_password=form.microsoft_password.data,
            google_email=form.google_email.data,
            google_password=form.google_password.data,
            clever_email=form.clever_email.data,
            clever_password=form.clever_password.data,
            powerschool_email=form.powerschool_email.data,
            powerschool_password=form.powerschool_password.data,
            device_id=form.device_id.data,
            powercord_id=form.powercord_id.data,
        )
        db.session.add(new_personnel)
        db.session.commit()
        flash("Personnel added successfully!", "success")
        return redirect(url_for("main.manage_personnels"))
    return render_template("add_personnel.html", form=form)

@main.route("/add_staff", methods=["GET", "POST"])
@login_required
def add_staff():
    if not current_user.is_admin:
        return redirect(url_for("main.homepage"))

    form = StaffForm()
    if form.validate_on_submit():
        new_staff = Staff(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            title=form.title.data,
            laptop_username=form.laptop_username.data,
            laptop_password=form.laptop_password.data,
            microsoft_password=form.microsoft_password.data,
            google_password=form.google_password.data,
            xmedius_password=form.xmedius_password.data,
            pin_code_number=form.pin_code_number.data,
            keri_card_number=form.keri_card_number.data,
            apple=form.apple.data,
            device_id=form.device_id.data,
            powercord_id=form.powercord_id.data,
            notes=form.notes.data,
        )
        db.session.add(new_staff)
        db.session.commit()
        flash("Staff added successfully!", "success")
        return redirect(url_for("main.manage_staffs"))
    #   Debug condition
    #    else:
    #        print("Form did not validate.")
    #        print("Form errors:", form.errors)
    #        print("Form data:", form.data)
    return render_template("add_staff.html", form=form)

@main.route("/devices", methods=["GET"])
@login_required
def manage_devices():
    search_query = request.args.get("search", "")
    sort_by = request.args.get("sort_by", "model_name")
    status_filter = request.args.get("status", "")

    devices = Device.query

    if search_query:
        devices = devices.filter(
            (Device.model_name.ilike(f"%{search_query}%"))
            | (Device.asset_number.ilike(f"%{search_query}%"))
            | (Device.manufacturer.ilike(f"%{search_query}%"))
            | (Device.assigned_user.ilike(f"%{search_query}%"))
        )

    if status_filter:
        devices = devices.filter_by(status=status_filter)

    if sort_by:
        devices = devices.order_by(getattr(Device, sort_by))

    devices = devices.all()
    return render_template(
        "devices.html",
        devices=devices,
        search_query=search_query,
        sort_by=sort_by,
        status_filter=status_filter,
    )

@main.route("/delete_device/<int:device_id>", methods=["POST"])
@login_required
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    flash("Device deleted successfully!", "success")
    return redirect(url_for("main.manage_devices"))

@main.route("/delete_personnel/<int:personnel_id>", methods=["POST"])
@login_required
def delete_personnel(personnel_id):
    personnel = Personnel.query.get_or_404(personnel_id)

    # Delete associated logs and attachments first
    PersonnelLog.query.filter_by(personnel_id=personnel.id).delete()

    db.session.delete(personnel)
    db.session.commit()

    flash("Personnel deleted successfully!", "success")
    return redirect(url_for("main.manage_personnels"))

@main.route("/delete_staff/<int:staff_id>", methods=["POST"])
@login_required
def delete_staff(staff_id):
    if not current_user.is_admin:
        return redirect(url_for("main.homepage"))
    staff = Staff.query.get_or_404(staff_id)

    # Delete associated logs and attachments first
    StaffLog.query.filter_by(staff_id=staff.id).delete()

    db.session.delete(staff)
    db.session.commit()

    flash("Staff deleted successfully!", "success")
    return redirect(url_for("main.manage_staffs"))

@main.route("/devices/<int:device_id>", methods=["GET", "POST"])
@login_required
def device_detail(device_id):
    device = Device.query.get_or_404(device_id)
    form = DeviceForm(obj=device)

    if form.validate_on_submit():
        changes = []
        if device.model_name != form.model_name.data:
            changes.append(
                f"Type changed from {device.model_name} to {form.model_name.data}"
            )
            device.model_name = form.model_name.data
        if device.asset_number != form.asset_number.data:
            changes.append(
                f"Asset Number changed from {device.asset_number} to {form.asset_number.data}"
            )
            device.asset_number = form.asset_number.data

        if device.serial_number != form.serial_number.data:
            changes.append(
                f"Serial Number changed from {device.serial_number} to {form.serial_number.data}"
            )
            device.serial_number = form.serial_number.data
        if device.manufacturer != form.manufacturer.data:
            changes.append(
                f"Manufacturer changed from {device.manufacturer} to {form.manufacturer.data}"
            )
            device.manufacturer = form.manufacturer.data
        if device.purchase_date != form.purchase_date.data:
            changes.append(
                f"Purchase Date changed from {device.purchase_date} to {form.purchase_date.data}"
            )
            device.purchase_date = form.purchase_date.data
        if device.warranty_info != form.warranty_info.data:
            changes.append(
                f"Warranty Info changed from {device.warranty_info} to {form.warranty_info.data}"
            )
            device.warranty_info = form.warranty_info.data
        if device.assigned_user != form.assigned_user.data:
            changes.append(
                f"Assigned User changed from {device.assigned_user} to {form.assigned_user.data}"
            )
            device.assigned_user = form.assigned_user.data
        if device.status != form.status.data:
            changes.append(f"Status changed from {device.status} to {form.status.data}")
            device.status = form.status.data

        db.session.commit()

        for change in changes:
            log_entry = DeviceLog(
                device_id=device.id, change_description=change, user_id=current_user.id
            )
            db.session.add(log_entry)
        db.session.commit()

        flash("Device updated successfully!", "success")
        return redirect(url_for("main.device_detail", device_id=device.id))

    logs = DeviceLog.query.filter_by(device_id=device.id).all()
    return render_template(
        "device_detail.html",
        device=device,
        logs=logs,
        device_form=form,
    )

@main.route("/edit_device/<int:device_id>", methods=["GET", "POST"])
@login_required
def edit_device(device_id):
    device = Device.query.get_or_404(device_id)
    form = DeviceForm(obj=device)  # Ensure the form is populated with the device data

    if form.validate_on_submit():
        changes = []
        if device.model_name != form.model_name.data:
            changes.append(
                f"Type changed from {device.model_name} to {form.model_name.data}"
            )
            device.model_name = form.model_name.data
        if device.asset_number != form.asset_number.data:
            changes.append(
                f"Asset Number changed from {device.asset_number} to {form.asset_number.data}"
            )
            device.asset_number = form.asset_number.data
        if device.serial_number != form.serial_number.data:
            changes.append(
                f"Serial Number changed from {device.serial_number} to {form.serial_number.data}"
            )
            device.serial_number = form.serial_number.data
        if device.manufacturer != form.manufacturer.data:
            changes.append(
                f"Manufacturer changed from {device.manufacturer} to {form.manufacturer.data}"
            )
            device.manufacturer = form.manufacturer.data
        if device.purchase_date != form.purchase_date.data:
            changes.append(
                f"Purchase Date changed from {device.purchase_date} to {form.purchase_date.data}"
            )
            device.purchase_date = form.purchase_date.data
        if device.warranty_info != form.warranty_info.data:
            changes.append(
                f"Warranty Info changed from {device.warranty_info} to {form.warranty_info.data}"
            )
            device.warranty_info = form.warranty_info.data
        if device.assigned_user != form.assigned_user.data:
            changes.append(
                f"Assigned User changed from {device.assigned_user} to {form.assigned_user.data}"
            )
            device.assigned_user = form.assigned_user.data
        if device.status != form.status.data:
            changes.append(f"Status changed from {device.status} to {form.status.data}")
            device.status = form.status.data

        db.session.commit()

        for change in changes:
            log_entry = DeviceLog(
                device_id=device.id, change_description=change, user_id=current_user.id
            )
            db.session.add(log_entry)
        db.session.commit()

        flash("Device updated successfully!", "success")
        return redirect(url_for("main.device_detail", device_id=device.id))

    logs = DeviceLog.query.filter_by(device_id=device.id).all()  # Fetch device logs
    return render_template("edit_device.html", form=form, device=device, logs=logs)

@main.route("/edit_personnel/<int:personnel_id>", methods=["GET", "POST"])
@login_required
def edit_personnel(personnel_id):
    personnel = Personnel.query.get_or_404(personnel_id)
    form = PersonnelForm(obj=personnel)

    if form.validate_on_submit():
        changes2 = []
        if personnel.first_name != form.first_name.data:
            changes2.append(
                f"First Name changed from {personnel.first_name} to {form.first_name.data}"
            )
            personnel.first_name = form.first_name.data
        if personnel.last_name != form.last_name.data:
            changes2.append(
                f"Last Name changed from {personnel.last_name} to {form.last_name.data}"
            )
            personnel.last_name = form.last_name.data
        if personnel.laptop_username != form.laptop_username.data:
            changes2.append(
                f"Laptop Username changed from {personnel.laptop_username} to {form.laptop_username.data}"
            )
            personnel.laptop_username = form.laptop_username.data
        if personnel.laptop_password != form.laptop_password.data:
            changes2.append(
                f"Laptop Password changed from {personnel.laptop_password} to {form.laptop_password.data}"
            )
            personnel.laptop_password = form.laptop_password.data
        if personnel.microsoft_email != form.microsoft_email.data:
            changes2.append(
                f"Microsoft Email changed from {personnel.microsoft_email} to {form.microsoft_email.data}"
            )
            personnel.microsoft_email = form.microsoft_email.data
        if personnel.microsoft_password != form.microsoft_password.data:
            changes2.append(
                f"Microsoft Password changed from {personnel.microsoft_password} to {form.microsoft_password.data}"
            )
            personnel.microsoft_password = form.microsoft_password.data
        if personnel.google_email != form.google_email.data:
            changes2.append(
                f"Google Email changed from {personnel.google_email} to {form.google_email.data}"
            )
            personnel.google_email = form.google_email.data
        if personnel.google_password != form.google_password.data:
            changes2.append(
                f"Google Password changed from {personnel.google_password} to {form.google_password.data}"
            )
            personnel.google_password = form.google_password.data
        if personnel.clever_email != form.clever_email.data:
            changes2.append(
                f"Clever Email changed from {personnel.clever_email} to {form.clever_email.data}"
            )
            personnel.clever_email = form.clever_email.data
        if personnel.clever_password != form.clever_password.data:
            changes2.append(
                f"Clever Password changed from {personnel.clever_password} to {form.clever_password.data}"
            )
            personnel.clever_password = form.clever_password.data
        if personnel.powerschool_email != form.powerschool_email.data:
            changes2.append(
                f"Powerschool Email changed from {personnel.powerschool_email} to {form.powerschool_email.data}"
            )
            personnel.powerschool_email = form.powersch
        if personnel.powerschool_password != form.powerschool_password.data:
            changes2.append(
                f"Powerschool Password changed from {personnel.powerschool_password} to {form.powerschool_password.data}"
            )
            personnel.powerschool_password = form.powerschool_password.data
        if personnel.device_id != form.device_id.data:
            changes2.append(
                f"Device ID changed from {personnel.device_id} to {form.device_id.data}"
            )
            personnel.device_id = form.device_id.data
        if personnel.powercord_id != form.powercord_id.data:
            changes2.append(
                f"Powercord ID changed from {personnel.powercord_id} to {form.powercord_id.data}"
            )
            personnel.powercord_id = form.powercord_id.data

        db.session.commit()

        for change in changes2:
            log_entry = PersonnelLog(
                personnel_id=personnel.id,
                change_description=change,
                user_id=current_user.id,
            )
            db.session.add(log_entry)
        db.session.commit()

        flash("Personnel updated successfully!", "success")
        return redirect(url_for("main.personnel_detail", personnel_id=personnel.id))

    logs = PersonnelLog.query.filter_by(
        personnel_id=personnel.id
    ).all()  # Fetch personnel logs
    return render_template(
        "edit_personnel.html", form=form, personnel=personnel, logs=logs
    )

@main.route("/edit_staff/<int:staff_id>", methods=["GET", "POST"])
@login_required
def edit_staff(staff_id):
    if not current_user.is_admin:
        return redirect(url_for("main.homepage"))
    staff = Staff.query.get_or_404(staff_id)
    form = StaffForm(obj=staff)

    if form.validate_on_submit():
        changes2 = []
        if staff.first_name != form.first_name.data:
            changes2.append(
                f"First Name changed from {staff.first_name} to {form.first_name.data}"
            )
            staff.first_name = form.first_name.data
        if staff.last_name != form.last_name.data:
            changes2.append(
                f"Last Name changed from {staff.last_name} to {form.last_name.data}"
            )
            staff.last_name = form.last_name
        if staff.laptop_username != form.laptop_username.data:
            changes2.append(
                f"Laptop Username changed from {staff.laptop_username} to {form.laptop_username.data}"
            )
            staff.laptop_username = form.laptop_username.data
        if staff.laptop_password != form.laptop_password.data:
            changes2.append(
                f"Laptop Password changed from {staff.laptop_password} to {form.laptop_password.data}"
            )
            staff.laptop_password = form.laptop_password.data
        if staff.microsoft_password != form.microsoft_password.data:
            changes2.append(
                f"Microsoft Password changed from {staff.microsoft_password} to {form.microsoft_password.data}"
            )
            staff.microsoft_password = form.microsoft_password.data
        if staff.google_password != form.google_password.data:
            changes2.append(
                f"Google Password changed from {staff.google_password} to {form.google_password.data}"
            )
            staff.google_password = form.google_password.data
        if staff.xmedius_password != form.xmedius_password.data:
            changes2.append(
                f"Xmedius Password changed from {staff.xmedius_password} to {form.xmedius_password.data}"
            )
            staff.xmedius_password = form.xmedius_password.data
        if staff.pin_code_number != form.pin_code_number.data:
            changes2.append(
                f"Pin Code Number changed from {staff.pin_code_number} to {form.pin_code_number.data}"
            )
            staff.pin_code_number = form.pin_code_number.data
        if staff.keri_card_number != form.keri_card_number.data:
            changes2.append(
                f"Keri Card Number changed from {staff.keri_card_number} to {form.keri_card_number.data}"
            )
            staff.keri_card_number = form.keri_card_number.data
        if staff.apple != form.apple.data:
            changes2.append(f"Apple changed from {staff.apple} to {form.apple.data}")
            staff.apple = form.apple.data
        if staff.device_id != form.device_id.data:
            changes2.append(
                f"PC Asset Number changed from {staff.device_id} to {form.device_id.data}"
            )
            staff.device_id = form.device_id.data
        if staff.powercord_id != form.powercord_id.data:
            changes2.append(
                f"Powercord Asset Number changed from {staff.powercord_id} to {form.powercord_id.data}"
            )
            staff.powercord_id = form.powercord_id.data
        if staff.notes != form.notes.data:
            changes2.append(f"Notes changed from {staff.notes} to {form.notes.data}")
            staff.notes = form.notes.data

        db.session.commit()

        for change in changes2:
            log_entry = StaffLog(
                staff_id=staff.id,
                change_description=change,
                user_id=current_user.id,
            )
            db.session.add(log_entry)
        db.session.commit()

        flash("Staff updated successfully!", "success")
        return redirect(url_for("main.staff_detail", staff_id=staff.id))

    logs = StaffLog.query.filter_by(staff_id=staff.id).all()  # Fetch staff logs
    return render_template("edit_staff.html", form=form, staff=staff, logs=logs)

@main.route("/export_devices", methods=["GET"])
@login_required
def export_devices():
    si = StringIO()
    cw = csv.writer(si)
    devices = Device.query.all()
    cw.writerow(
        [
            "ID",
            "Type",
            "Asset Number",
            "Serial Number",
            "Manufacturer",
            "Purchase Date",
            "Warranty Information",
            "Assigned User",
            "Status",
        ]
    )
    for device in devices:
        cw.writerow(
            [
                device.id,
                device.model_name,
                device.asset_number,
                device.serial_number,
                device.manufacturer,
                device.purchase_date,
                device.warranty_info,
                device.assigned_user,
                device.status,
            ]
        )
    output = si.getvalue().encode("utf-8")
    return send_file(
        BytesIO(output),
        as_attachment=True,
        download_name="devices.csv",
        mimetype="text/csv",
    )

@main.route("/export_personnel", methods=["GET"])
@login_required
def export_personnel():
    si = StringIO()
    cw = csv.writer(si)
    personnel = Personnel.query.all()
    cw.writerow(
        [
            "ID",
            "First Name",
            "Last Name",
            "Laptop Username",
            "Laptop Password",
            "Microsoft Email",
            "Microsoft Password",
            "Google Email",
            "Google Password",
            "Clever Email",
            "Clever Password",
            "Powerschool Email",
            "Powerschool Password",
            "Device ID",
            "Powercord ID",
        ]
    )
    for p in personnel:
        cw.writerow(
            [
                p.id,
                p.first_name,
                p.last_name,
                p.laptop_username,
                p.laptop_password,
                p.microsoft_email,
                p.microsoft_password,
                p.google_email,
                p.google_password,
                p.clever_email,
                p.clever_password,
                p.powerschool_email,
                p.powerschool_password,
                p.device_id,
                p.powercord_id,
            ]
        )
    output = si.getvalue().encode("utf-8")
    return send_file(
        BytesIO(output),
        as_attachment=True,
        download_name="personnel.csv",
        mimetype="text/csv",
    )

@main.route("/export_staff", methods=["GET"])
@login_required
def export_staff():
    if not current_user.is_admin:
        return redirect(url_for("main.homepage"))
    si = StringIO()
    cw = csv.writer(si)
    staff = Staff.query.all()
    cw.writerow(
        [
            "ID",
            "First Name",
            "Last Name",
            "Title",
            "Laptop Username",
            "Laptop Password",
            "Microsoft Password",
            "Google Password",
            "XMedius Password",
            "Pin Code Number",
            "Keri Card Number",
            "Apple",
            "PC Asset Number",
            "Powercord Asset Number",
            "Notes",
        ]
    )
    for s in staff:
        cw.writerow(
            [
                s.id,
                s.first_name,
                s.last_name,
                s.title,
                s.laptop_username,
                s.laptop_password,
                s.microsoft_password,
                s.google_password,
                s.xmedius_password,
                s.pin_code_number,
                s.keri_card_number,
                s.apple,
                s.device_id,
                s.powercord_id,
                s.notes,
            ]
        )
    output = si.getvalue().encode("utf-8")
    return send_file(
        BytesIO(output),
        as_attachment=True,
        download_name="staff.csv",
        mimetype="text/csv",
    )

@main.route("/files/<filename>")
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@main.route("/homepage")
@login_required
def homepage():
    return render_template("homepage.html")

@main.route("/import_devices", methods=["GET", "POST"])
@login_required
def import_devices():
    form = ImportDevicesForm()  # Create an instance of the form
    if form.validate_on_submit():
        file = form.file.data  # Access the file field from the form
        if file and file.filename.endswith(".csv"):
            stream = StringIO(file.stream.read().decode("UTF-8", errors="ignore"))
            csv_input = csv.reader(stream)
            header = next(csv_input)  # Skip header row

            device_ids = set()
            asset_numbers = set()
            error_messages = []

            for row in csv_input:
                if len(row) != 9:
                    error_messages.append("Each row must have 9 fields.")
                    break

                try:
                    device_id = int(row[0])
                    if device_id in device_ids:
                        error_messages.append(f"Duplicate ID found: {device_id}")
                    device_ids.add(device_id)
                except ValueError:
                    error_messages.append(f"Invalid ID: {row[0]}")
                    continue

                if row[2] in asset_numbers:
                    error_messages.append(f"Duplicate Asset Number found: {row[2]}")
                asset_numbers.add(row[2])

                try:
                    purchase_date = datetime.datetime.strptime(row[5], "%m/%d/%Y")
                except ValueError:
                    error_messages.append(
                        f"Invalid date format for purchase date: {row[5]}, should be Month/Day/Year"
                    )
                    continue

            if error_messages:
                for error in error_messages:
                    flash(error, "danger")
            else:
                stream.seek(0)
                next(csv_input)  # Skip header row again
                for row in csv_input:
                    device_id = int(row[0])
                    device = Device.query.get(device_id)
                    if device:
                        # Update existing device
                        device.model_name = row[1]
                        device.asset_number = row[2]
                        device.serial_number = row[3]
                        device.manufacturer = row[4]
                        device.purchase_date = datetime.datetime.strptime(
                            row[5], "%m/%d/%Y"
                        )
                        device.warranty_info = row[6]
                        device.assigned_user = row[7]
                        device.status = row[8]
                    else:
                        # Add new device
                        new_device = Device(
                            id=device_id,
                            model_name=row[1],
                            asset_number=row[2],
                            serial_number=row[3],
                            manufacturer=row[4],
                            purchase_date=datetime.datetime.strptime(
                                row[5], "%m/%d/%Y"
                            ),
                            warranty_info=row[6],
                            assigned_user=row[7],
                            status=row[8],
                        )
                        db.session.add(new_device)
                db.session.commit()
                flash("Devices imported successfully!", "success")
        else:
            flash("Invalid file format. Please upload a CSV file.", "danger")
    return render_template("import_devices.html", form=form)

@main.route("/import_personnel", methods=["GET", "POST"])
@login_required
def import_personnel():
    form = ImportPersonnelForm()  # Create an instance of the form
    if form.validate_on_submit():
        file = form.file.data  # Access the file field from the form
        if file and file.filename.endswith(".csv"):
            stream = StringIO(file.stream.read().decode("UTF-8", errors="ignore"))
            csv_input = csv.reader(stream)
            header = next(csv_input)  # Skip header row

            personnel_ids = set()
            error_messages = []

            for row in csv_input:
                if len(row) != 15:
                    error_messages.append("Each row must have 15 fields.")
                    break

                try:
                    personnel_id = int(row[0])
                    if personnel_id in personnel_ids:
                        error_messages.append(f"Duplicate ID found: {personnel_id}")
                    personnel_ids.add(personnel_id)
                except ValueError:
                    error_messages.append(f"Invalid ID: {row[0]}")
                    continue

            if error_messages:
                for error in error_messages:
                    flash(error, "danger")
            else:
                stream.seek(0)
                next(csv_input)  # Skip header row again
                for row in csv_input:
                    personnel_id = int(row[0])
                    personnel = Personnel.query.get(personnel_id)
                    if personnel:
                        # Update existing personnel
                        personnel.first_name = row[1]
                        personnel.last_name = row[2]
                        personnel.laptop_username = row[3]
                        personnel.laptop_password = row[4]
                        personnel.microsoft_email = row[5]
                        personnel.microsoft_password = row[6]
                        personnel.google_email = row[7]
                        personnel.google_password = row[8]
                        personnel.clever_email = row[9]
                        personnel.clever_password = row[10]
                        personnel.powerschool_email = row[11]
                        personnel.powerschool_password = row[12]
                        personnel.device_id = int(row[13]) if row[13] else None
                        personnel.powercord_id = int(row[14]) if row[14] else None
                    else:
                        # Add new personnel
                        new_personnel = Personnel(
                            id=personnel_id,
                            first_name=row[1],
                            last_name=row[2],
                            laptop_username=row[3],
                            laptop_password=row[4],
                            microsoft_email=row[5],
                            microsoft_password=row[6],
                            google_email=row[7],
                            google_password=row[8],
                            clever_email=row[9],
                            clever_password=row[10],
                            powerschool_email=row[11],
                            powerschool_password=row[12],
                            device_id=int(row[13]) if row[13] else None,
                            powercord_id=int(row[14]) if row[14] else None,
                        )
                        db.session.add(new_personnel)
                db.session.commit()
                flash("Students imported successfully!", "success")
        else:
            flash("Invalid file format. Please upload a CSV file.", "danger")
    return render_template("import_personnel.html", form=form)

@main.route("/import_staff", methods=["GET", "POST"])
@login_required
def import_staff():
    if not current_user.is_admin:
        return redirect(url_for("main.homepage"))
    form = ImportStaffForm()  # Create an instance of the form
    if form.validate_on_submit():
        file = form.file.data  # Access the file field from the form
        if file and file.filename.endswith(".csv"):
            stream = StringIO(file.stream.read().decode("UTF-8", errors="ignore"))
            csv_input = csv.reader(stream)
            header = next(csv_input)  # Skip header row

            staff_ids = set()
            error_messages = []

            for row in csv_input:
                if len(row) != 15:
                    error_messages.append("Each row must have 10 fields.")
                    break

                try:
                    staff_id = int(row[0])
                    if staff_id in staff_ids:
                        error_messages.append(f"Duplicate ID found: {staff_id}")
                    staff_ids.add(staff_id)
                except ValueError:
                    error_messages.append(f"Invalid ID: {row[0]}")
                    continue

            if error_messages:
                for error in error_messages:
                    flash(error, "danger")
            else:
                stream.seek(0)
                next(csv_input)  # Skip header row again
                for row in csv_input:
                    staff_id = int(row[0])
                    staff = Staff.query.get(staff_id)
                    if staff:
                        # Update existing staff
                        staff.first_name = row[1]
                        staff.last_name = row[2]
                        staff.title = row[3]
                        staff.laptop_username = row[4]
                        staff.laptop_password = row[5]
                        staff.microsoft_password = row[6]
                        staff.google_password = row[7]
                        staff.xmedius_password = row[8]
                        staff.pin_code_number = row[9]
                        staff.keri_card_number = row[10]
                        staff.apple = row[11]
                        staff.device_id = row[12]
                        staff.powercord_id = row[13]
                        staff.notes = row[14]
                    else:
                        # Add new staff
                        new_staff = Staff(
                            id=staff_id,
                            first_name=row[1],
                            last_name=row[2],
                            title=row[3],
                            laptop_username=row[4],
                            laptop_password=row[5],
                            microsoft_password=row[6],
                            google_password=row[7],
                            xmedius_password=row[8],
                            pin_code_number=row[9],
                            keri_card_number=row[10],
                            apple=row[11],
                            device_id=row[12],
                            powercord_id=row[13],
                            notes=row[14],
                        )
                        db.session.add(new_staff)
                db.session.commit()
                flash("Staff imported successfully!", "success")
        else:
            flash("Invalid file format. Please upload a CSV file.", "danger")
    return render_template("import_staff.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            # redirect to homepage
            return redirect(url_for("main.homepage"))
        else:
            flash("Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/personnels", methods=["GET"])
@login_required
def manage_personnels():
    search_query = request.args.get("search", "")
    sort_by = request.args.get("sort_by", "first_name")
    status_filter = request.args.get("status", "")
    personnels = Personnel.query
    if search_query:
        personnels = personnels.filter(
            (Personnel.first_name.ilike(f"%{search_query}%"))
            | (Personnel.last_name.ilike(f"%{search_query}%"))
            | (Personnel.laptop_username.ilike(f"%{search_query}%"))
            | (Personnel.laptop_password.ilike(f"%{search_query}%"))
            | (Personnel.microsoft_email.ilike(f"%{search_query}%"))
        )
    if status_filter:
        personnels = personnels.filter_by(status=status_filter)
    if sort_by:
        personnels = personnels.order_by(getattr(Personnel, sort_by))
    personnels = personnels.all()
    return render_template(
        "personnels.html",
        personnels=personnels,
        search_query=search_query,
        sort_by=sort_by,
        status_filter=status_filter,
    )

    # staff , only accessable if admin level status

@main.route("/personnels/<int:personnel_id>", methods=["GET", "POST"])
@login_required
def personnel_detail(personnel_id):
    personnel = Personnel.query.get_or_404(personnel_id)
    form = PersonnelForm(obj=personnel)

    if form.validate_on_submit():
        changes = []
        if personnel.first_name != form.first_name.data:
            changes.append(
                f"First Name changed from {personnel.first_name} to {form.first_name.data}"
            )
            personnel.first_name = form.first_name.data
        if personnel.last_name != form.last_name.data:
            changes.append(
                f"Last Name changed from {personnel.last_name} to {form.last_name.data}"
            )
            personnel.last_name = form.last_name.data
        if personnel.laptop_username != form.laptop_username.data:
            changes.append(
                f"Laptop Username changed from {personnel.laptop_username} to {form.laptop_username.data}"
            )
            personnel.laptop_username = form.laptop_username.data
        if personnel.laptop_password != form.laptop_password.data:
            changes.append(
                f"Laptop Password changed from {personnel.laptop_password} to {form.laptop_password.data}"
            )
            personnel.laptop_password = form.laptop_password.data
        if personnel.microsoft_email != form.microsoft_email.data:
            changes.append(
                f"Microsoft Email changed from {personnel.microsoft_email} to {form.microsoft_email.data}"
            )
            personnel.microsoft_email = form.microsoft_email.data
        if personnel.microsoft_password != form.microsoft_password.data:
            changes.append(
                f"Microsoft Password changed from {personnel.microsoft_password} to {form.microsoft_password.data}"
            )
            personnel.microsoft_password = form.microsoft_password.data
        if personnel.google_email != form.google_email.data:
            changes.append(
                f"Google Email changed from {personnel.google_email} to {form.google_email.data}"
            )
            personnel.google_email = form.google_email.data
        if personnel.google_password != form.google_password.data:
            changes.append(
                f"Google Password changed from {personnel.google_password} to {form.google_password.data}"
            )
            personnel.google_password = form.google_password.data
        if personnel.clever_email != form.clever_email.data:
            changes.append(
                f"Clever Email changed from {personnel.clever_email} to {form.clever_email.data}"
            )
            personnel.clever_email = form.clever_email.data
        if personnel.clever_password != form.clever_password.data:
            changes.append(
                f"Clever Password changed from {personnel.clever_password} to {form.clever_password.data}"
            )
            personnel.clever_password = form.clever_password.data
        if personnel.powercord_email != form.powercord_email.data:
            changes.append(
                f"Powercord Email changed from {personnel.powercord_email} to {form.powercord_email.data}"
            )
            personnel.powercord_email = form.powercord_email.data
        if personnel.powercord_password != form.powercord_password.data:
            changes.append(
                f"Powercord Password changed from {personnel.powercord_password} to {form.powercord_password.data}"
            )
            personnel.powercord_password = form.powercord_password.data
        if personnel.device_id != form.device_id.data:
            changes.append(
                f"Device ID changed from {personnel.device_id} to {form.device_id.data}"
            )
            personnel.device_id = form.device_id.data
        if personnel.powercord_id != form.powercord_id.data:
            changes.append(
                f"Powercord ID changed from {personnel.powercord_id} to {form.powercord_id.data}"
            )
            personnel.powercord_id = form.powercord_id.data

        db.session.commit()

        for change in changes:
            log_entry = PersonnelLog(
                personnel_id=personnel.id,
                change_description=change,
                user_id=current_user.id,
            )
            db.session.add(log_entry)
        db.session.commit()

        flash("Personnel updated successfully!", "success")
        return render_template(
            "personnel_detail.html",
            personnel=personnel,
            personnel_form=form,
        )

    logs = PersonnelLog.query.filter_by(personnel_id=personnel.id).all()
    return render_template(
        "personnel_detail.html",
        personnel=personnel,
        logs=logs,
        personnel_form=form,
    )

@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for("main.register"))

        auth_code = form.registration_code.data
        if auth_code == "4f837hwek":
            is_admin = False
            is_theresa = False
        elif auth_code == "20f3hkskw":
            is_admin = True
            is_theresa = True
        elif auth_code == "pe9iv3nrf":
            is_admin = False
            is_theresa = True
        else:
            flash("Invalid authorization code", "danger")
            return redirect(url_for("main.register"))

        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256")
        user = User(
            username=form.username.data,
            password=hashed_password,
            is_admin=is_admin,
            is_theresa=is_theresa
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", title="Register", form=form)

@main.route("/repairs")
@login_required
def manage_repairs():
    repairs = Repair.query.all()
    return render_template("repairs.html", repairs=repairs)

@main.route("/repair/add", methods=["GET", "POST"])
@login_required
def add_repair():
    form = AddRepairForm()
    if form.validate_on_submit():
        slip_picture = None
        if form.slip_picture.data:
            slip_picture = save_picture(form.slip_picture.data, "slips")
        original_computer_damage_picture = None
        if form.original_computer_damage_picture.data:
            original_computer_damage_picture = save_picture(
                form.original_computer_damage_picture.data, "damage"
            )

        repair = Repair(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            original_damage=form.original_damage.data,
            asset_id=form.asset_id.data,
            loaner_id=form.loaner_id.data,
            loaner_damage=form.loaner_damage.data,
            slip_picture=slip_picture,
            original_computer_damage_picture=original_computer_damage_picture,
            status=form.status.data,
            new_computer_asset_id=form.new_computer_asset_id.data,
            new_computer_damages=form.new_computer_damages.data,
            notes=form.notes.data,
        )
        db.session.add(repair)
        db.session.commit()
        flash("Repair added successfully", "success")
        return redirect(url_for("main.manage_repairs"))
    return render_template("add_repair.html", form=form)

@main.route("/repair/<int:repair_id>/edit", methods=["GET", "POST"])
@login_required
def edit_repair(repair_id):
    repair = Repair.query.get_or_404(repair_id)
    form = EditRepairForm(obj=repair)
    
    if form.validate_on_submit():
        changes=[]
        
        if repair.first_name != form.first_name.data:
            changes.append(f"First Name changed from {repair.first_name} to {form.first_name.data}")
            repair.first_name = form.first_name.data
        if repair.last_name != form.last_name.data:
            changes.append(f"Last Name changed from {repair.last_name} to {form.last_name.data}")
            repair.last_name = form.last_name.data
        if repair.asset_id != form.asset_id.data:
            changes.append(f"Asset ID changed from {repair.asset_id} to {form.asset_id.data}")
            repair.asset_id = form.asset_id.data
        if repair.loaner_id != form.loaner_id.data:
            changes.append(f"Loaner ID changed from {repair.loaner_id} to {form.loaner_id.data}")
            repair.loaner_id = form.loaner_id.data
        if repair.loaner_damage != form.loaner_damage.data:
                changes.append(f"Loaner Damage changed from {repair.loaner_damage} to {form.loaner_damage.data}")
                repair.loaner_damage = form.loaner_damage.data
        if form.slip_picture.data:
                repair.slip_picture = save_picture(form.slip_picture.data, "slips")
        elif not form.slip_picture.data and repair.slip_picture:
            pass
        else:
            repair.slip_picture = None
        if form.original_computer_damage_picture.data:
                    repair.original_computer_damage_picture = save_picture(
                        form.original_computer_damage_picture.data, "damage"
                    )
        elif (
            not form.original_computer_damage_picture.data
            and repair.original_computer_damage_picture
        ):
            pass
        else:
                    repair.original_computer_damage_picture = None
        if repair.status != form.status.data:
            changes.append(f"Status changed from {repair.status} to {form.status.data}")
            repair.status = form.status.data
        if repair.new_computer_asset_id != form.new_computer_asset_id.data:
            changes.append(f"New Computer Asset ID changed from {repair.new_computer_asset_id} to {form.new_computer_asset_id.data}")
            repair.new_computer_asset_id = form.new_computer_asset_id.data
        if repair.new_computer_damages != form.new_computer_damages.data:
                changes.append(f"New Computer Damages changed from {repair.new_computer_damages} to {form.new_computer_damages.data}")
                repair.new_computer_damages = form.new_computer_damages.data
        if form.notes.data != repair.notes:
            changes.append(f"Notes changed from {repair.notes} to {form.notes.data}")
            repair.notes = form.notes.data

        db.session.commit()
        
        for change in changes:
            log_entry = RepairLog(
                repair_id=repair.id, change_description=change, user_id=current_user.id
            )
            db.session.add(log_entry)
        db.session.commit()
        
        flash("Repair updated successfully", "success")
        return redirect(url_for("main.manage_repairs"))
    
      
        repair.first_name = form.first_name.data
        repair.last_name = form.last_name.data
        repair.original_damage = form.original_damage.data
        repair.asset_id = form.asset_id.data
        repair.loaner_id = form.loaner_id.data
        repair.loaner_damage = form.loaner_damage.data
        if form.slip_picture.data:
            repair.slip_picture = save_picture(form.slip_picture.data, "slips")
        elif not form.slip_picture.data and repair.slip_picture:
            pass
        else:
            repair.slip_picture = None
        if form.original_computer_damage_picture.data:
            repair.original_computer_damage_picture = save_picture(
                form.original_computer_damage_picture.data, "damage"
            )
        elif (
            not form.original_computer_damage_picture.data
            and repair.original_computer_damage_picture
        ):
            pass
        else:
            repair.original_computer_damage_picture = None
        repair.status = form.status.data
        repair.new_computer_asset_id = form.new_computer_asset_id.data
        repair.new_computer_damages = form.new_computer_damages.data
        repair.notes = form.notes.data
        db.session.commit()
        flash("Repair updated successfully", "success")
        #/repair/<int:repair_id>/detail"
        return redirect(url_for("main.repair_detail", repair_id=repair.id))

    logs = RepairLog.query.filter_by(repair_id=repair.id).all()
    return render_template("edit_repair.html", form=form, repair=repair, logs=logs)

def save_picture(form_picture, folder):
    if isinstance(form_picture, str):
        return form_picture

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static", folder, picture_fn)

    with Image.open(form_picture) as img:
        img.save(picture_path)
    return picture_fn

@main.route("/repair/<int:repair_id>/detail")
@login_required
def repair_detail(repair_id):
    repair = Repair.query.get_or_404(repair_id)
    form = EditRepairForm(obj=repair)
    
    if form.validate_on_submit():
        changes=[]
        
        if repair.first_name != form.first_name.data:
            changes.append(f"First Name changed from {repair.first_name} to {form.first_name.data}")
            repair.first_name = form.first_name.data
        if repair.last_name != form.last_name.data:
            changes.append(f"Last Name changed from {repair.last_name} to {form.last_name.data}")
            repair.last_name = form.last_name.data
        if repair.asset_id != form.asset_id.data:
            changes.append(f"Asset ID changed from {repair.asset_id} to {form.asset_id.data}")
            repair.asset_id = form.asset_id.data
        if repair.loaner_id != form.loaner_id.data:
            changes.append(f"Loaner ID changed from {repair.loaner_id} to {form.loaner_id.data}")
            repair.loaner_id = form.loaner_id.data
        if repair.loaner_damage != form.loaner_damage.data:
                changes.append(f"Loaner Damage changed from {repair.loaner_damage} to {form.loaner_damage.data}")
                repair.loaner_damage = form.loaner_damage.data
        if form.slip_picture.data:
                repair.slip_picture = save_picture(form.slip_picture.data, "slips")
        elif not form.slip_picture.data and repair.slip_picture:
            pass
        else:
            repair.slip_picture = None
        if form.original_computer_damage_picture.data:
                    repair.original_computer_damage_picture = save_picture(
                        form.original_computer_damage_picture.data, "damage"
                    )
        elif (
            not form.original_computer_damage_picture.data
            and repair.original_computer_damage_picture
        ):
            pass
        else:
                    repair.original_computer_damage_picture = None
        if repair.status != form.status.data:
            changes.append(f"Status changed from {repair.status} to {form.status.data}")
            repair.status = form.status.data
        if repair.new_computer_asset_id != form.new_computer_asset_id.data:
            changes.append(f"New Computer Asset ID changed from {repair.new_computer_asset_id} to {form.new_computer_asset_id.data}")
            repair.new_computer_asset_id = form.new_computer_asset_id.data
        if repair.new_computer_damages != form.new_computer_damages.data:
                changes.append(f"New Computer Damages changed from {repair.new_computer_damages} to {form.new_computer_damages.data}")
                repair.new_computer_damages = form.new_computer_damages.data
        if form.notes.data != repair.notes:
            changes.append(f"Notes changed from {repair.notes} to {form.notes.data}")
            repair.notes = form.notes.data

        db.session.commit()
        
        for change in changes:
            log_entry = RepairLog(
                repair_id=repair.id, change_description=change, user_id=current_user.id
            )
            db.session.add(log_entry)
        db.session.commit()
        
        flash("Repair updated successfully", "success")
        return render_template("repair_details.html", repair=repair, repair_form=form)
    

    logs = RepairLog.query.filter_by(repair_id=repair.id).all()
    return render_template("repair_details.html", repair_form=form, repair=repair, logs=logs)
    
@main.route("/repair/<int:repair_id>/delete", methods=["POST"])
@login_required
def delete_repair(repair_id):
    if not current_user.is_admin:
        return redirect(url_for("main.homepage"))
    repair = Repair.query.get_or_404(repair_id)
    db.session.delete(repair)
    db.session.commit()
    flash("Repair deleted successfully", "success")
    return redirect(url_for("main.manage_repairs"))

@main.route("/staffs", methods=["GET"])
@login_required
def manage_staffs():
    if not current_user.is_admin:
        return redirect(url_for("main.homepage"))
    search_query = request.args.get("search", "")
    sort_by = request.args.get("sort_by", "first_name")
    status_filter = request.args.get("status", "")
    staffs = Staff.query
    if search_query:
        staffs = staffs.filter(
            (Staff.first_name.ilike(f"%{search_query}%"))
            | (Staff.last_name.ilike(f"%{search_query}%"))
            | (Staff.laptop_username.ilike(f"%{search_query}%"))
            | (Staff.laptop_password.ilike(f"%{search_query}%"))
            | (Staff.microsoft_password.ilike(f"%{search_query}%"))
            | (Staff.pin_code_number.ilike(f"%{search_query}%"))
            | (Staff.device_id.ilike(f"%{search_query}%"))
            | (Staff.powercord_id.ilike(f"%{search_query}%"))
        )
    if status_filter:
        staffs = staffs.filter_by(status=status_filter)
    if sort_by:
        staffs = staffs.order_by(getattr(Staff, sort_by))
    staffs = staffs.all()
    return render_template(
        "staffs.html",
        staffs=staffs,
        search_query=search_query,
        sort_by=sort_by,
        status_filter=status_filter,
    )

@main.route("/staffs/<int:staff_id>", methods=["GET", "POST"])
@login_required
def staff_detail(staff_id):
    if not current_user.is_admin:
        return redirect(url_for("main.homepage"))
    staff = Staff.query.get_or_404(staff_id)
    form = StaffForm(obj=staff)

    if form.validate_on_submit():
        changes = []
        if staff.first_name != form.first_name.data:
            changes.append(
                f"First name changed from {staff.first_name} to {form.first_name.data}"
            )
            staff.first_name = form.first_name.data
        if staff.last_name != form.last_name.data:
            changes.append(
                f"Last name changed from {staff.last_name} to {form.last_name.data}"
            )
            staff.last_name = form.last_name.data
        if staff.title != form.title.data:
            changes.append(f"Title changed from {staff.title} to {form.title.data}")
            staff.title = form.title.data
        if staff.laptop_username != form.laptop_username.data:
            changes.append(
                f"Laptop username changed from {staff.laptop_username} to {form.laptop_username.data}"
            )
            staff.laptop_username = form.laptop_username.data
        if staff.laptop_password != form.laptop_password.data:
            changes.append(
                f"Laptop password changed from {staff.laptop_password} to {form.laptop_password.data}"
            )
            staff.laptop_password = form.laptop_password.data
        if staff.microsoft_password != form.microsoft_password.data:
            changes.append(
                f"Microsoft password changed from {staff.microsoft_password} to {form.microsoft_password.data}"
            )
            staff.microsoft_password = form.microsoft_password.data
        if staff.google_password != form.google_password.data:
            changes.append(
                f"Google password changed from {staff.google_password} to {form.google_password.data}"
            )
            staff.google_password = form.google_password.data
        if staff.xmedius_password != form.xmedius_password.data:
            changes.append(
                f"Xmedius password changed from {staff.xmedius_password} to {form.xmedius_password.data}"
            )
            staff.xmedius_password = form.xmedius_password.data
        if staff.pin_code_number != form.pin_code_number.data:
            changes.append(
                f"Pin code number changed from {staff.pin_code_number} to {form.pin_code_number.data}"
            )
            staff.pin_code_number = form.pin_code_number.data
        if staff.keri_card_number != form.keri_card_number.data:
            changes.append(
                f"Keri card number changed from {staff.keri_card_number} to {form.keri_card_number.data}"
            )
            staff.keri_card_number = form.keri_card_number.data
        if staff.apple != form.apple.data:
            changes.append(f"Apple changed from {staff.apple} to {form.apple.data}")
            staff.apple = form.apple.data
        if staff.device_id != form.device_id.data:
            changes.append(
                f"PC asset number changed from {staff.device_id} to {form.device_id.data}"
            )
            staff.device_id = form.device_id.data
        if staff.notes != form.notes.data:
            changes.append(f"Notes changed from {staff.notes} to {form.notes.data}")
            staff.notes = form.notes.data

        db.session.commit()

        for change in changes:
            log_entry = StaffLog(
                staff_id=staff.id,
                change_description=change,
                user_id=current_user.id,
            )
            db.session.add(log_entry)
        db.session.commit()

        flash("Staff details updated successfully!", "success")
        return render_template(
            "staff_details.html",
            staff=staff,
            staff_form=form,
        )

    logs = StaffLog.query.filter_by(staff_id=staff.id).all()
    return render_template(
        "staff_details.html",
        staff=staff,
        logs=logs,
        staff_form=form,
    )

@main.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    update_form = UpdateAccountTypeForm()
    password_form = PasswordResetForm()
    admin_password_form = AdminPasswordResetForm()
    delete_form = DeleteAccountForm()
    if current_user.is_admin:
        if update_form.validate_on_submit() and "update_account" in request.form:
            user = User.query.filter_by(username=update_form.username.data).first()
            if user:
                user.is_admin = update_form.is_admin.data
                db.session.commit()
                flash("Account type updated!", "success")
            else:
                flash("User not found.", "danger")

        if delete_form.validate_on_submit() and "delete_account" in request.form:
            user = User.query.filter_by(username=delete_form.username.data).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                flash("Account deleted!", "success")
            else:
                flash("User not found.", "danger")

    if password_form.validate_on_submit() and "change_password" in request.form:
        print("Password form validated and submitted")
        if current_user.check_password(password_form.old_password.data):
            print("Old password correct")
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash("Your password has been updated!", "success")
        else:
            print("Old password incorrect")
            flash("Old password is incorrect.", "danger")

    if (
        admin_password_form.validate_on_submit()
        and "admin_change_password" in request.form
    ):
        print("Admin password form validated and submitted")
        user = User.query.filter_by(username=admin_password_form.username.data).first()
        if user:
            user.set_password(admin_password_form.new_password.data)
            db.session.commit()
            flash(f"Password for {user.username} has been updated!", "success")
        else:
            flash("User not found.", "danger")

    return render_template(
        "settings.html",
        update_form=update_form,
        password_form=password_form,
        admin_password_form=admin_password_form,
        delete_form=delete_form,
    )


#_____________________________________________________________
#
#        WEB FILE EXPLORER          
# 
#   ROOT_DIR
#   Def     A -> Z
#   Routes  A -> Z
#_____________________________________________________________


#
#   ROOT_DIR
#
ROOT_DIR = os.path.join(os.getcwd(), 'miniRoot')

#
#   DEFINITIONS A -> Z
#
def is_safe_path(base_path, user_path, follow_symlinks=True):
    if follow_symlinks:
        base_path = os.path.realpath(base_path)
        user_path = os.path.realpath(user_path)
    return os.path.commonprefix([base_path, user_path]) == base_path

def search_files_and_folders(directory, query):
    result = {'folders': [], 'files': []}
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if query in folder.lower():
                relative_path = os.path.relpath(folder_path, directory)
                result['folders'].append(relative_path)
        for file in files:
            file_path = os.path.join(root, file)
            if query in file.lower():
                relative_path = os.path.relpath(file_path, directory)
                result['files'].append(relative_path)
    return result

def sort_items(items, sort_key, reverse=False):
    return sorted(items, key=lambda x: x[sort_key], reverse=reverse)




#
#   ROUTES A -> Z
#

@main.route('/create_folder', methods=['POST'])
@login_required
def create_folder():
    data = request.get_json()
    parent_dir = os.path.join(ROOT_DIR, data.get('parent_dir').lstrip('/'))
    new_folder_name = data.get('new_folder_name')
    new_folder_path = os.path.join(parent_dir, new_folder_name)

    if not is_safe_path(ROOT_DIR, new_folder_path):
        abort(403)

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        return 'Folder created successfully'
    else:
        return 'Error: Folder already exists', 400

@main.route('/delete', methods=['POST'])
@login_required
def delete():
    data = request.get_json()
    path_to_delete = os.path.join(ROOT_DIR, data.get('path').lstrip('/'))

    if not is_safe_path(ROOT_DIR, path_to_delete):
        abort(403)

    if os.path.isdir(path_to_delete):
        shutil.rmtree(path_to_delete)
        return 'Folder deleted successfully'
    elif os.path.isfile(path_to_delete):
        os.remove(path_to_delete)
        return 'File deleted successfully'
    else:
        return 'Error: File or directory not found', 404

@main.route('/download_file', methods=['GET'])
@login_required
def download_file():
    file_path = request.args.get('file_path', '')
    abs_file_path = os.path.join(ROOT_DIR, file_path.lstrip('/'))

    if not is_safe_path(ROOT_DIR, abs_file_path):
        abort(403)

    if os.path.exists(abs_file_path) and os.path.isfile(abs_file_path):
        return send_from_directory(directory=os.path.dirname(abs_file_path), path=os.path.basename(abs_file_path), as_attachment=True)
    else:
        return 'Error: File not found', 404

@main.route('/download_folder', methods=['GET'])
@login_required
def download_folder():
    folder_path = request.args.get('folder_path', '')
    abs_folder_path = os.path.join(ROOT_DIR, folder_path.lstrip('/'))

    if not is_safe_path(ROOT_DIR, abs_folder_path):
        abort(403)

    if os.path.exists(abs_folder_path) and os.path.isdir(abs_folder_path):
        zip_path = shutil.make_archive(abs_folder_path, 'zip', abs_folder_path)
        return send_from_directory(directory=os.path.dirname(zip_path), path=os.path.basename(zip_path), as_attachment=True)
    else:
        return 'Error: Folder not found', 404

@main.route('/list', methods=['GET'])
@login_required
def list_files():
    directory = request.args.get('dir', ROOT_DIR)
    directory = os.path.join(ROOT_DIR, directory.lstrip('/'))
    query = request.args.get('query', '').lower()
    sort = request.args.get('sort', 'name-asc')

    if not is_safe_path(ROOT_DIR, directory):
        abort(403)

    if not os.path.exists(directory):
        return jsonify({'folders': [], 'files': [], 'path': directory})

    if query:
        result = search_files_and_folders(directory, query)
    else:
        result = {'folders': [], 'files': []}
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                result['folders'].append(item)
            else:
                result['files'].append(item)

    sort_key, sort_order = sort.split('-')
    reverse = sort_order == 'desc'
    result['folders'] = sort_items([{'name': f, 'path': os.path.join(directory, f)} for f in result['folders']], 'name', reverse)
    result['files'] = sort_items([{'name': f, 'path': os.path.join(directory, f)} for f in result['files']], 'name', reverse)

    return jsonify({'folders': [f['name'] for f in result['folders']], 'files': [f['name'] for f in result['files']], 'path': directory})

@main.route('/move_to_parent', methods=['POST'])
@login_required
def move_to_parent():
    data = request.get_json()
    path = os.path.join(ROOT_DIR, data.get('path').lstrip('/'))
    parent_path = os.path.dirname(os.path.dirname(path))
    new_path = os.path.join(parent_path, os.path.basename(path))

    if not (is_safe_path(ROOT_DIR, path) and is_safe_path(ROOT_DIR, new_path)):
        abort(403)

    if os.path.exists(path):
        os.rename(path, new_path)
        return 'Moved to parent directory successfully'
    else:
        return 'Error: File or directory not found', 404

@main.route('/rename', methods=['POST'])
@login_required
def rename():
    data = request.get_json()
    old_name = os.path.join(ROOT_DIR, data.get('old_name').lstrip('/'))
    new_name = os.path.join(ROOT_DIR, data.get('new_name').lstrip('/'))

    if not (is_safe_path(ROOT_DIR, old_name) and is_safe_path(ROOT_DIR, new_name)):
        return jsonify({'error': 'Unsafe path'}), 403

    if os.path.exists(old_name):
        try:
            os.rename(old_name, new_name)
            return jsonify({'message': 'Folder renamed successfully', 'path': os.path.dirname(new_name)})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File or directory not found'}), 404

@main.route('/upload', methods=['POST'])
@login_required
def upload():
    target_dir = request.form['target_dir']
    target_dir = os.path.join(ROOT_DIR, target_dir.lstrip('/'))

    if not is_safe_path(ROOT_DIR, target_dir):
        abort(403)

    file = request.files['file']
    file.save(os.path.join(target_dir, file.filename))
    return 'File uploaded successfully'

@main.route('/view_file', methods=['GET'])
@login_required
def view_file():
    file_path = request.args.get('file_path', '')
    abs_file_path = os.path.join(ROOT_DIR, file_path.lstrip('/'))

    if not is_safe_path(ROOT_DIR, abs_file_path):
        abort(403)

    if os.path.exists(abs_file_path) and os.path.isfile(abs_file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext in ['.txt', '.html', '.css', '.js', '.py']:
            with open(abs_file_path, 'r') as f:
                return Response(f.read(), mimetype='text/plain')
        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return send_from_directory(directory=os.path.dirname(abs_file_path), path=os.path.basename(abs_file_path))
        elif file_ext == '.pdf':
            return send_from_directory(directory=os.path.dirname(abs_file_path), path=os.path.basename(abs_file_path))
        elif file_ext == '.docx':
            doc = Document(abs_file_path)
            doc_text = '\n'.join([para.text for para in doc.paragraphs])
            return Response(doc_text, mimetype='text/plain')
        else:
            return 'Unsupported file type', 415
    else:
        return 'Error: File not found', 404

@main.route('/web_files')
@login_required
def web_files():
    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)
    return render_template('web_files.html', root_dir=ROOT_DIR)