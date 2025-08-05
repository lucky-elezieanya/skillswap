from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from api.models import (
    Profile, Category, Skill, Service, Booking, Review,
    TrustBadge, Message, PaymentTransaction, EscrowTransaction, Location
)
from decimal import Decimal
import random
from faker import Faker

fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with mock data for SkillSwap'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding SkillSwap data...'))

        # 1. Clean database — delete in proper order
        EscrowTransaction.objects.all().delete()
        PaymentTransaction.objects.all().delete()
        Message.objects.all().delete()
        TrustBadge.objects.all().delete()
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Service.objects.all().delete()
        Skill.objects.all().delete()
        Category.objects.all().delete()
        Location.objects.all().delete()
        Profile.objects.all().delete()  # must come before user
        User.objects.exclude(is_superuser=True).delete()

        # 2. Create Users
        users = []
        for i in range(10):
            is_provider = i % 2 == 0
            user = User.objects.create_user(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password="password123",
                is_provider=is_provider,
                phone=fake.phone_number(),
                location=fake.city(),
                is_verified=random.choice([True, False]),
                community_verified=random.choice([True, False]),
                video_intro_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" if is_provider else ""
            )
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(users)} users."))

        # 3. Create Profiles
        for user in users:
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    "bio": fake.paragraph(),
                    "languages": "English, French",
                    "hourly_rate": Decimal(random.randint(20, 100)),
                    "rating": round(random.uniform(3.0, 5.0), 1)
                }
            )
        self.stdout.write(self.style.SUCCESS("✅ Created user profiles."))

        # 4. Categories and Skills
        categories = []
        cat_names = ['Design', 'Writing', 'Development', 'Marketing', 'Music', 'Fitness']
        for name in cat_names:
            cat = Category.objects.create(name=name)
            categories.append(cat)

        skills = []
        for cat in categories:
            for i in range(3):
                skill = Skill.objects.create(
                    name=f"{cat.name} Skill {i+1}",
                    category=cat
                )
                skills.append(skill)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(categories)} categories and {len(skills)} skills."))

        # 5. Assign skills to profiles
        for profile in Profile.objects.all():
            profile.skills.set(random.sample(skills, k=random.randint(1, 4)))

        # 6. Create Services
        services = []
        for provider in User.objects.filter(is_provider=True):
            for _ in range(2):
                service = Service.objects.create(
                    provider=provider,
                    title=fake.job(),
                    description=fake.paragraph(),
                    service_type=random.choice(['digital', 'local']),
                    payment_type=random.choice(['escrow', 'postpay', 'barter']),
                    price=Decimal(random.randint(30, 150)),
                    is_active=True
                )
                service.skills.set(random.sample(skills, k=random.randint(1, 3)))
                services.append(service)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(services)} services."))

        # 7. Create Bookings
        bookings = []
        clients = User.objects.filter(is_provider=False)
        for _ in range(10):
            client = random.choice(clients)
            service = random.choice(services)
            booking = Booking.objects.create(
                client=client,
                service=service,
                status=random.choice(['pending', 'accepted', 'in_progress', 'completed', 'cancelled']),
                scheduled_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                message=fake.sentence(),
                location=fake.city(),
                agreed_price=service.price,
                is_barter=random.choice([True, False]),
                barter_offer=fake.sentence()
            )
            bookings.append(booking)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(bookings)} bookings."))

        # 8. Create Reviews
        for _ in range(10):
            reviewer = random.choice(clients)
            provider = random.choice(User.objects.filter(is_provider=True))
            Review.objects.create(
                reviewer=reviewer,
                provider=provider,
                rating=random.randint(3, 5),
                comment=fake.sentence()
            )

        self.stdout.write(self.style.SUCCESS("✅ Created reviews."))

        # 9. Create Trust Badges
        for user in random.sample(users, 5):
            TrustBadge.objects.create(
                user=user,
                title="Community Star",
                issuer="SkillSwap Community",
                description="Awarded for exceptional service"
            )

        self.stdout.write(self.style.SUCCESS("✅ Created trust badges."))

        # 10. Create Messages
        for _ in range(10):
            sender, recipient = random.sample(users, 2)
            Message.objects.create(
                sender=sender,
                recipient=recipient,
                text=fake.sentence()
            )

        self.stdout.write(self.style.SUCCESS("✅ Created messages."))

        # 11. Create Payment Transactions
        for booking in random.sample(bookings, 5):
            PaymentTransaction.objects.create(
                booking=booking,
                amount=booking.agreed_price or Decimal("50.00"),
                status=random.choice(['initiated', 'held', 'released', 'refunded'])
            )

        self.stdout.write(self.style.SUCCESS("✅ Created payment transactions."))

        # 12. Create Escrow Transactions
        for _ in range(5):
            payer, receiver = random.sample(users, 2)
            EscrowTransaction.objects.create(
                payer=payer,
                receiver=receiver,
                amount=Decimal(random.randint(50, 200)),
                description="Escrow for freelance service",
                status=random.choice(['pending', 'released', 'refunded', 'disputed']),
                created_at=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS("✅ Created escrow transactions."))

        # 13. Create Locations
        for _ in range(5):
            Location.objects.create(
                city=fake.city(),
                state=fake.state(),
                country=fake.country(),
                postal_code=fake.postcode(),
                latitude=round(random.uniform(-90, 90), 6),
                longitude=round(random.uniform(-180, 180), 6)
            )

        self.stdout.write(self.style.SUCCESS("✅ Created locations."))
        self.stdout.write(self.style.SUCCESS("🎉 SkillSwap data seeded successfully!"))
