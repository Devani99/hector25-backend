"""
Seed the database with realistic sample data for the Hector25 demo.

Usage:
    venv\Scripts\python manage.py seed_data

Creates:
  - 2 demo users (agent + buyer)
  - 8 properties (houses, apartments, villas, offices — buy/rent/new_launch)
  - amenities for each property
  - 4 community posts with comments and likes
  - 3 notifications
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from properties.models import Property, Amenity, Favorite
from community.models import Post, Comment, Like, Save
from notifications.models import Notification

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data for demo'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('\n🌱 Seeding Hector25 database...\n'))

        # ── Users ──────────────────────────────────────────────────────────────
        agent, _ = User.objects.get_or_create(
            email='agent@hector25.com',
            defaults={
                'username': 'agent_raj',
                'name': 'Raj Mehta',
                'phone': '+91 98765 43210',
                'bio': 'Senior property consultant with 10+ years of experience in real estate.',
                'is_agent': True,
            }
        )
        if _:
            agent.set_password('Agent@1234')
            agent.save()
            self.stdout.write(self.style.SUCCESS('  ✔ Agent user created: agent@hector25.com / Agent@1234'))

        buyer, _ = User.objects.get_or_create(
            email='buyer@hector25.com',
            defaults={
                'username': 'priya_buyer',
                'name': 'Priya Shah',
                'phone': '+91 91234 56789',
                'bio': 'First-time home buyer looking for a 3BHK.',
                'is_agent': False,
            }
        )
        if _:
            buyer.set_password('Buyer@1234')
            buyer.save()
            self.stdout.write(self.style.SUCCESS('  ✔ Buyer user created: buyer@hector25.com / Buyer@1234'))

        # ── Properties ─────────────────────────────────────────────────────────
        properties_data = [
            {
                'title': 'Modern 4BHK Family House',
                'description': 'A stunning modern family home with open-plan living, a large garden, and a double garage. Located in a quiet, tree-lined neighbourhood with excellent schools nearby.',
                'location': 'Bandra West, Mumbai',
                'price': 8500000,
                'type': 'House',
                'listing_type': 'buy',
                'bedrooms': 4, 'bathrooms': 3, 'area_sqft': 2500,
                'is_featured': True,
                'amenities': ['Swimming Pool', 'Garden', 'Garage', 'CCTV Security', 'Gym'],
            },
            {
                'title': 'Luxury 3BHK Apartment',
                'description': 'Premium high-rise apartment with panoramic city views. Features marble flooring, modular kitchen, and 24/7 security. Walking distance to metro station.',
                'location': 'Lower Parel, Mumbai',
                'price': 12000000,
                'type': 'Apartment',
                'listing_type': 'buy',
                'bedrooms': 3, 'bathrooms': 2, 'area_sqft': 1800,
                'is_featured': True,
                'amenities': ['Rooftop Pool', 'Gym', 'Club House', 'Power Backup', 'Concierge'],
            },
            {
                'title': 'Cozy 1BHK Studio Apartment',
                'description': 'Fully furnished studio apartment perfect for working professionals. Includes high-speed internet, air conditioning in all rooms, and weekly housekeeping.',
                'location': 'Andheri East, Mumbai',
                'price': 35000,
                'type': 'Apartment',
                'listing_type': 'rent',
                'bedrooms': 1, 'bathrooms': 1, 'area_sqft': 650,
                'is_featured': False,
                'amenities': ['Fully Furnished', 'WiFi', 'Air Conditioning', 'Housekeeping'],
            },
            {
                'title': 'Spacious 5BHK Sea-View Villa',
                'description': 'Breathtaking sea-facing villa with private pool. Ideal for large families or holiday rentals. Comes with staff quarters, home theatre, and landscaped garden.',
                'location': 'Alibaug, Maharashtra',
                'price': 25000000,
                'type': 'Villa',
                'listing_type': 'buy',
                'bedrooms': 5, 'bathrooms': 4, 'area_sqft': 4200,
                'is_featured': True,
                'amenities': ['Private Pool', 'Home Theatre', 'Staff Quarters', 'Sea View', 'Jacuzzi', 'Garden'],
            },
            {
                'title': 'Premium Office Space',
                'description': 'Grade-A fully furnished office space in the heart of the financial district. High-speed fibre internet, dedicated parking, 24/7 power backup, and meeting rooms included.',
                'location': 'BKC, Mumbai',
                'price': 150000,
                'type': 'Office',
                'listing_type': 'rent',
                'bedrooms': 0, 'bathrooms': 2, 'area_sqft': 3000,
                'is_featured': False,
                'amenities': ['Fibre Internet', 'Meeting Rooms', 'Cafeteria', 'Parking', 'Power Backup'],
            },
            {
                'title': 'New Launch: Smart 2BHK Apartment',
                'description': 'Brand new smart home apartment with IoT-enabled appliances. Early-bird pricing available. Ready to move in Q2 2025.',
                'location': 'Thane West, Mumbai',
                'price': 6500000,
                'type': 'Apartment',
                'listing_type': 'new_launch',
                'bedrooms': 2, 'bathrooms': 2, 'area_sqft': 1100,
                'is_featured': True,
                'amenities': ['Smart Home', 'EV Charging', 'Solar Power', 'Kids Play Area', 'Gym'],
            },
            {
                'title': '3BHK Independent House',
                'description': 'Independent house in a peaceful residential society. Comes with a private terrace and parking for 2 cars. No brokerage.',
                'location': 'Pune, Maharashtra',
                'price': 42000,
                'type': 'House',
                'listing_type': 'rent',
                'bedrooms': 3, 'bathrooms': 2, 'area_sqft': 1600,
                'is_featured': False,
                'amenities': ['Terrace', 'Parking', 'Garden', 'CCTV'],
            },
            {
                'title': 'New Launch: Luxury Sky Villa',
                'description': 'Ultra-luxury sky villa on the 40th floor with 270-degree city views. Private elevator, infinity pool, and personal concierge included.',
                'location': 'Worli, Mumbai',
                'price': 45000000,
                'type': 'Villa',
                'listing_type': 'new_launch',
                'bedrooms': 4, 'bathrooms': 5, 'area_sqft': 5500,
                'is_featured': True,
                'amenities': ['Private Elevator', 'Infinity Pool', 'Personal Concierge', 'Helipad Access', 'Wine Cellar'],
            },
        ]

        created_properties = []
        for data in properties_data:
            amenity_names = data.pop('amenities')
            prop, created = Property.objects.get_or_create(
                title=data['title'],
                defaults={**data, 'owner': agent}
            )
            if created:
                for amenity in amenity_names:
                    Amenity.objects.create(property=prop, name=amenity)
            created_properties.append(prop)

        self.stdout.write(self.style.SUCCESS(f'  ✔ {len(properties_data)} properties created'))

        # Buyer favorites 2 properties
        Favorite.objects.get_or_create(user=buyer, property=created_properties[0])
        Favorite.objects.get_or_create(user=buyer, property=created_properties[3])

        # ── Community Posts ────────────────────────────────────────────────────
        posts_data = [
            {
                'title': 'Looking for a spacious 3BHK in a prime location',
                'content': "I'm in the market for a 3BHK apartment in a central area with good connectivity. My budget is around ₹80 lakhs. Any recommendations or leads would be greatly appreciated! Open to both ready-to-move and under-construction options.",
                'author': buyer,
            },
            {
                'title': 'Investment opportunity: Commercial property in BKC',
                'content': "I've come across a commercial property in BKC. The projected ROI is 7-8% annually. Has anyone invested in commercial real estate lately? What's the current market sentiment?",
                'author': agent,
            },
            {
                'title': 'Tips for first-time home buyers in Mumbai',
                'content': "Buying your first home can be overwhelming. Here are my top 5 tips:\n1. Get pre-approved for a home loan first\n2. Consider total cost of ownership (not just EMI)\n3. Research the builder's track record\n4. Check RERA registration\n5. Factor in stamp duty and registration charges (~7% of property value)",
                'author': agent,
            },
            {
                'title': 'Is Thane a good investment now? Market Analysis 2025',
                'content': "Thane has seen consistent 12-15% appreciation over the last 3 years. With the new metro line and upcoming infrastructure projects, I believe it's still a good investment destination. What are your thoughts? Have any of you recently bought or sold in Thane?",
                'author': buyer,
            },
        ]

        created_posts = []
        for data in posts_data:
            post, _ = Post.objects.get_or_create(title=data['title'], defaults=data)
            created_posts.append(post)

        # Add likes and comments
        Like.objects.get_or_create(post=created_posts[0], user=agent)
        Like.objects.get_or_create(post=created_posts[1], user=buyer)
        Like.objects.get_or_create(post=created_posts[2], user=buyer)
        Like.objects.get_or_create(post=created_posts[3], user=agent)
        Save.objects.get_or_create(post=created_posts[2], user=buyer)

        Comment.objects.get_or_create(
            post=created_posts[0], author=agent,
            defaults={'content': "I have a few listings in Andheri and Powai that match your requirement. Let me know if you'd like a site visit!"}
        )
        Comment.objects.get_or_create(
            post=created_posts[2], author=buyer,
            defaults={'content': "This is really helpful, especially the RERA tip. I didn't know about that!"}
        )
        Comment.objects.get_or_create(
            post=created_posts[3], author=agent,
            defaults={'content': "Thane is definitely hot right now. The Ghodbunder Road corridor is seeing massive development."}
        )

        self.stdout.write(self.style.SUCCESS(f'  ✔ {len(posts_data)} community posts created with likes & comments'))

        # ── Notifications ──────────────────────────────────────────────────────
        Notification.objects.get_or_create(
            user=buyer, message='New property matching your search criteria: Modern 4BHK Family House in Bandra West'
        )
        Notification.objects.get_or_create(
            user=buyer, message='Agent Raj Mehta commented on your post'
        )
        Notification.objects.get_or_create(
            user=agent, message='New launch listing approved: Smart 2BHK Apartment in Thane West'
        )

        self.stdout.write(self.style.SUCCESS('  ✔ 3 notifications created'))

        self.stdout.write(self.style.MIGRATE_HEADING('\n✅ Seeding complete!\n'))
        self.stdout.write('  📧 Agent login:  agent@hector25.com  /  Agent@1234')
        self.stdout.write('  📧 Buyer login:  buyer@hector25.com  /  Buyer@1234')
        self.stdout.write('  🌐 API Root:     http://127.0.0.1:8000/')
        self.stdout.write('  🔧 Admin Panel:  http://127.0.0.1:8000/admin/\n')
