# 🎫 Event Management & Ticketing System

A full-stack event management and ticketing platform built with Flask (backend) and React (frontend). This system serves two primary user roles: **Attendees** who can browse and purchase event tickets, and **Organizers** who can create and manage events.

## 🌟 Features

### 👥 For Attendees
- 📝 Register and manage account
- 🔐 Secure login/logout
- 🏠 Browse events on homepage
- 🔍 Search events by title
- 🏷️ Filter events by category
- 📋 View detailed event information
- 🎟️ Purchase tickets through modal confirmation
- 📊 Personal dashboard to view purchased tickets

### 🎪 For Organizers
- 📝 Register as an organizer
- 🔐 Secure login/logout
- 📊 Customized organizer dashboard
- ➕ Create new events with full details
- 📝 Edit existing events
- 🗑️ Delete events
- 📈 Monitor event management

## 🛠️ Tech Stack

### Backend
- 🐍 **Python Flask** - Web framework
- 🗄️ **SQLAlchemy** - ORM for database operations
- 🔒 **Flask-Bcrypt** - Password hashing
- 🌐 **Flask-CORS** - Cross-origin resource sharing
- 📦 **SQLite** - Database (development)

### Frontend
- ⚛️ **React** - UI framework
- 🛣️ **React Router** - Client-side routing
- 📝 **Formik + Yup** - Form handling and validation
- 🎨 **CSS/SCSS** - Styling
- 🔗 **Axios** - HTTP client

## 📂 Project Structure

### 🖥️ Backend Structure
```
server/
├── 🔧 .env
├── 📋 requirements.txt
├── 🚀 app.py
├── 📁 instance/
│   └── 🗄️ app.db
├── 📁 migrations/
└── 📁 app/
    ├── 🐍 __init__.py
    ├── ⚙️ config.py
    ├── 🌱 seed.py
    ├── 📁 models/
    │   ├── 🐍 __init__.py
    │   ├── 👤 user.py
    │   ├── 🎪 event.py
    │   ├── 🎫 ticket.py
    │   ├── 🏷️ category.py
    │   └── 🔗 associations.py
    └── 📁 routes/
        ├── 🐍 __init__.py
        ├── 🔐 auth_routes.py
        ├── 🎪 event_routes.py
        ├── 👤 user_routes.py
        └── 🏷️ category_routes.py
```

### 🌐 Frontend Structure
```
client/
├── 🔧 .env
├── 📖 README.md
├── 📁 public/
│   └── 🌐 index.html
└── 📁 src/
    ├── ⚛️ App.js
    ├── 🚀 index.js
    ├── 📁 api/
    ├── 📁 components/
    │   ├── 🧭 NavBar.js
    │   ├── 🎪 EventCard.js
    │   ├── 📝 EventForm.js
    │   ├── 🔐 AuthForm.js
    │   ├── 🎫 TicketCard.js
    │   ├── ➕ CreateEventModal.js
    │   ├── ✏️ EditEventModal.js
    │   └── 🗑️ DeleteConfirmationModal.js
    ├── 📁 context/
    │   └── 🔐 AuthContext.js
    └── 📁 pages/
        ├── 🏠 HomePage.js
        ├── 📊 DashboardPage.js
        └── 🔐 LoginPage.js
```

## 🗄️ Database Schema

### 👤 Users Table
- 🆔 `id` - Primary key
- 👤 `username` - Unique display name
- 📧 `email` - Unique email for login
- 🔒 `_password_hash` - Encrypted password
- 🎭 `role` - User type ('attendee' or 'organizer')
- 📅 `created_at` - Account creation timestamp

### 🎪 Events Table
- 🆔 `id` - Primary key
- 📝 `title` - Event name
- 📄 `description` - Event details
- 📅 `date` - Event date and time
- 📍 `location` - Event venue
- 💰 `price` - Ticket price
- 🖼️ `image_url` - Event banner image
- 👤 `organizer_id` - Foreign key to users
- 📅 `created_at` - Creation timestamp

