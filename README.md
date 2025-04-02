```markdown
# DavidTabibov Python Project

This project is a Full Stack application that includes a Django-based backend (Blog API) and a React-based frontend. The backend provides a RESTful API for managing users, articles, and comments, while the frontend (if implemented) will consume the API to display blog content and handle user interactions.

---

## Features

### Backend (Blog API)
- **User Management:**
  - User registration and login endpoints.
  - JWT authentication.
  - **User Roles & Groups:**  
    - The project distinguishes between regular users and admin users.
    - Admin users (or users belonging to a dedicated "Editors" or "Admin" group) can create, update, and delete articles, and have the ability to delete inappropriate comments.
    - Regular users can view articles and post comments.
  - *Note:* If you wish to manage groups (e.g., Editors, Users, Admins) via Django Admin or custom management commands, you can do so.

- **Articles Management:**
  - CRUD operations for articles.
  - Each article includes a title, content, publication date, author, and tags (stored as a comma-separated string).
  - Publicly viewable by all users.
  - Search functionality by title, content, tags, or author.
  - Only admin users (or users with proper group membership) can create, update, or delete articles.

- **Comments Management:**
  - Registered users can add comments to articles.
  - Each comment includes content, the author’s name, and the comment date.
  - Only admin users can delete comments.
  - *Optional Improvement:* You can extend the functionality to allow users to delete their own comments.

- **Initial Database Seeding:**
  - A custom management command (`seed`) seeds the database with at least 2 users, 2 articles, and 2 comments per article.

- **Security:**
  - Sensitive information (secret keys, database credentials) is stored in environment variables via a `.env` file.
  - The project uses PostgreSQL as the database.

- **Unit Tests:**
  - Each app includes a `tests.py` file.  
  - It is recommended to add unit tests for authentication, article CRUD operations, and comment functionalities to ensure the API behaves as expected.

### Frontend (React)
- Will include a navigation bar for registration, login, and logout.
- Homepage displaying the latest articles with search and load more functionality.
- Detailed article pages with comments and options for comment editing/deletion (by the comment's author).

---

## Project Structure

```
DAVIDTABIBOV-PYTHONPROJECT/
├── VENV/                      # Virtual environment directory (ensure it's in .gitignore)
├── BLOG-API/                  # Backend code (Django)
│   ├── BLOG-API/              # Django project folder (settings.py, urls.py, wsgi.py, etc.)
│   ├── ACCOUNTS/              # Django app for user management & authentication
│   │   ├── admin.py           # (Optional) Customize Django Admin if needed
│   │   ├── apps.py
│   │   ├── models.py          # Empty if using Django's built-in User model
│   │   ├── serializers.py     # Contains registration serializer
│   │   ├── tests.py           # (Add unit tests here)
│   │   ├── urls.py            # Contains the /api/register/ endpoint
│   │   └── views.py           # Contains the RegisterView
│   ├── ARTICLES/              # Django app for managing blog articles
│   │   ├── admin.py           # Registers the Article model for Django Admin
│   │   ├── apps.py
│   │   ├── models.py          # Defines the Article model
│   │   ├── permissions.py     # Custom permissions (e.g., IsAdminOrReadOnly)
│   │   ├── serializers.py     # Serializes Article objects
│   │   ├── tests.py           # (Add unit tests here)
│   │   ├── urls.py            # Defines endpoints for articles
│   │   └── views.py           # Contains the ArticleViewSet with search functionality
│   ├── COMMENTS/              # Django app for managing comments
│   │   ├── admin.py           # Registers the Comment model for Django Admin
│   │   ├── apps.py
│   │   ├── models.py          # Defines the Comment model (with FK to Article and User)
│   │   ├── serializers.py     # Serializes Comment objects
│   │   ├── tests.py           # (Add unit tests here)
│   │   ├── urls.py            # Defines endpoints for comments
│   │   └── views.py           # Contains views for listing/creating and deleting comments
│   ├── .env                   # Environment variables file (placed at BLOG-API root)
│   ├── manage.py              # Django management file
│   ├── requirements.txt       # List of Python dependencies
│   └── README.md              # (Optional) Backend-specific documentation
├── FRONTEND/                  # Frontend code (React)
│   ├── package.json
│   ├── public/
│   ├── src/
│   └── ...                    # Other React-related files
└── README.md                  # This README file (project documentation)
```

**Notes:**
- The **VENV** folder should be located at the project root and must be excluded from Git (via `.gitignore`).
- The **.env** file is placed in the root of the **BLOG-API** folder so that Django’s settings can access the environment variables.
- The main README.md (this file) covers an overview of both the backend and frontend.
- If an app (e.g., Accounts) does not require a custom model because it uses Django's built-in User, its models.py can remain empty.

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the project root directory:**
   ```bash
   cd DAVIDTABIBOV-PYTHONPROJECT
   ```

3. **Create and activate a virtual environment:**
   ```bash
   python -m venv VENV
   # Activate the virtual environment:
   # On Windows:
   VENV\Scripts\activate
   # On Linux/Mac:
   source VENV/bin/activate
   ```

4. **Install the required Python packages for the backend:**
   Navigate to the `BLOG-API` folder and run:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create the `.env` file in the BLOG-API folder:**
   Create a file named `.env` in the `BLOG-API` folder with the following content (update values as needed):
   ```dotenv
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=blog_api_db
   DB_USER=postgres
   DB_PASSWORD=123456
   DB_HOST=localhost
   DB_PORT=5432
   ```

6. **Run Django migrations:**
   From the `BLOG-API` folder, run:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **(Optional) Seed the database:**
   Populate the database with initial data for users, articles, and comments:
   ```bash
   python manage.py seed
   ```

8. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

9. **(If applicable) Setup the Frontend:**
   Navigate to the `FRONTEND` folder, install dependencies, and run the React app:
   ```bash
   cd ../FRONTEND
   npm install
   npm start
   ```

---

## API Endpoints (Backend)

### Authentication
- **POST** `/api/register/` – Register a new user.
- **POST** `/api/token/` – Obtain a JWT token for login.
- **POST** `/api/token/refresh/` – Refresh the JWT token.

### Articles
- **GET** `/api/articles/` – Retrieve all articles.
- **GET** `/api/articles/?search=<query>` – Search articles by title, content, tags, or author.
- **GET** `/api/articles/<id>/` – Retrieve a specific article.
- **POST** `/api/articles/` – Create a new article (admin only).
- **PUT** `/api/articles/<id>/` – Update an article (admin only).
- **DELETE** `/api/articles/<id>/` – Delete an article (admin only).

### Comments
- **GET** `/api/articles/<id>/comments/` – Retrieve comments for a specific article.
- **POST** `/api/articles/<id>/comments/` – Add a comment to an article (registered users only).
- **DELETE** `/api/comments/<id>/` – Delete a comment (admin only).

---

## Additional Notes

- **User Groups & Permissions:**  
  The project differentiates between regular users and admin users. Admin users (or users in a dedicated group) have full CRUD access on articles and the ability to delete comments. Regular users can only view articles and add comments. You can manage user groups via Django Admin or through additional management commands if required.

- **Unit Tests:**  
  It is recommended to write unit tests for authentication, article CRUD operations, and comment functionalities. Each app includes a `tests.py` file for this purpose.

- **Environment Variables:**  
  Sensitive data such as secret keys and database credentials are managed via the `.env` file using `python-decouple`.

---

## License

[Specify your license here]

---

## Acknowledgments

- Developed as part of a Full Stack module project.
- Thanks to the instructors and mentors for their guidance.
```
