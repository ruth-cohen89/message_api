# Message API

The Message API is a Django-based application designed to facilitate communication between users by allowing them to send messages to each other. It utilizes MySQL as the database management system.

## Features

- **User Authentication:** Users can register, login, and authenticate themselves to send and receive messages.
- **Message Sending:** Authenticated users can send messages to other users.
- **Message Retrieval:** Users can retrieve messages sent to them.
- **Message History:** Users can view their message history.
- **Database Integration:** Utilizes MySQL to store user information and messages.

## Getting Started

To get started with the Message API, follow these steps:

1. **Installation:** Clone the repository from GitHub:
    ```bash
    git clone https://github.com/yourusername/message-api.git
    ```

2. **Database Setup:** Set up MySQL database and configure database settings in Django settings file.

3. **Environment Setup:** Create a virtual environment and install dependencies from requirements.txt:
    ```bash
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4. **Database Migration:** Run database migrations to create necessary tables:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run Server:** Start the Django development server:
    ```bash
    python manage.py runserver
    ```

6. **API Documentation:** Explore the API endpoints and their usage through the provided documentation.

## API Documentation

For detailed documentation on available endpoints and their usage, refer to the API documentation provided within the project or visit `/api/docs/` after running the server.

## Database Schema

The database schema includes tables for users and messages. Here's a simplified representation:

- **User Table:**
  - id (Primary Key)
  - username
  - email
  - password

- **Message Table:**
  - id (Primary Key)
  - sender_id (Foreign Key to User)
  - receiver_id (Foreign Key to User)
  - content
  - timestamp

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for any improvements, bug fixes, or new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to customize this README according to your project's specific details and requirements.
