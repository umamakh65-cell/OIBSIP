Task 2 - BMI Calculator

Project Overview

This project is an advanced BMI (Body Mass Index) Calculator built using Python.

The application provides a graphical user interface using Tkinter, stores BMI records in an SQLite database, supports multiple users, and displays BMI trends using Matplotlib.

Features

- Tkinter graphical user interface

- User name, weight, and height input

- BMI calculation using:
  
  BMI = weight / (height²)

- BMI classification:
  
  - Underweight: BMI < 18.5
  - Normal: BMI 18.5–24.9
  - Overweight: BMI 25–29.9
  - Obese: BMI ≥ 30

- BMI result rounded to two decimal places

- Color-coded BMI category feedback

- Input validation for invalid and non-positive values

- Multi-user BMI records

- SQLite database for historical records

- View historical BMI records

- BMI trend line graph using Matplotlib

- Database error handling

Technologies Used

- Python
- Tkinter
- SQLite3
- Matplotlib
- datetime

Project Structure

Task02_BMI_Calculator/
├── bmi_calculator.py
├── bmi_records.db
└── README.md

How to Run

1. Make sure Python is installed.

2. Install Matplotlib:

pip install matplotlib

3. Run the application:

python bmi_calculator.py

4. Enter the user's name, weight in kilograms, and height in meters.

5. Click Calculate BMI.

6. Use View History to see stored records.

7. Use View BMI Trend to display the user's BMI trend.

Data Storage

BMI records are stored locally in an SQLite database named:

"bmi_records.db"

The database stores:

- User name
- Weight
- Height
- BMI
- BMI category
- Date and time of the record

Error Handling

The application validates user input and displays helpful error messages when:

- Weight or height is not numeric
- Weight or height is zero or negative
- A user name is missing
- Database reading fails
- Database writing fails

The application avoids crashing when these errors occur.

Privacy Considerations

The application processes BMI information entered by the user.

BMI records are stored locally in the application's SQLite database and are not intentionally sent to an external server or third-party service.

Users should avoid entering unnecessary personal information.

The local database file should not be shared publicly if it contains personal records.

Learning Outcome

This project demonstrates Python GUI development, input validation, database storage, exception handling, multi-user data management, and data visualization using Matplotlib.
