# Credit API Setup Guide

This guide will help you set up the project environment, including installing dependencies and setting up a PostgreSQL database.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3
- PostgreSQL
- `psql` command-line tool (usually included with PostgreSQL)

## Steps to Set Up

1. **Clone the Repository**

   Clone the repository to your local machine using the following command:

   ```bash
   git clone https://github.com/krishnaraj2912/Credit-API.git
   cd Credit-API
   ```

2. **Run the Setup Script**

   Execute the setup script, which will prompt you for PostgreSQL credentials and the database name:

   ```bash
   python setup.py
   ```

   During this process, you will be asked for:
   - PostgreSQL username (default is `postgres`)
   - PostgreSQL password
   - Desired database name (default is `Credit`)

   The script will:
   - Create a virtual environment.
   - Install the required packages listed in `requirements.txt`.
   - Create a `.env` file containing the database URL.
   - Attempt to create the PostgreSQL database.

3. **Database Creation**

   If the database creation fails due to permission issues, you may need to create the database manually using a PostgreSQL GUI tool (e.g., pgAdmin) or using the command line. The database name you should create is the one you specified in the setup script.

4. **Activate the Virtual Environment**

   After running the setup script, activate the virtual environment created during the setup:

   - On Windows:

     ```bash
     .\env\Scripts\activate
     ```

   - On Unix or macOS:

     ```bash
     source env/bin/activate
     ```

5. **Running the Project**

   Once the setup is complete and the virtual environment is activated, you can run the project using
   ```
   uvicorn application.index:app --host 0.0.0.0 --port 8000 --reload
   ```

## Testing

### Option 1: Import into Postman

1. **Open Postman** and click **Import**.
2. Select the `Credit_API.postman_collection.json` file from the project root.
3. Click on the imported collection and hit **Run** to execute the requests.

### Option 2: Run Tests via Python Script

```bash
cd Credit/test
```

1. **Start the FastAPI App**:
   - Run the following command:
     ```bash
     uvicorn index:app --host 127.0.0.1 --port 8000 --reload
     ```

2. **Run the Test Script**:
   - Execute the test script:
     ```bash
     python test.py
     ```

## Documentation

- For API Documentation use '/service/docs' endpoint

