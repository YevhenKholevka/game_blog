
# Blogging Platform

An interactive web application for a blogging platform built with Flask, SQLite, and SQLAlchemy.

---

## 🚀 How to Run the Project Locally

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your_username/blogging-platform.git
    cd blogging-platform
    ```

2. **Create a virtual environment and install dependencies**:

    **Windows**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

    **Mac/Linux**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Set up the SQLite database**:

    No additional setup required for SQLite. The database will be automatically created when you run the migrations.

4. **Apply migrations**:

    ```bash
    flask db init      # Initialize migrations
    flask db migrate   # Create migration files
    flask db upgrade   # Apply migrations and create the database
    ```

5. **Run the development server**:

    ```bash
    flask run
    ```

6. **Open the browser**:

    Go to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 📂 Project Structure

```bash
game_blog/
├── app.py                    # Main application file
├── blog.db                   # SQLite database file
├── config.py                 # Configuration settings (secret key, database URI)
├── extensions.py             # Extension initializations (SQLAlchemy, Flask-Migrate)
├── models.py                 # Database models
├── requirements.txt          # Python dependencies
├── project_structure.txt     # File containing the project structure
├── README.md                 # Project setup instructions
├── .venv/                    # Virtual environment
├── migrations/               # Flask-Migrate migration scripts
├── static/                   # Static files (CSS, JS, images)
│   ├── scripts.js
│   └── styles.css
└── templates/                # Jinja2 HTML templates
    ├── add_post.html
    ├── edit_post.html
    ├── index.html
    ├── login.html
    ├── post.html
    └── register.html              # Project setup instructions
```

## 🛠️ Technologies Required
1. Python 3.10+
2. Flask 2.0+
3. SQLAlchemy 1.4+
4. Flask-Migrate
5. SQLite 3.0+
6. Git

## 📋 Additional Notes
If you encounter any issues, check the following:

1. Make sure Python 3.10+ is installed and added to the system PATH.
2. Verify the `requirements.txt` file has been correctly installed:
    ```bash
    pip install -r requirements.txt
    ```
3. Ensure that the database migrations have been correctly applied using `flask db upgrade`.

If you're using a different database (e.g., PostgreSQL), update the database URI in `config.py` accordingly.
