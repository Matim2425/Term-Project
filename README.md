# CyberSafe Vault

#### Video Demo: <PASTE-YOUR-VIDEO-URL-HERE>

#### Description:

CyberSafe Vault is a Python-based cybersecurity project that helps users organize, evaluate, and protect account credentials in a simple local vault. I chose this project because it connects directly to real-world security problems. Many users still reuse weak passwords or keep login information in unsafe places like notes apps, spreadsheets, or plain text files. This program was designed to solve a small but meaningful version of that problem by giving the user a structured way to create and manage secure credential records.

The project is menu-driven, which means the user interacts with the application through a list of numbered options. This design choice keeps the program simple to use and easy to demonstrate in a video presentation. When the program starts, it loads previously saved entries from a JSON file if one already exists. If the vault file does not exist, the program creates a new empty vault during execution. This allows the project to demonstrate both reading from and writing to files, which is one of the required outcomes for the assignment.

The application includes several key features. First, the user can add a new vault entry by entering a site name, username, and password. The user can either type a password manually or allow the program to generate one automatically. The password generator uses Python libraries to combine uppercase letters, lowercase letters, digits, and symbols into a stronger password. This shows how Python modules can extend the program’s functionality.

Another major feature is password strength analysis. The program checks the entered password and labels it as Weak, Moderate, or Strong based on its length and whether it contains lowercase letters, uppercase letters, digits, and punctuation characters. This makes the project more interesting than a basic storage app because it includes logic, data analysis, and decision-making instead of just saving text.

For security reasons, the program does not store raw passwords in plain text. Instead, it hashes the password using SHA-256 through the hashlib module before saving it. This was an intentional design decision because storing passwords in plain text would be a bad security practice. Even though this is a classroom project and not a production system, I wanted the design to reflect cybersecurity principles and show that I understand the importance of protecting sensitive data.

The project also includes a search feature so users can quickly find saved entries by site name or username. This improves usability and demonstrates how to loop through structured data. There is also a delete feature that allows the user to remove entries from the vault. These features help make the project more complete and more advanced than a small lab exercise.

An additional feature is the export report option. This creates a text-based security report that summarizes how many entries are saved and how many passwords are weak, moderate, or strong. I added this because it gives the application another practical use case and demonstrates file output in a second format besides JSON. The report can also be shown clearly during the required presentation video.

The project contains the following files:

- **TermProject.py**: The main Python program. It contains the menu, functions, class definition, password generation logic, password hashing logic, file handling, and error handling.
- **README.md**: This documentation file. It explains the purpose of the project, how it works, the design decisions, and the role of each file.
- **requirements.txt**: Lists the required libraries for the project. This project uses only Python standard library modules, so no third-party packages are needed.
- **vault_data.json**: Created automatically when the program saves entries. It stores the credential records in structured JSON format.
- **activity_log.txt**: Created automatically when the program runs. It logs important actions and errors.
- **security_report.txt**: Created automatically if the user chooses the export option. It summarizes saved vault data and password strength information.

There are several important design decisions in this project. The first was using JSON instead of plain text because JSON is structured, readable, and easy to load into Python. The second was using a class called `VaultEntry` to demonstrate object-oriented programming. While the project could have been built using only dictionaries, using a class made the structure clearer and helped meet the course objective related to OOP. The third design decision was separating the program into multiple functions instead of writing everything inside `main()`. This improves organization, readability, testing, and maintainability.

Overall, CyberSafe Vault demonstrates Python syntax, control structures, object-oriented programming, exception handling, file handling, and the use of libraries and modules. It is more advanced than a basic lab because it combines multiple course concepts into one practical cybersecurity-themed application.
