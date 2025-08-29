from app import create_app, db
from app.models.event import Event
from app.models.category import Category
from datetime import datetime, timedelta
import os

def clear_data():
    
    print("Clearing existing data...")
    db.drop_all()
    db.create_all()
    print("✅ Database cleared and tables recreated")

def create_categories():
    
    print("📂 Creating categories...")
    
    categories_data = [
        {
            'name': 'Music & Concerts',
            'description': 'Live music performances, concerts, and music festivals',
            'slug': 'mziki-Genge'
        },
        {
            'name': 'Technology',
            'description': 'Tech conferences, workshops, hackathons, and meetups',
            'slug': 'tech-shujaa'
        },
        {
            'name': 'Sports & Fitness',
            'description': 'Sporting events, tournaments, marathons, and fitness activities',
            'slug': 'sports-fitness'
        },
        {
            'name': 'Business & Networking',
            'description': 'Business conferences, networking events, and entrepreneurship',
            'slug': 'business-networking'
        },
        {
            'name': 'Arts & Culture',
            'description': 'Cultural festivals, art exhibitions, theater, and cultural events',
            'slug': 'arts-culture'
        },
        {
            'name': 'Food & Drink',
            'description': 'Food festivals, wine tastings, and culinary experiences',
            'slug': 'food-drink'
        },
        {
            'name': 'Education & Workshops',
            'description': 'Educational seminars, workshops, and training sessions',
            'slug': 'education-workshops'
        },
        {
            'name': 'Community & Social',
            'description': 'Community gatherings, charity events, and social activities',
            'slug': 'community-social'
        }
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
    
    print("🎪 Creating events...")
    
    events_data = [
        {
            'title': 'Nairobi Tech Summit 2024',
            'description': 'The largest technology conference in East Africa featuring keynotes on artificial intelligence, blockchain technology, fintech innovations, and digital transformation. Join over 5,000 tech enthusiasts, entrepreneurs, and investors for three days of networking, learning, and innovation.',
            'short_description': 'East Africa\'s largest tech conference featuring AI, blockchain, and fintech innovations.',
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
            'description': 'The premier international rugby sevens tournament in Kenya, attracting teams from around the world. Experience world-class rugby action in the heart of Nairobi with food, entertainment, and the famous Safari Sevens atmosphere.',
            'short_description': 'International rugby sevens tournament with world-class teams and entertainment.',
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
        {
            'title': 'Ngemi Festival',
            'description': 'Kenya\'s premier outdoor music festival featuring a stellar lineup of local and international artists. Set against the stunning backdrop of Hell\'s Gate National Park, enjoy live performances, local cuisine, and craft vendors in this unique festival experience.',
            'short_description': 'Premier outdoor music festival with local and international artists in Hell\'s Gate.',
            'date': datetime.now() + timedelta(days=15),
            'location': 'Naivasha',
            'venue': 'Hell\'s Gate National Park',
            'price': 4500.0,
            'image_url': 'https://littleimages.blob.core.windows.net/movieproviders/movies//65C7BF07-B682-48F0-9823-39031BF710FE',
            'max_attendees': 8000,
            'slug': 'ngemi-festival-2025',
            'categories': ['music-concerts', 'arts-culture']
        },
        {
            'title': 'Tusker Oktoberfest Kenya',
            'description': 'Experience authentic German culture in the heart of Nairobi! Tusker Oktoberfest brings you traditional German beer, cuisine, live oompah bands, and entertainment. Dress in your best lederhosen and dirndls for this cultural celebration.',
            'short_description': 'Authentic German beer festival with traditional music, food, and entertainment.',
            'date': datetime.now() + timedelta(days=60),
            'end_date': datetime.now() + timedelta(days=62),
            'location': 'Nairobi',
            'venue': 'Carnivore Grounds',
            'price': 3000.0,
            'image_url': 'https://bazeonlineradio.co.ke/wp-content/uploads/2023/10/29th-October-2023-756x756.jpg',
            'max_attendees': 3000,
            'slug': 'tusker-oktoberfest-2025',
            'categories': ['food-drink', 'music-concerts', 'arts-culture']
        },
        {
            'title': 'Kenya Entrepreneurship Summit',
            'description': 'Connect with Kenya\'s most successful entrepreneurs, investors, and business leaders. This summit features panel discussions, pitch competitions, workshops on scaling businesses, and networking opportunities that could transform your entrepreneurial journey.',
            'short_description': 'Premier business summit connecting entrepreneurs with investors and industry leaders.',
            'date': datetime.now() + timedelta(days=25),
            'location': 'Nairobi',
            'venue': 'Strathmore University Business School',
            'price': 8000.0,
            'image_url': 'https://businesssummit.net/wp-content/uploads/2025/02/Investors-Summit-Kenya-2025-Banner-scaled.jpg',
            'max_attendees': 1000,
            'slug': 'kenya-entrepreneurship-summit-2025',
            'categories': ['business-networking', 'education-workshops']
        },
        {
            'title': 'Lamu Cultural Festival',
            'description': 'Celebrate the rich Swahili culture and heritage of Kenya\'s coast. Experience traditional dhow races, Swahili poetry, local crafts, historical tours, and authentic coastal cuisine in the UNESCO World Heritage site of Lamu Old Town.',
            'short_description': 'Celebration of Swahili culture with traditional music, dance, crafts, and cuisine.',
            'date': datetime.now() + timedelta(days=90),
            'end_date': datetime.now() + timedelta(days=93),
            'location': 'Lamu',
            'venue': 'Lamu Old Town',
            'price': 2000.0,
            'image_url': 'https://www.kenyamoja.com/sites/default/files/styles/width_500px/public/events/posters/GAFa_LlWoAAdIep.jpeg?itok=5QvFnyed',
            'max_attendees': 2000,
            'slug': 'lamu-cultural-festival-2025',
            'categories': ['arts-culture', 'community-social']
        },
        {
            'title': 'Nairobi Restaurant Week',
            'description': 'A week-long celebration of Nairobi\'s diverse culinary scene. Over 100 restaurants participate offering special menus, cooking classes, wine pairings, and meet-the-chef events. Discover hidden gems and celebrate local and international cuisine.',
            'short_description': 'Week-long culinary celebration featuring 100+ restaurants with special menus.',
            'date': datetime.now() + timedelta(days=20),
            'end_date': datetime.now() + timedelta(days=27),
            'location': 'Nairobi',
            'venue': 'Various restaurants across Nairobi',
            'price': 0.0,  # Free to participate, individual restaurants charge
            'image_url': 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800',
            'slug': 'nairobi-restaurant-week-2025',
            'categories': ['food-drink', 'community-social']
        },
        {
            'title': 'Magical Kenya Open Golf Championship',
            'description': 'Part of the European Tour, this prestigious golf tournament attracts world-class golfers to the historic Muthaiga Golf Club. Watch professional golf at its finest while enjoying the clubhouse atmosphere and networking opportunities.',
            'short_description': 'European Tour golf championship with world-class professional golfers.',
            'date': datetime.now() + timedelta(days=120),
            'end_date': datetime.now() + timedelta(days=123),
            'location': 'Nairobi',
            'venue': 'Muthaiga Golf Club',
            'price': 2500.0,
            'image_url': 'https://awak.co.ke/wp-content/uploads/2025/02/IMG-20250207-WA0068.jpg',
            'max_attendees': 5000,
            'slug': 'magical-kenya-open-golf-2025',
            'categories': ['sports-fitness']
        },
        {
            'title': 'Nairobi Design Week',
            'description': 'Celebrating creativity and innovation in design across Kenya. Features exhibitions, workshops, talks by renowned designers, pop-up installations, and the annual Design Awards ceremony. Perfect for designers, artists, and creative professionals.',
            'short_description': 'Annual celebration of design featuring exhibitions, workshops, and awards.',
            'date': datetime.now() + timedelta(days=35),
            'end_date': datetime.now() + timedelta(days=42),
            'location': 'Nairobi',
            'venue': 'Various venues across Nairobi',
            'price': 1000.0,
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRaoaSD9XPg3ZfNNd-N07-Of7RkvTfjtKh4Aw&s',
            'slug': 'nairobi-design-week-2025',
            'categories': ['arts-culture', 'education-workshops']
        },
        {
            'title': 'Standard Chartered Nairobi Marathon',
            'description': 'East Africa\'s premier marathon event featuring full marathon, half marathon, 10K, and family fun runs. Join thousands of runners from around the world as they take on the streets of Nairobi for this IAAF-certified course.',
            'short_description': 'Premier marathon event with multiple race categories for all fitness levels.',
            'date': datetime.now() + timedelta(days=75),
            'location': 'Nairobi',
            'venue': 'Starting at Nyayo National Stadium',
            'price': 3500.0,
            'image_url': 'https://static.wixstatic.com/media/577345_e5dd29dbb28f4d989865760c81f7fe14~mv2.jpg/v1/fill/w_980,h_784,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/DSC00539.jpg',
            'max_attendees': 20000,
            'slug': 'nairobi-marathon-2025',
            'categories': ['sports-fitness', 'community-social']
        },
        {
            'title': 'African Blockchain Conference',
            'description': 'Leading blockchain and cryptocurrency conference in Africa. Features presentations on DeFi, NFTs, Web3, regulatory frameworks, and investment opportunities. Network with blockchain developers, crypto investors, and fintech innovators.',
            'short_description': 'Premier blockchain conference covering DeFi, NFTs, Web3, and crypto investments.',
            'date': datetime.now() + timedelta(days=50),
            'end_date': datetime.now() + timedelta(days=51),
            'location': 'Nairobi',
            'venue': 'Villa Rosa Kempinski',
            'price': 12000.0,
            'image_url': 'https://images.lumacdn.com/cdn-cgi/image/format=auto,fit=cover,dpr=2,anim=false,background=white,quality=75,width=500,height=500/event-covers/7r/8359eedb-6196-4196-974c-d811ba0bf6b3.jpg',
            'max_attendees': 800,
            'slug': 'african-blockchain-conference-2025',
            'categories': ['technology', 'business-networking']
        },
        {
            'title': 'Blankets & Wine Nairobi',
            'description': 'The ultimate Sunday afternoon experience combining great music, food, and vibes. Bring your blanket and enjoy performances by top local and regional artists while sampling gourmet food and drinks in a relaxed outdoor setting.',
            'short_description': 'Sunday afternoon music festival with great food, drinks, and relaxed vibes.',
            'date': datetime.now() + timedelta(days=10),
            'location': 'Nairobi',
            'venue': 'Uhuru Gardens',
            'price': 2200.0,
            'image_url': 'https://blanketsandwine.com/kenya/wp-content/uploads/2025/02/all-dates-25-e1739623303217.png',
            'max_attendees': 4000,
            'slug': 'blankets-wine-nairobi-2025',
            'categories': ['music-concerts', 'food-drink']
        }
    ]
    
    events = []
    for event_data in events_data:
        # Extract and convert category slugs to category objects
        category_slugs = event_data.pop('categories', [])
        event_categories = [categories[slug] for slug in category_slugs if slug in categories]
        
        # Create event
        event = Event(**event_data)
        event.categories = event_categories
        
        db.session.add(event)
        events.append(event)
    
    db.session.commit()
    print(f"✅ Created {len(events_data)} events")
    return events

def seed_database():
    
    app = create_app('development')
    
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        # Clear existing data
        clear_data()
        
        # Create categories
        categories = create_categories()
        
        # Create events
        events = create_events(categories)
        
        print(f"\n🎉 Seeding completed successfully!")
        print(f"📊 Summary:")
        print(f"   • Categories: {len(categories)}")
        print(f"   • Events: {len(events)}")
        print(f"   • Database: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == '__main__':
    seed_database()