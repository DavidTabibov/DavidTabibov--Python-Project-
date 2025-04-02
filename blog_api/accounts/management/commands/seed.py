from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from articles.models import Article
from comments.models import Comment

class Command(BaseCommand):
    help = 'Seed the database with initial data including groups.'

    def handle(self, *args, **options):
        # Create groups if not exist
        groups = {
            "Viewer": "Can view articles and comments.",
            "Connected": "Can add comments.",
            "Editor": "Can add articles.",
            "Admin": "Can do everything."
        }
        for group_name, description in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists.'))

        # Create admin user if not exist and assign Admin group
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpass'
            )
            admin_group = Group.objects.get(name="Admin")
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS('Admin user created and added to Admin group.'))
        else:
            admin_user = User.objects.get(username='admin')
            self.stdout.write(self.style.WARNING('Admin user already exists.'))

        # Create regular user if not exist and assign Connected group
        if not User.objects.filter(username='user').exists():
            regular_user = User.objects.create_user(
                username='user',
                email='user@example.com',
                password='userpass'
            )
            connected_group = Group.objects.get(name="Connected")
            regular_user.groups.add(connected_group)
            self.stdout.write(self.style.SUCCESS('Regular user created and added to Connected group.'))
        else:
            regular_user = User.objects.get(username='user')
            self.stdout.write(self.style.WARNING('Regular user already exists.'))

        # Create articles
        article1, created = Article.objects.get_or_create(
            title='First Article',
            defaults={
                'content': 'Content of the first article.',
                'author': admin_user,
                'tags': 'django,rest'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Article 1 created.'))
        else:
            self.stdout.write(self.style.WARNING('Article 1 already exists.'))

        article2, created = Article.objects.get_or_create(
            title='Second Article',
            defaults={
                'content': 'Content of the second article.',
                'author': admin_user,
                'tags': 'python,api'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Article 2 created.'))
        else:
            self.stdout.write(self.style.WARNING('Article 2 already exists.'))

        # Create comments for each article (2 per article)
        for article in [article1, article2]:
            if article.comments.count() < 2:
                Comment.objects.create(article=article, user=regular_user, content="Great article!")
                Comment.objects.create(article=article, user=regular_user, content="Thanks for sharing.")
                self.stdout.write(self.style.SUCCESS(f'2 comments added to {article.title}.'))
            else:
                self.stdout.write(self.style.WARNING(f'{article.title} already has 2 or more comments.'))

        self.stdout.write(self.style.SUCCESS('Seeding completed.'))
