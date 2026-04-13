# Abia Arise Backend

Django REST API backend for the Abia Arise political movement website.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- Virtual environment

### Installation

1. **Navigate to backend folder:**
```bash
cd backend
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create .env file for database configuration:**
```bash
# .env file in backend folder
DATABASE_NAME=abia_arise_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Create superuser (admin account):**
```bash
python manage.py createsuperuser
```

7. **Run development server:**
```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`
Admin panel: `http://localhost:8000/admin`

## API Endpoints

### Authentication/Accounts
- `POST /api/auth/members/register/` - Register individual member
- `POST /api/auth/members/check_duplicate/` - Check NIN/phone duplicates
- `POST /api/auth/members/login/` - Individual member login
- `POST /api/auth/groups/register/` - Register pro-group
- `POST /api/auth/groups/login/` - Pro-group login
- `GET /api/auth/group-members/` - List group members
- `POST /api/auth/group-members/add_member/` - Add member to group

### Core Content
- `GET /api/core/achievements/` - List achievements
- `POST /api/core/achievements/` - Create achievement (admin)
- `GET /api/core/news/` - List news
- `POST /api/core/news/` - Create news (admin)

## Database Models

### IndividualMember
- Personal identification, contact, location, and origin information
- Auto-generated Abia Arise ID
- Profile picture support

### ProGroup
- Group information with chairman and secretary details
- Auto-generated Group License Number
- Members database file upload support

### GroupMember
- Links members to pro-groups
- Supports roles: chairman, secretary, member
- Star indicator for dual membership

### Achievement & News
- Content management for homepage sections

## Features

✅ Individual member registration with NIN/phone validation
✅ Pro-group registration with file upload
✅ Member authentication (ID + last 4 digits of phone)
✅ Group member management
✅ Achievement and news management
✅ CORS enabled for frontend communication
✅ File upload for passports and member databases

## Next Steps

1. Set up PostgreSQL database
2. Configure environment variables
3. Run migrations
4. Create admin user
5. Connect with React frontend on port 3000