### 🎫 Tickets Table
- 🆔 `id` - Primary key
- 🏷️ `ticket_type` - Type of ticket
- 📅 `purchase_date` - Purchase timestamp
- 👤 `user_id` - Foreign key to users
- 🎪 `event_id` - Foreign key to events

### 🏷️ Categories Table
- 🆔 `id` - Primary key
- 📝 `name` - Category name

### 🔗 Event Categories (Association Table)
- 🎪 `event_id` - Foreign key to events
- 🏷️ `category_id` - Foreign key to categories

## 🛣️ Routes

### 🌐 Client-Side Routes
| Route | 📄 Page | 🔒 Access |
|-------|---------|-----------|
| `/login` | 🔐 Login/Register | Public |
| `/` | 🏠 Homepage | Public |
| `/events` | 🎪 All Events | Public |
| `/events/:id` | 📋 Event Details | Public |
| `/events/new` | ➕ Create Event | Organizer Only |
| `/events/:id/edit` | ✏️ Edit Event | Organizer Only |
| `/dashboard` | 📊 User Dashboard | Authenticated |

## ✅ Form Validation

### 🔐 Authentication Forms
- 📧 **Email**: Valid email format required
- 🔒 **Password**: Minimum length + special character requirement

### 🎪 Event Forms
- ✅ **Required Fields**: All fields must be completed
- 📅 **Date Validation**: Future dates only
- 👥 **Capacity**: Must be ≥ 0

### 🎫 Ticket Purchase Forms
- 🏷️ **Ticket Type**: Required selection
- 🔢 **Quantity**: Must be > 0
- ✅ **Capacity Check**: Verify availability

## 🌐 Deployment

### 🚀 Live Application

**[Event Horizons](https://group-6-event-management-app-tfpl.onrender.com/)** 

## 🚀 Getting Started

### 📋 Prerequisites
- 🐍 Python 3.8+
- 📦 Node.js 14+
- 📦 npm or yarn

### 🔧 Backend Setup
1. Navigate to server directory:
   ```bash
   cd server
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env`:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///instance/app.db
   ```

5. Initialize database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Seed the database (optional):
   ```bash
   python app/seed.py
   ```

7. Run the server:
   ```bash
   flask run
   ```

### 🌐 Frontend Setup
1. Navigate to client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables in `.env`:
   ```env
   REACT_APP_API_BASE_URL=http://localhost:5000
   ```

4. Start the development server:
   ```bash
   npm start
   ```

## 📚 API Endpoints

### 🔐 Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/check` - Check authentication status

### 🎪 Events
- `GET /events` - Get all events (with optional filters)
- `GET /events/:id` - Get single event
- `POST /events` - Create new event (organizer only)
- `PUT /events/:id` - Update event (organizer only)
- `DELETE /events/:id` - Delete event (organizer only)

### 🎫 Tickets
- `GET /tickets` - Get user's tickets
- `POST /tickets` - Purchase ticket
- `GET /events/:id/tickets` - Get event tickets (organizer only)

### 🏷️ Categories
- `GET /categories` - Get all categories

### 👤 Users
- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update user profile

## 🎯 MVP User Stories Checklist

### ✅ Attendee Features
- [ ] 📝 Account registration as attendee
- [ ] 🔐 Secure login/logout
- [ ] 🏠 Browse events on homepage
- [ ] 🔍 Search events by title
- [ ] 🏷️ Filter events by category
- [ ] 📋 View detailed event information
- [ ] 🎫 Purchase tickets via modal
- [ ] 📊 View purchased tickets on dashboard

### ✅ Organizer Features
- [ ] 📝 Account registration as organizer
- [ ] 🔐 Secure login/logout
- [ ] 📊 Access organizer dashboard
- [ ] ➕ Create new events
- [ ] 📝 View created events
- [ ] ✏️ Update event details
- [ ] 🗑️ Delete events

## 🤝 Contributing
1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. 💻 Make your changes
4. ✅ Test thoroughly
5. 📤 Submit a pull request

---

Built by Group 6 with ❤️ using Flask and React