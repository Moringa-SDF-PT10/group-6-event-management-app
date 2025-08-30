from app import create_app, db
from app.models import User, Event, Category, Ticket
from datetime import datetime, timedelta

def seed_data():
    """Seeds the database with initial data."""
    app = create_app()
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Ticket.query.delete()
        Event.query.delete()
        Category.query.delete()
        User.query.delete()
        db.session.commit()
        
        # Create users
        organizer1 = User(
            first_name='Kenya',
            last_name='Events',
            phone_number='123-456-7890',
            username='KenyaEvents', 
            email='contact@kenyaevents.co.ke', 
            role='organizer'
        )
        organizer1.set_password('password123')
        
        organizer2 = User(
            first_name='Nairobi',
            last_name='Entertainment',
            phone_number='555-123-4567',
            username='NairobiEntertainment', 
            email='info@nrbentertainment.com', 
            role='organizer'
        )
        organizer2.set_password('password123')
        
        attendee1 = User(
            first_name='Test',
            last_name='Attendee',
            phone_number='098-765-4321',
            username='TestAttendee', 
            email='attendee@test.com', 
            role='attendee'
        )
        attendee1.set_password('password123')
        
        attendee2 = User(
            first_name='Jane',
            last_name='Doe',
            phone_number='111-222-3333',
            username='JaneDoe', 
            email='jane@example.com', 
            role='attendee'
        )
        attendee2.set_password('password123')

        db.session.add_all([organizer1, organizer2, attendee1, attendee2])
        db.session.commit()
        
        # Create categories
        categories_data = [
            'Music', 'Technology', 'Business', 'Arts', 'Sports', 
            'Food & Drink', 'Education', 'Health', 'Fashion', 'Travel'
        ]
        
        categories = []
        for cat_name in categories_data:
            category = Category(name=cat_name)
            categories.append(category)
            db.session.add(category)
        
        db.session.commit()
        
        # Create events
        events_data = [
            {
                'title': 'Nairobi Tech Conference 2025',
                'description': 'Join us for the biggest tech conference in East Africa. Learn about the latest trends in AI, blockchain, and mobile development.',
                'date': datetime.now() + timedelta(days=30),
                'location': 'KICC, Nairobi',
                'price': 5000.0,
                'image_url': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800',
                'organizer': organizer1,
                'categories': [categories[1], categories[6]]  # Technology, Education
            },
            {
                'title': 'Safaricom Jazz Festival',
                'description': 'Experience the best of local and international jazz artists in an unforgettable evening of music.',
                'date': datetime.now() + timedelta(days=45),
                'location': 'Carnivore Grounds, Nairobi',
                'price': 3000.0,
                'image_url': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800',
                'organizer': organizer2,
                'categories': [categories[0]]  # Music
            },
            {
                'title': 'Startup Pitch Competition',
                'description': 'Watch innovative startups pitch their ideas to top investors. Network with entrepreneurs and venture capitalists.',
                'date': datetime.now() + timedelta(days=20),
                'location': 'iHub, Nairobi',
                'price': 1500.0,
                'image_url': 'https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800',
                'organizer': organizer1,
                'categories': [categories[2], categories[1]]  # Business, Technology
            },
            {
                'title': 'Nairobi Food & Wine Festival',
                'description': 'Celebrate the flavors of Kenya with top chefs, local farmers, and wine makers from around the world.',
                'date': datetime.now() + timedelta(days=60),
                'location': 'Uhuru Gardens, Nairobi',
                'price': 2500.0,
                'image_url': 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800',
                'organizer': organizer2,
                'categories': [categories[5]]  # Food & Drink
            },
            {
                'title': 'Digital Marketing Masterclass',
                'description': 'Learn from industry experts about social media marketing, SEO, and digital advertising strategies.',
                'date': datetime.now() + timedelta(days=15),
                'location': 'Strathmore University, Nairobi',
                'price': 4000.0,
                'image_url': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800',
                'organizer': organizer1,
                'categories': [categories[2], categories[6]]  # Business, Education
            },
            {
                'title': 'Nairobi Art Gallery Opening',
                'description': 'Discover contemporary African art at the opening of our new gallery featuring local and international artists.',
                'date': datetime.now() + timedelta(days=10),
                'location': 'Nairobi National Museum',
                'price': 1000.0,
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
                'organizer': organizer2,
                'categories': [categories[3]]  # Arts
            }
        ]
        
        events = []
        for event_data in events_data:
            event = Event(
                title=event_data['title'],
                description=event_data['description'],
                date=event_data['date'],
                location=event_data['location'],
                price=event_data['price'],
                image_url=event_data['image_url'],
                organizer_id=event_data['organizer'].id
            )
            event.categories = event_data['categories']
            events.append(event)
            db.session.add(event)
        
        db.session.commit()
        
        # Create some sample tickets
        tickets_data = [
            {'user': attendee1, 'event': events[0], 'ticket_type': 'Regular'},
            {'user': attendee1, 'event': events[1], 'ticket_type': 'VIP'},
            {'user': attendee2, 'event': events[2], 'ticket_type': 'Regular'},
            {'user': attendee2, 'event': events[5], 'ticket_type': 'Regular'},
        ]
        
        for ticket_data in tickets_data:
            ticket = Ticket(
                user_id=ticket_data['user'].id,
                event_id=ticket_data['event'].id,
                ticket_type=ticket_data['ticket_type']
            )
            db.session.add(ticket)
        
        db.session.commit()
        
        print("Database seeded successfully! 🌱")
        print(f"Created {len([organizer1, organizer2, attendee1, attendee2])} users")
        print(f"Created {len(categories)} categories")
        print(f"Created {len(events)} events")
        print(f"Created {len(tickets_data)} tickets")

if __name__ == '__main__':
    seed_data()