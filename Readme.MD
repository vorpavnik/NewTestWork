# Restaurant Booking API

This project provides a REST API for managing restaurant table reservations.

## Features

*   **Table Management:**  Create, read, update, and delete tables.
*   **Reservation Management:** Create, read, update, and delete reservations.
*   **Automated Table Availability:**  Automatically release tables and deactivate reservations after their scheduled duration.
*   **Booking Restrictions:**  Prevents booking in the past or less than 5 minutes from the current time.

## Technologies Used

*   Python 3.12
*   Django 4.2
*   Django REST Framework
*   Celery (for asynchronous tasks)
*   Redis (for Celery broker and result backend)
*   PostgreSQL (database)
*   Docker
*   Docker Compose

## Prerequisites

Before you begin, ensure you have the following installed:

*   Docker: [https://www.docker.com/get-started](https://www.docker.com/get-started)
*   Docker Compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## Installation and Setup

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd <your_project_directory>
    ```

2.  **Build and run the containers:**

    ```bash
    docker-compose up --build
    ```

    This command will:

    *   Build the Docker images for the web, Celery worker, Celery beat, Redis, and PostgreSQL services.
    *   Start all the containers in detached mode.

3.  **Apply database migrations:**

    Open a new terminal and execute the following command to apply the database migrations:

    ```bash
    docker-compose exec newtestwork_web_1 python manage.py migrate
    ```

4.  **Create a superuser (optional):**

    If you want to access the Django admin panel, create a superuser:

    ```bash
    docker-compose exec newtestwork_web_1 python manage.py createsuperuser
    docker-compose exec newtestwork_web_1 python manage.py drf_create_token # for auth from token
    ```

5.  **Access the API:**

    The API will be available at `http://localhost:8000`.

## API Endpoints

*   `/api/tables/tables/` : Manages the tables.
*   `/api/reservation/reservations/` : Manages the reservations.

## Celery Beat Schedule

The following Celery tasks are scheduled:

*   `update_tables_busyness_task`: Runs every 60 seconds to update table availability and reservation statuses.
*   `delete_old_reservations_task`: Runs daily to delete reservations older than 3 months.

## Notes

*   The application uses `Europe/Moscow` timezone by default.
*   The database is persistent using Docker volumes.