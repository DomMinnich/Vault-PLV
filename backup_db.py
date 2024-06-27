# Dev Dominic Minnich 2024
# backup_db.py

import os
import shutil
from datetime import datetime

def backup_database():
    # Define the paths
    instance_folder = os.path.join(os.getcwd(), 'instance')
    backup_folder = os.path.join(os.getcwd(), 'backups')

    # Ensure the backup folder exists
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # Get the current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Define the source and destination file paths
    source_file = os.path.join(instance_folder, 'inventory.db')
    destination_file = os.path.join(backup_folder, f'backup_{current_time}.db')

    # Copy the file
    shutil.copy2(source_file, destination_file)

if __name__ == '__main__':
    backup_database()
