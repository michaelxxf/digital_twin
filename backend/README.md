# Digital Twin System Backend

A comprehensive backend system for the Digital Twin System Administrator Simulation platform.

## Features

- **User Authentication & Authorization**: JWT-based authentication with role-based access control
- **Real-time Monitoring**: WebSocket-based real-time activity monitoring and alerts
- **Activity Logging**: Comprehensive activity tracking and logging system
- **Admin Dashboard**: Complete admin interface with user management and system monitoring
- **Staff Management**: Staff-specific operations and department management
- **Security Alerts**: Real-time security threat detection and alerting

## Prerequisites

- Python 3.8+
- MySQL/MariaDB (XAMPP recommended)
- Virtual environment (recommended)

## Installation

1. **Clone the repository and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - Start XAMPP and ensure MySQL is running
   - Create a database named `digital_twin`
   - Update database credentials in `app/database.py` if needed

5. **Initialize Database**
   ```bash
   python -m app.init_db
   ```

## Running the Application

### Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## Default Users

The system creates these default users on initialization:

- **Admin**: username: `admin`, password: `admin123`
- **Staff**: username: `staff1`, password: `staff123`
- **User**: username: `user1`, password: `user123`

## API Endpoints

### Authentication
- `POST /token` - Login and get access token
- `POST /register` - Register new user

### Admin Routes (`/admin`)
- `GET /dashboard/stats` - Get dashboard statistics
- `GET /users` - Get all users
- `GET /users/{user_id}` - Get specific user
- `PUT /users/{user_id}/status` - Update user status
- `DELETE /users/{user_id}` - Delete user
- `GET /security/alerts` - Get security alerts
- `POST /staff/create` - Create staff user
- `GET /analytics/activities` - Get activity analytics

### Staff Routes (`/staff`)
- `GET /profile` - Get staff profile
- `PUT /profile/department` - Update department
- `GET /department/stats` - Get department statistics
- `GET /activity/summary` - Get activity summary
- `GET /performance/metrics` - Get performance metrics

### Activity Routes (`/activity`)
- `POST /log` - Log new activity
- `GET /user/{user_id}` - Get user activities
- `GET /all` - Get all activities (admin only)
- `GET /suspicious` - Get suspicious activities
- `GET /summary` - Get activity summary

### WebSocket
- `WS /ws/{client_type}` - Real-time communication
  - `client_type`: `admin`, `staff`, or `users`

## Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://root:@localhost:3306/digital_twin
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control
- Activity logging and monitoring
- Real-time security alerts
- Input validation and sanitization

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `hashed_password`
- `is_active`
- `role` (user, staff, admin)
- `created_at`

### Staff Table
- `id` (Primary Key)
- `user_id` (Foreign Key to Users)
- `department`

### Admin Table
- `id` (Primary Key)
- `user_id` (Foreign Key to Users)
- `privileges`

### Activity Logs Table
- `id` (Primary Key)
- `user_id` (Foreign Key to Users)
- `action`
- `timestamp`
- `details`

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL is running in XAMPP
   - Check database credentials in `database.py`
   - Verify database `digital_twin` exists

2. **Import Errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **Port Already in Use**
   - Change port in uvicorn command: `--port 8001`
   - Or kill existing process using the port

4. **Permission Errors**
   - Ensure proper file permissions
   - Run as administrator if needed (Windows)

## Development

### Adding New Features

1. Create new models in `app/models.py`
2. Add corresponding schemas in `app/schemas.py`
3. Implement business logic in appropriate module
4. Create API routes in `app/routes/`
5. Update main.py to include new routes

### Testing

```bash
# Run tests (when implemented)
pytest

# Check code coverage
pytest --cov=app
```

## License

This project is part of the Digital Twin System Administrator Simulation platform.
