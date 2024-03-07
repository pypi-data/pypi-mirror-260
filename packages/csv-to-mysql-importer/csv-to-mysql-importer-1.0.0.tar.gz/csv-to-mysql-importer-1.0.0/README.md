# csv_importer

csv_importer is a Python library that simplifies the process of importing CSV files into a MySQL database. It provides functionalities to organize CSV files, clean data, and upload data to a MySQL database.

## Features

- **CSV File Management:** Automatically organizes CSV files into a designated directory for processing.
- **Data Cleaning:** Cleans column names and data types for compatibility with MySQL.
- **Database Upload:** Uploads cleaned data from CSV files to a MySQL database.

## Installation

You can install csv_importer using pip:

```bash
pip install csv_importer



-> Usage
1) Prepare CSV Files:
    a)Place your CSV files in a directory of your choice.

2)Run main.py Script:
    a)Execute the main.py script from the command line.
    b)Provide your database connection details as command-line arguments:
        python main.py <db_host> <db_name> <db_user> <db_password>
    c)Replace <db_host>, <db_name>, <db_user>, and <db_password> with your actual database connection details.

3)Interact with the GUI:

    a)After running the main.py script, a GUI window titled "CSV to MySQL Importer" will appear.
    b)Click the "Select Folder" button to choose a directory containing CSV files.
    c)The selected folder will be processed, and the CSV files will be imported into your MySQL database.


-> Database Connection Details

1)You can modify your database connection details by providing them as command-line arguments when running the main.py script. The required arguments are:

<db_host>: The hostname or IP address of your MySQL server.
<db_name>: The name of the database you want to connect to.
<db_user>: The username for accessing the MySQL database.
<db_password>: The password for the specified username.

2)For example, to run the main.py script with your database connection details, you would use a command like this:

            python main.py localhost my_database username password


-> Dependencies

a)numpy
b)pandas
c)mysql-connector-python



```
