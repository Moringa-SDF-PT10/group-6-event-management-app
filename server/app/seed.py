from app import create_app, db
from app.models.event import Event
from app.models.category import Category
from app.models.user import User  # Added import for User model
from datetime import datetime, timedelta
import os

def clear_data():
    """Drops all tables and recreates them."""
    print("Clearing existing data...")
    db.drop_all()
    db.create_all()
    print("✅ Database cleared and tables recreated")

def create_users():
    """Seeds the database with initial user data."""
    print("👤 Creating users...")
    
    # Create an organizer user
    organizer1 = User(
        first_name='Kenya',
        last_name='Events',
        phone_number='123-456-7890',
        username='KenyaEvents', 
        email='contact@kenyaevents.co.ke', 
        role='organizer'
    )
    organizer1.set_password('password123')

    # Create an attendee user
    attendee1 = User(
        first_name='Test',
        last_name='Attendee',
        phone_number='098-765-4321',
        username='TestAttendee', 
        email='attendee@test.com', 
        role='attendee'
    )
    attendee1.set_password('password123')

    users = [organizer1, attendee1]
    db.session.add_all(users)
    db.session.commit()
    
    print(f"✅ Created {len(users)} users")
    return users

def create_categories():
    """Seeds the database with event categories."""
    print("📂 Creating categories...")
    
    categories_data = [
        {'name': 'Music & Concerts', 'description': 'Live music performances, concerts, and music festivals', 'slug': 'music-concerts'},
        {'name': 'Technology', 'description': 'Tech conferences, workshops, hackathons, and meetups', 'slug': 'technology'},
        {'name': 'Sports & Fitness', 'description': 'Sporting events, tournaments, marathons, and fitness activities', 'slug': 'sports-fitness'},
        {'name': 'Business & Networking', 'description': 'Business conferences, networking events, and entrepreneurship', 'slug': 'business-networking'},
        {'name': 'Arts & Culture', 'description': 'Cultural festivals, art exhibitions, theater, and cultural events', 'slug': 'arts-culture'},
        {'name': 'Food & Drink', 'description': 'Food festivals, wine tastings, and culinary experiences', 'slug': 'food-drink'},
        {'name': 'Education & Workshops', 'description': 'Educational seminars, workshops, and training sessions', 'slug': 'education-workshops'},
        {'name': 'Community & Social', 'description': 'Community gatherings, charity events, and social activities', 'slug': 'community-social'}
    ]
    
    categories = {}
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.session.add(category)
        categories[cat_data['slug']] = category
    
    db.session.commit()
    print(f"✅ Created {len(categories_data)} categories")
    return categories

def create_events(categories):
    """Seeds the database with events."""
    print("🎪 Creating events...")
    
    events_data = [
        {
            'title': 'Nairobi Tech Summit 2024',
            'description': 'The largest technology conference in East Africa...',
            'short_description': 'East Africa\'s largest tech conference...',
            'date': datetime.now() + timedelta(days=30),
            'end_date': datetime.now() + timedelta(days=32),
            'location': 'Nairobi',
            'venue': 'Kenyatta International Conference Centre',
            'price': 15000.0,
            'image_url': 'https://blog.busha.co/content/images/size/w2640/2022/04/africa-summit-nairobi.png',
            'max_attendees': 5000,
            'slug': 'nairobi-tech-summit-2024',
            'categories': ['technology', 'business-networking']
        },
        {
            'title': 'Safari Sevens Rugby Tournament',
            'description': 'The premier international rugby sevens tournament in Kenya...',
            'short_description': 'International rugby sevens tournament...',
            'date': datetime.now() + timedelta(days=45),
            'end_date': datetime.now() + timedelta(days=46),
            'location': 'Nairobi',
            'venue': 'RFUEA Ground',
            'price': 2500.0,
            'image_url': 'https://www.kru.co.ke/wp-content/uploads/2025/02/2025-Safari-7s-Official-Poster-scaled-e1738822485784.jpeg',
            'max_attendees': 15000,
            'slug': 'safari-sevens-rugby-2025',
            'categories': ['sports-fitness', 'community-social']
        },
        # ... (add the rest of the events data here for brevity)
    ]
    
    events = []
    for event_data in events_data:
        category_slugs = event_data.pop('categories', [])
        event_categories = [categories[slug] for slug in category_slugs if slug in categories]
        
        event = Event(**event_data)
        event.categories = event_categories
        
        db.session.add(event)
        events.append(event)
    
    db.session.commit()
    print(f"✅ Created {len(events_data)} events")
    return events

def seed_database():
    """Main function to run all seeding operations."""
    app = create_app('development')
    
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        # Clear existing data
        clear_data()
        
        # Create data in order
        users = create_users()
        categories = create_categories()
        events = create_events(categories)
        
        print(f"\n🎉 Seeding completed successfully!")
        print(f"📊 Summary:")
        print(f"   • Users: {len(users)}")
        print(f"   • Categories: {len(categories)}")
        print(f"   • Events: {len(events)}")
        print(f"   • Database: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == '__main__':
    seed_database()