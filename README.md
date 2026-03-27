# User Management API

Simple REST API for managing users. Provides endpoints to create, read, update and delete (or deactivate) users with input validation and consistent responses.

Note: This README is intentionally written in English to follow common open-source practices and enable broader collaboration.

## Features

- Create users with validated input
- List users with optional pagination/filters
- Get user by ID
- Update user data (partial updates supported)
- Delete or deactivate users
- Consistent error handling and status codes

## Tech Stack

- Language: Python
- Database: PostgreSQL
- Tooling: Git + GitHub, Postman

## API Overview

- POST `/users` — Create a new user
  - Example body:
    ```json
    {
      "name": "Jane Doe",
      "email": "jane.doe@example.com",
      "password": "your-strong-password"
    }
    ```
- GET `/users` — List users (supports basic filtering/pagination)
- GET `/users/{id}` — Get a user by ID
- PATCH `/users/{id}` — Update one or more fields
- DELETE `/users/{id}` — Delete or deactivate a user

## Getting Started (local)

1) Clone the repository
   ```bash
   git clone https://github.com/will-csc/User-Management-Api
   cd User-Management-Api
   ```
2) Create a virtual environment and install dependencies
   ```bash
   # Windows (PowerShell)
   py -m venv .venv
   .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```
3) Configure environment variables (examples)
   - `DATABASE_URL=postgresql://user:password@localhost:5432/your_db`
   - `PORT=8000`
4) Run the application
   - Use the project's main entry point (e.g., `python app.py`) or your chosen framework's runner.
5) Test with Postman/Insomnia or via automated tests if available.

## Project Status

Initial scope includes core CRUD plus basic validation. Additional features (authentication, advanced filtering, soft delete, etc.) can be added as needed.

## Team

- João Vitor de Morais Timotio — 103916
- Eduardo Oliveira Silva — 106462
- Gabriel Cardoso Pereira — 106415
- Sabrina Paes Novais — 106490
- William Cesar Silva de Carvalho — 105637

Group: Lost Birds

## Contributing

Issues and pull requests are welcome. Please open a discussion before major changes.

## License

Choose and state a license here (e.g., MIT).
