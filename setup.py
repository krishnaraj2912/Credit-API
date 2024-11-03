import os
import subprocess
import sys
from pathlib import Path
import getpass

project_root = Path(__file__).parent
venv_path = project_root / "env"
requirements_file = project_root / "requirements.txt"
env_file_path = project_root / ".env"

def create_virtualenv():
    try:
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
    except subprocess.CalledProcessError as e:
        print(f"Failed to create virtual environment: {e}")

def install_requirements():
    try:
        print("Installing requirements...")
        if os.name == "nt":  # Check if the OS is Windows
            pip_executable = os.path.join(venv_path, "Scripts", "pip.exe")
        else:  # For Unix-like systems
            pip_executable = os.path.join(venv_path, "bin", "pip")

        subprocess.check_call([pip_executable, "install", "-r", requirements_file])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")

def create_env_file(db_username, db_password, db_name):
    try:
        print("Creating .env file...")
        env_content = f"DB_URL=postgresql+asyncpg://{db_username}:{db_password}@localhost:5432/{db_name}"
        with open(env_file_path, "w") as f:
            f.write(env_content)
    except IOError as e:
        print(f"Failed to create .env file: {e}")

def create_database(db_name):
    try:
        print("Creating database...")
        if os.name == "nt":
            subprocess.check_call(["psql", "-U", "postgres", "-c", f'CREATE DATABASE "{db_name}";'])
        else:
            subprocess.check_call(["sudo", "-u", "postgres", "psql", "-c", f'CREATE DATABASE "{db_name}";'])
    except subprocess.CalledProcessError as e:
        print("\n\n")
        print("------------------------------------------------------------------")
        print("This should be because of permission issue")
        print(f"Kindly Create a db using postgres GUI with DB Name: '{db_name}'")
        print("------------------------------------------------------------------")
        print("\n\n")
        print(f"Failed to create database: {e}")

def main():
    try:
        db_username = input("Enter the PostgreSQL username[postgres]: ")
        if db_username == "":
            db_username = "postgres"
        db_password = getpass.getpass("Enter the PostgreSQL password: ")
        db_name = input("Enter the desired database name[Credit]: ")
        if db_name == "":
            db_name = "Credit"

        create_virtualenv()
        install_requirements()
        create_env_file(db_username, db_password, db_name)
        create_database(db_name)

        print("Setup complete!")
    except Exception as e:
        print(f"An error occurred during setup: {e}")

if __name__ == "__main__":
    main()
