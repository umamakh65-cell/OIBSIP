Random Password Generator

Oasis Infobyte Internship — OIBSIP Task 3

A secure graphical password generator built with Python and Tkinter. The application generates strong random passwords according to user-defined criteria and includes password-strength feedback, automatic clipboard copying, ambiguous-character exclusion, and session-only generation history.

---

1- Objective

The objective of this project is to build a password generator that creates strong and random passwords based on user-defined requirements.

This project implements the Advanced Tier of the task by providing a graphical user interface with customizable password criteria, cryptographically secure password generation, password-strength indication, clipboard integration, security validation, and generation history.

---

2- Features

Password Length

- Password length can be selected using a Spinbox.
- Supported length: 8 to 64 characters.
- A minimum of 8 characters is enforced.
- Invalid password lengths are rejected with an error message.

Character Type Selection

Users can choose which character types should be included:

- Uppercase letters: "A-Z"
- Lowercase letters: "a-z"
- Numbers: "0-9"
- Symbols: "!@#$..."

At least two character types must be selected before a password can be generated.

Cryptographically Secure Generation

The application uses Python's "secrets" module rather than the standard "random" module for password generation.

Secure random selection is performed using:

secrets.choice()

and the final password is securely shuffled using:

secrets.randbelow()

This makes the generator appropriate for security-sensitive password creation.

Character-Type Guarantee

The generator guarantees that the resulting password contains at least one character from every selected character type.

For example, if uppercase letters, lowercase letters, and numbers are selected, the generated password will contain at least one character from each of those three categories.

The remaining characters are then selected from the combined character pool.

Password Strength Indicator

The application provides both:

- A text-based strength label
- A visual strength bar

The strength calculation considers factors such as:

- Password length
- Lowercase characters
- Uppercase characters
- Numbers
- Symbols
- Number of selected character types

The resulting strength is displayed as:

- Weak
- Medium
- Strong

Automatic Clipboard Copy

Every newly generated password is automatically copied to the system clipboard using "pyperclip".

A separate COPY TO CLIPBOARD button is also available for manually copying the currently displayed password.

Exclude Ambiguous Characters

The application provides an option to exclude characters that can be visually confusing.

The excluded characters are:

0 O l 1 I

This option can be enabled through the Exclude ambiguous characters checkbox.

Generation History

The application maintains the last five generated passwords during the current session.

- The newest password is displayed first.
- Only five passwords are retained.
- When a sixth password is generated, the oldest password is removed.
- Password history is kept only in memory.
- Password history is not saved to a file or database.

Scrollable Interface

The application uses a scrollable Tkinter interface with a vertical scrollbar.

This ensures that all sections of the application remain accessible when the window is smaller than the complete interface, including the Generation History section.

---

3- User Interface

The interface contains the following sections:

1. Random Password Generator title
2. Password Length
3. Character Types
4. Security Options
5. Generated Password
6. Password Strength
7. Generate Password button
8. Copy to Clipboard button
9. Generation History

The interface is designed to keep the password-generation process simple and easy to use.

---

4- Security Approach

Security is an important part of this project because passwords are sensitive credentials.

"secrets" Instead of "random"

The project uses Python's "secrets" module for random password generation.

The "secrets" module is intended for generating cryptographically strong random values and is therefore more appropriate for password generation than the standard "random" module.

Guaranteed Character Diversity

The generator explicitly selects one character from each character set selected by the user before filling the remaining password positions.

This prevents a generated password from accidentally missing one of the requested character categories.

Secure Shuffling

After the password characters have been selected, the application uses "secrets.randbelow()" to perform a secure shuffle.

Session-Only History

Generated passwords are not written to disk.

The history is maintained in memory while the application is running and is lost when the application closes.

This avoids permanently storing generated passwords.

---

5- How Password Generation Works

The password-generation process follows these steps:

