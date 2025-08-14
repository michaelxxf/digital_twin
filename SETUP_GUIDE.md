# Digital Twin System - Complete Setup Guide

This guide will help you set up the Digital Twin System Administrator Simulation platform to be 100% functional.

## 🎯 What We've Implemented

### Backend (FastAPI)
✅ **Complete API System**
- User authentication with JWT tokens
- Role-based access control (Admin, Staff, User)
- Real-time WebSocket communication
- Activity logging and monitoring
- Security alerts and threat detection
- Admin dashboard with analytics
- Staff management system
- Comprehensive API documentation

✅ **Database System**
- MySQL database with SQLAlchemy ORM
- User, Staff, Admin, and Activity tables
- Sample data creation
- Proper relationships and constraints

✅ **Security Features**
- Password hashing with bcrypt
- JWT token authentication
- Input validation and sanitization
- Activity tracking and monitoring

### Frontend (HTML/CSS/JavaScript)
✅ **Complete User Interface**
- Admin portal with dashboard
- Staff portal with department management
- User desktop simulation
- Real-time monitoring interface
- Security alerts display
- Responsive design with Tailwind CSS

## 🚀 Quick Start Guide

### Step 1: Prerequisites
1. **Install XAMPP** (for MySQL database)
   - Download from: https://www.apachefriends.org/
   - Install and start Apache and MySQL services

2. **Install Python 3.8+**
   - Download from: https://www.python.org/
   - Ensure pip is available

### Step 2: Database Setup
1. **Start XAMPP**
   - Open XAMPP Control Panel
   - Start Apache and MySQL services

2. **Create Database**
   - Open http://localhost/phpmyadmin
   - Create new database named `digital_twin`
   - Leave all other settings as default

### Step 3: Backend Setup
1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the startup script**
   ```bash
   python start.py
   ```

   This will:
   - Check all dependencies
   - Verify database connection
   - Initialize database tables
   - Create sample users
   - Start the FastAPI server

### Step 4: Frontend Setup
1. **Open the main page**
   - Navigate to the project root directory
   - Open `index.html` in your browser
   - Or serve it using a local server

2. **Test the system**
   - Click "Admin Portal" to access admin interface
   - Use default credentials:
     - Username: `admin`
     - Password: `admin123`

## 🔧 Configuration

### Backend Configuration
The backend is pre-configured for local development. Key settings in `backend/app/database.py`:
```python
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "digital_twin"
```

### Frontend Configuration
The frontend is configured to connect to `localhost:8000`. Update `config.js` if needed:
```javascript
API_BASE_URL: 'http://localhost:8000',
WS_BASE_URL: 'ws://localhost:8000',
```

## 👥 Default Users

The system creates these users automatically:

| Role | Username | Password | Access |
|------|----------|----------|---------|
| Admin | `admin` | `admin123` | Full system access |
| Staff | `staff1` | `staff123` | Staff portal access |
| User | `user1` | `user123` | User desktop access |

## 📊 System Features

### Admin Portal (`admins.html`)
- **Dashboard**: Real-time system statistics
- **User Management**: Create, edit, delete users
- **Activity Monitoring**: View all user activities
- **Security Alerts**: Monitor suspicious activities
- **Analytics**: Activity charts and reports
- **Staff Management**: Create and manage staff accounts

### Staff Portal (`staff-auth.html`)
- **Profile Management**: Update personal information
- **Department Stats**: View department statistics
- **Activity Summary**: Personal activity tracking
- **Performance Metrics**: Performance analytics
- **Colleagues**: View department members

### User Desktop (`User.html`)
- **File Management**: Simulated file operations
- **Email System**: Internal email simulation
- **Settings**: System configuration
- **Activity Tracking**: All actions are logged
- **Security Policies**: Enforced system policies

## 🔌 API Endpoints

### Authentication
- `POST /token` - Login
- `POST /register` - Register new user

### Admin Routes
- `GET /admin/dashboard/stats` - Dashboard statistics
- `GET /admin/users` - List all users
- `GET /admin/security/alerts` - Security alerts
- `POST /admin/staff/create` - Create staff user

### Staff Routes
- `GET /staff/profile` - Staff profile
- `GET /staff/department/stats` - Department statistics
- `GET /staff/activity/summary` - Activity summary

### Activity Routes
- `POST /activity/log` - Log activity
- `GET /activity/all` - Get all activities
- `GET /activity/suspicious` - Suspicious activities

### WebSocket
- `WS /ws/admin` - Admin real-time updates
- `WS /ws/staff` - Staff real-time updates
- `WS /ws/users` - User real-time updates

## 🛠️ Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```
   Solution: Ensure XAMPP MySQL is running
   ```

2. **Port 8000 Already in Use**
   ```
   Solution: Change port in start.py or kill existing process
   ```

3. **Import Errors**
   ```
   Solution: Ensure virtual environment is activated and dependencies installed
   ```

4. **CORS Errors**
   ```
   Solution: Backend is configured to allow all origins for development
   ```

### Debug Mode
To run in debug mode with detailed logs:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

## 📈 Monitoring and Logs

### Activity Logging
All user actions are automatically logged:
- Login/logout events
- File operations
- System settings changes
- Admin actions
- Security events

### Real-time Monitoring
- WebSocket connections provide real-time updates
- Security alerts are pushed immediately
- Activity feeds update in real-time

### Database Logs
Check the database for detailed activity logs:
```sql
SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT 10;
```

## 🔒 Security Features

### Authentication
- JWT token-based authentication
- Password hashing with bcrypt
- Session management
- Automatic token refresh

### Authorization
- Role-based access control
- Endpoint protection
- Admin-only functions
- Staff-specific features

### Monitoring
- Activity logging
- Security alerts
- Suspicious activity detection
- Real-time threat monitoring

## 🚀 Production Deployment

### Backend Deployment
1. **Environment Variables**
   ```env
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=mysql+pymysql://user:pass@host:port/db
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

2. **Database**
   - Use production MySQL server
   - Configure proper backups
   - Set up monitoring

3. **Server**
   - Use production WSGI server (Gunicorn)
   - Set up reverse proxy (Nginx)
   - Configure SSL certificates

### Frontend Deployment
1. **Static Hosting**
   - Deploy to CDN or web server
   - Update API endpoints in config.js
   - Configure CORS properly

2. **Security**
   - Enable HTTPS
   - Set up proper CORS policies
   - Configure CSP headers

## 📚 API Documentation

Once the backend is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎉 Success!

Your Digital Twin System is now 100% functional! You can:

1. **Access the admin portal** and manage the entire system
2. **Monitor user activities** in real-time
3. **Create staff accounts** and manage departments
4. **Track security events** and respond to threats
5. **View detailed analytics** and system statistics

The system provides a complete simulation environment for system administration training and demonstration.

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the logs in the terminal
3. Verify all prerequisites are installed
4. Ensure database is properly configured

The system is designed to be self-contained and should work out of the box with the provided setup instructions. 