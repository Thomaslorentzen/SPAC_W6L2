# Library Management System

This Python project is developed as part of a software solution for libraries. The system facilitates various library operations such as managing book collections, handling loans, returns, and reservations.

## System Requirements

### Book Collection
- The system should be capable of creating, storing, and searching a collection of books.
- Each book entry should include a title, author, publication year, and a unique identification code.

### User Accounts
- Create user accounts for library members, including:
  - User ID
  - User Name
  - User Address
  - Overview of borrowed books

### Loans and Returns
- Implement functions to allow borrowing and returning books.
- The system should check the availability of the book and update the user's borrowing overview accordingly.

### Reservation
- Allow users to reserve books that are currently on loan and receive notifications when the book becomes available.


## Outputs
- Users should have the option to receive notifications about their loans in the form of a report.
- Consider additional relevant reports such as loan history for a specific book, overall loans, etc.

## Menu
- A GUI will be implemented to allow users to access the system seamlessly.


## Installation Guide

### Prerequisites:
- Anaconda installed
- pip installed (usually comes with Anaconda)
- MySQL server installed
- Graphviz installed (for UML)

### Steps:

1. **Clone the Repository:**
`git clone https://github.com/Thomaslorentzen/SPAC_W6L2`

2. **Navigate to the Repository Directory:**
`cd */SPAC_W6L2`

3. **Create a Virtual Environment (Optional but Recommended):**
`conda create -n your-env-name python=3.9`

4. **Activate the Virtual Environment:**
`conda activate your-env-name`

5. **Install Required Packages:**
`pip install .`

6. **Verify Installation:**
Ensure all dependencies are installed successfully without any errors.

7. **Deactivate Virtual Environment (If Created):**
`conda deactivate`

8. **Create config.json.**
Create a file containing the fields username and password in the repocetory directory.


## Contributors
- [Thomas Kristian Lorentzen](https://github.com/Thomaslorentzen)
- [Søren Langkilde](https://github.com/soeren97)

### Additional Notes:

- **Virtual Environment:** Creating a virtual environment is a good practice to isolate project dependencies from other projects and the system Python environment.
- **pip Install:** The `pip install .` command installs the necessary packages specified in the `setup.py` file from the current directory.
- **requirements** The required packages can be found in the `setup.py` file as the variable `INSTALL_REQQUIRES`.
- **UML diagrams** UML diagrams can be generated using the `uml_generator.py` file and will be located in a new folder called `UML`