1. Validate the requested password length.
2. Confirm that at least two character types have been selected.
3. Build the selected character sets.
4. Remove ambiguous characters if the security option is enabled.
5. Select at least one character from each selected character set.
6. Combine the usable character sets into one character pool.
7. Generate the remaining characters using "secrets.choice()".
8. Securely shuffle the generated characters using "secrets.randbelow()".
9. Display the resulting password.
10. Calculate the password strength.
11. Update the visual strength bar.
12. Automatically copy the password to the clipboard.
13. Add the password to the session history.

---

6- Password Strength Calculation

The password-strength system uses a custom score based on password characteristics.

Points are awarded for:

- Password length of at least 8 characters
- Password length of at least 12 characters
- Password length of at least 20 characters
- Lowercase characters
- Uppercase characters
- Numbers
- Symbols
- Three or more selected character types
- All four character types

The final score determines the displayed strength:

Score Range| Strength| Visual Bar
0–3| Weak| 30%
4–6| Medium| 65%
7+| Strong| 100%

The strength bar also changes according to the calculated strength level.

---

7- Input Validation

The application validates user input before generating a password.

Length Validation

The application rejects:

- Invalid or non-numeric values
- Passwords shorter than 8 characters
- Passwords longer than 64 characters

Character Selection Validation

The application requires at least two selected character types.

It also verifies that the selected character sets remain usable after ambiguous characters are removed.

---

8- Generation History Behavior

The history stores a maximum of five generated passwords.

New passwords are inserted at the beginning of the history.

For example:

Newest Password
Password 2
Password 3
Password 4
Oldest Password

When another password is generated, the oldest entry is removed so that only the latest five remain.

The history exists only for the current application session.

---

9- Technologies Used

- Python — Application development
- Tkinter — Graphical user interface
- secrets — Cryptographically secure random generation
- string — Standard character sets
- pyperclip — Clipboard integration

---

10- Installation

Prerequisites

- Python 3.x
- "pyperclip"

Tkinter is included with most standard Python installations.

Install the Dependency

Open a terminal or command prompt and run:

pip install pyperclip

Alternatively, if a "requirements.txt" file is included:

pip install -r requirements.txt

---

11- Running the Application

Navigate to the project directory and run:

python password_generator.py

The Random Password Generator window will open.

---

12- How to Use

Step 1 — Select Password Length

Use the Password Length Spinbox to select a length between 8 and 64 characters.

Step 2 — Select Character Types

Choose the character types you want to include.

At least two types must be selected.

Step 3 — Configure Security Options

Enable Exclude ambiguous characters if you want to remove visually confusing characters such as "0", "O", "l", "1", and "I".

Step 4 — Generate

Click:

GENERATE PASSWORD

The application will generate a secure password based on the selected criteria.

Step 5 — Check Strength

The generated password's strength is displayed below the password along with a visual strength bar.

Step 6 — Clipboard

The generated password is automatically copied to the clipboard.

You can also click:

COPY TO CLIPBOARD

to copy the displayed password again.

Step 7 — View History

Scroll down to the Generation History - Last 5 section to view recently generated passwords.

---

13- Testing

The application was tested to verify its main functionality and security rules.

Tests included:

- Generating passwords with all four character types
- Generating passwords with exactly two character types
- Testing minimum password length
- Testing maximum password length
- Testing invalid length input
- Testing insufficient character-type selection
- Testing ambiguous-character exclusion
- Verifying that every selected character type appears in the generated password
- Testing password-strength calculation
- Testing automatic clipboard copying
- Testing manual clipboard copying
- Generating more than five passwords to verify the history limit
- Verifying that the newest password appears first
- Verifying that password history is session-only
- Testing the scrollable interface

All tested features are functioning as expected.

---

14- Project Structure

Task3_Random_Password_Generator/
│
├── password_generator.py
├── README.md
├── requirements.txt
└── screenshots/
    ├── main_interface.png
    ├── generated_password.png
    └── generation_history.png

---

15- requirements.txt

The project's external dependency is:

pyperclip

The following modules are part of Python's standard library:

tkinter
secrets
string

---

19- Author

Umama Khan

Oasis Infobyte Internship — OIBSIP

Task 3 — Random Password Generator
