# Flask Demo Project: CRUD, Authentication, and File Handling
A functional, minimal news blog built with the **Python Flask** framework. This project serves as a comprehensive demonstration of core web development skills, data persistence, and application logic using standard Python tools.

---

## 🔑 Test Credentials (Journalist Access)

For demonstration purposes, you can log in as a journalist (author) using the following credentials to test the post creation, update, and delete functionality.

| Role | Login (Email) | Password |
| :--- | :--- | :--- |
| Journalist | `rudeusgreyrat@gmail.com` | `password` |
| Journalist | `erisboreasgreyrat@gmail.com` | `password` |
| Journalist | `ghislainededoldia@gmail.com` | `password` |

---

## 🚀 Key Features and Skills Demonstrated

* **Full CRUD Functionality:** Implements the complete Create, Read, Update, and Delete cycle for user-generated articles using RESTful routing.
* **Authentication & Authorization:** Demonstrates session-based user authentication and implements authorization logic to ensure only the author can modify their posts.
* **Data Persistence:** Utilizes **SQLAlchemy ORM** for efficient database interaction and data modeling with a **SQLite** backend.
* **File Handling:** Includes logic for secure file uploads, image saving, and deleting previous files upon update.
* **User Interface:** Features a responsive, modern design powered by **Bootstrap 5** and dynamic rendering via **Jinja2** templates.

---

## 🛠️ Getting Started (Setup & Run)

Follow these steps to get the development environment running on your local machine.

### Prerequisites

You must have Python 3 installed.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/stepanovcpp/flask_demo_news.git](https://github.com/stepanovcpp/flask_demo_news.git)
    cd flask_demo_news
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    *(Assuming your dependencies are listed in a `requirements.txt` file)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    *(The exact command may vary based on your app structure, but typically)*
    ```bash
    python app.py
    ```

5.  Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## ⚠️ Security Disclaimer (Demo Environment)

**ATTENTION:** This repository is intended strictly for **demonstration and portfolio purposes**.

For ease of setup and functionality showcase, the SQLite database files (`*.db`) and/or basic configuration containing Flask's **Secret Keys** may be deliberately included in the repository.

**DO NOT** use this approach in any production or live environment. In a real-world application, database files and secret keys **must** be excluded via `.gitignore` and stored securely using environment variables.
