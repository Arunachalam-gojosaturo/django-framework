import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import Category, Instructor, Course, Review

def seed():
    print("🌱 Seeding database for Seminar Unit V...")

    # 1. Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@edupulse.edu', 'admin123')
        print("✅ Superuser created: admin / admin123")
    else:
        print("ℹ️ Superuser already exists.")

    # 2. Categories
    cat_python, _ = Category.objects.get_or_create(
        slug='python-fundamentals',
        defaults={'name': 'Python Fundamentals', 'description': 'Core syntax, data types, loops, OOP and built-in structures.', 'icon': '🐍'}
    )
    cat_web, _ = Category.objects.get_or_create(
        slug='django-web-framework',
        defaults={'name': 'Django Web Framework', 'description': 'MVT architecture, ORM, models, templates, views, and forms.', 'icon': '🌐'}
    )
    cat_data, _ = Category.objects.get_or_create(
        slug='data-science-ai',
        defaults={'name': 'Data Science & Analytics', 'description': 'NumPy arrays, Pandas DataFrames, and Matplotlib data visualization.', 'icon': '📊'}
    )
    cat_db, _ = Category.objects.get_or_create(
        slug='databases-sql',
        defaults={'name': 'Databases & Query Optimization', 'description': 'Relational schema design, SQL queries, and Django ORM indices.', 'icon': '💾'}
    )

    # 3. Instructors
    inst_lambert, _ = Instructor.objects.get_or_create(
        email='lambert@edupulse.edu',
        defaults={'name': 'Prof. K.A. Lambert', 'title': 'Computer Science Department Chair', 'bio': 'Author of "Fundamentals of Python: First Programs" with 25+ years teaching Python.'}
    )
    inst_sarah, _ = Instructor.objects.get_or_create(
        email='sarah@edupulse.edu',
        defaults={'name': 'Dr. Sarah Connor', 'title': 'Senior Full-Stack Engineer', 'bio': 'Specialist in Django web development, PostgreSQL optimization, and RESTful architectures.'}
    )
    inst_alex, _ = Instructor.objects.get_or_create(
        email='alex@edupulse.edu',
        defaults={'name': 'Alex Rivera', 'title': 'Data Scientist & AI Researcher', 'bio': 'Expert in NumPy, Pandas, Matplotlib visualizations, and machine learning pipelines.'}
    )

    # 4. Courses
    courses_data = [
        {
            'title': 'Mastering Python Fundamentals: First Programs',
            'slug': 'mastering-python-fundamentals',
            'category': cat_python,
            'instructor': inst_lambert,
            'summary': 'Comprehensive introduction to strings, loops, functions, lists, and recursive problem solving.',
            'content': """Curriculum Outline:
1. Fundamental ideas of Computer Science & Strings
2. Control Structures: Definite iteration (for) & while loops
3. Data structures: Lists, dictionaries, and string manipulation
4. Functional programming and recursive problem solving
5. Designing reusable classes with inheritance and polymorphism""",
            'price': 0.00,
            'difficulty': 'beginner',
            'status': 'published',
            'views_count': 340,
        },
        {
            'title': 'Building Web Applications with Django 5.x',
            'slug': 'building-web-applications-with-django',
            'category': cat_web,
            'instructor': inst_sarah,
            'summary': 'Learn the MVT architecture, ORM models, views, templates, and the Django administration site.',
            'content': """Curriculum Outline:
1. Installing Django & setting up project structure
2. Data schema modeling with SQLite and PostgreSQL
3. Mastering QuerySets, Managers, and lazy evaluation
4. Creating customized ModelAdmin with search & filters
5. Building Class-Based List and Detail Views""",
            'price': 49.00,
            'difficulty': 'intermediate',
            'status': 'published',
            'views_count': 520,
        },
        {
            'title': 'Data Analysis with NumPy, Pandas & Matplotlib',
            'slug': 'data-analysis-numpy-pandas-matplotlib',
            'category': cat_data,
            'instructor': inst_alex,
            'summary': 'Manipulate multi-dimensional ndarrays, build Pandas series and dataframes, and render interactive charts.',
            'content': """Curriculum Outline:
1. NumPy ndarray slicing, broadcasting, and manipulation
2. Pandas Series, DataFrames, and index objects
3. Data cleansing, missing value handling, and grouping
4. Matplotlib architecture: figures, axes, subplots
5. Line, Bar, and Pie chart visualization best practices""",
            'price': 39.00,
            'difficulty': 'intermediate',
            'status': 'published',
            'views_count': 280,
        },
        {
            'title': 'Advanced Django ORM & QuerySet Deep Dive',
            'slug': 'advanced-django-orm-queryset-deep-dive',
            'category': cat_web,
            'instructor': inst_sarah,
            'summary': 'Unlocking the power of select_related, prefetch_related, custom model managers, and raw SQL inspection.',
            'content': """Curriculum Outline:
1. Anatomy of a QuerySet: Query compiler & connection backend
2. Custom Model Managers & QuerySet subclassing
3. Eliminating N+1 query bottlenecks via prefetch_related
4. Aggregate, Annotate, Subquery, and OuterRef expressions
5. Database migrations internals and schema migrations""",
            'price': 79.00,
            'difficulty': 'advanced',
            'status': 'published',
            'views_count': 610,
        },
        {
            'title': 'Object-Oriented Design & Data Structures in Python',
            'slug': 'oop-data-structures-python',
            'category': cat_python,
            'instructor': inst_lambert,
            'summary': 'Classes, objects, inheritance, polymorphism, grids, and GUI-based event handling with Tkinter.',
            'content': """Curriculum Outline:
1. Design with Classes: Encapsulation and abstraction
2. Structuring hierarchies with inheritance and polymorphism
3. Designing grid data structures and memory layouts
4. Event-driven GUI programming with widgets and command buttons""",
            'price': 25.00,
            'difficulty': 'beginner',
            'status': 'published',
            'views_count': 195,
        },
        {
            'title': 'Draft / Internal: Upcoming Microservices with Django',
            'slug': 'upcoming-microservices-with-django',
            'category': cat_web,
            'instructor': inst_sarah,
            'summary': 'Draft curriculum being developed by the department.',
            'content': 'Coming soon: API Gateways and microservices architecture.',
            'price': 99.00,
            'difficulty': 'advanced',
            'status': 'draft',
            'views_count': 12,
        }
    ]

    for c_data in courses_data:
        c, created = Course.objects.get_or_create(
            slug=c_data['slug'],
            defaults=c_data
        )
        if created:
            print(f"  + Course created: {c.title}")

    # 5. Reviews
    c_django = Course.objects.get(slug='building-web-applications-with-django')
    Review.objects.get_or_create(
        course=c_django,
        student_name='Arunachalam',
        defaults={'rating': 5, 'comment': 'Fantastic coverage of the MVT architecture and Custom Managers. Perfect for our Unit V seminar!'}
    )
    Review.objects.get_or_create(
        course=c_django,
        student_name='Priya Sharma',
        defaults={'rating': 5, 'comment': 'The QuerySet Explorer helped me visually understand how lazy evaluation works.'}
    )

    c_python = Course.objects.get(slug='mastering-python-fundamentals')
    Review.objects.get_or_create(
        course=c_python,
        student_name='Vignesh K.',
        defaults={'rating': 5, 'comment': 'Clear and concise explanations. Follows Lambert textbook perfectly.'}
    )

    print("🎉 Database seeding complete! You are ready for the seminar presentation!")

if __name__ == '__main__':
    seed()
