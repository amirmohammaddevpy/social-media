
# Social Media Platform

A feature-rich social media platform built with Python, Django, and Django REST Framework. The project provides a RESTful API for social networking features, user profiles, posts, stories, and private messaging.

## Features

### Authentication and User Profiles
- JWT-based authentication.
- User profile management and profile editing.
- Follow and unfollow users.
- User search functionality.

### Posts and Interactions
- Create and explore posts.
- Like and dislike posts.
- Comment on posts.
- Display post and like counts.
- Save posts for later.
- Upload images and videos.

### Stories
- Create and view stories.
- Automatic story expiration after 24 hours.
- Stories visibility restricted to followers.

### Private Messaging
- Private conversations between users.
- Persistent message storage in the database.
- Message read receipts (seen status).
- Last-seen status for users.
- Online status based on periodic heartbeat requests.

### User Activity
- Online/offline status tracking.
- Human-readable last-seen timestamps, such as hours or days ago.
- Heartbeat-based activity tracking using HTTP requests.

### API Documentation
- API endpoints documented for easier exploration and testing.
- JWT authentication for protected endpoints.

## Tech Stack

- **Language:** Python
- **Backend:** Django
- **API:** Django REST Framework (DRF)
- **Authentication:** JSON Web Tokens (JWT)
- **Real-time features:** HTTP heartbeat-based presence tracking
- **Database:** Django-supported database (configure for your environment)
- **API Testing:** Postman

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/amirmohammaddevpy/social-media.git
cd socia-media
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Linux or macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Configure the required environment variables for your local setup, including Django settings and secret keys.

Never commit production secrets or private credentials to GitHub.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The development server will be available at:

`http://127.0.0.1:8000/`

## API Documentation

Run the project locally and open the API documentation endpoint configured in your Django project.

Protected endpoints require valid JWT authentication.

## Project Goals

This project was built to develop practical backend engineering skills, including:

- Designing RESTful APIs.
- Implementing authentication and authorization.
- Managing relational data and user relationships.
- Handling media uploads.
- Building messaging and read-receipt functionality.
- Tracking user presence with heartbeat requests.
- Organizing a Django application for maintainability.

## Future Improvements

- Automated tests for API endpoints and permissions.
- Improved API performance and database query optimization.
- Rate limiting and additional security hardening.
- More robust presence tracking and message delivery handling.
- Containerized deployment with Docker.

## Author

**Amir Mohammad Barabadi**

Computer Science Student | Django Backend Developer

- GitHub: [@YOUR_GITHUB_USERNAME](https://github.com/amirmohammaddevpy)
- LinkedIn: [Amir Mohammad Barabadi](www.linkedin.com/in/amir-mohammad-barabadi)

## Live Demo

🌐 [Visit Social Media Platform](https://www.amirmohammadbarabadi.ir/)

## License

Choose and add a license before distributing or reusing this project.

