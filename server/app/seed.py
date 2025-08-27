from app import create_app, db
from app.models.user import User

def seed_data():
    app = create_app()
    with app.app_context():
        User.query.delete()
        db.session.commit()
        
        organizer1 = User(username='KenyaEvents', email='contact@kenyaevents.co.ke', role='organizer')
        organizer1.set_password('password123')
        
        attendee1 = User(username='TestAttendee', email='attendee@test.com', role='attendee')
        attendee1.set_password('password123')

        db.session.add_all([organizer1, attendee1])
        db.session.commit()
        print("Database seeded with users! 🌱")

if __name__ == '__main__':
    seed_data()