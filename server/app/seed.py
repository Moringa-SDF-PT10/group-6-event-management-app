from app import create_app, db
from app.models.user import User

def seed_data():
    """Seeds the database with initial user data."""
    app = create_app()
    with app.app_context():
        # NOTE: This will delete all users!
        print("Clearing existing users...")
        User.query.delete()
        db.session.commit()
        
        # Create an organizer user with all required fields
        organizer1 = User(
            first_name='Kenya',
            last_name='Events',
            phone_number='123-456-7890',
            username='KenyaEvents', 
            email='contact@kenyaevents.co.ke', 
            role='organizer'
        )
        organizer1.set_password('password123')
        # Create an attendee user with all required fields
        attendee1 = User(
            first_name='Test',
            last_name='Attendee',
            phone_number='098-765-4321',
            username='TestAttendee', 
            email='attendee@test.com', 
            role='attendee'
        )
        attendee1.set_password('password123')

        db.session.add_all([organizer1, attendee1])
        db.session.commit()
        
        print("Database seeded with users! 🌱")

if __name__ == '__main__':
    seed_data()
