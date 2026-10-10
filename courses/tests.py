from django.test import TestCase, Client
from django.urls import reverse
from courses.models import Course, Category, Instructor, Review

class UnitVSyllabusTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Python Fundamentals",
            slug="python-fundamentals",
            description="Testing category"
        )
        self.instructor = Instructor.objects.create(
            name="Prof. Lambert",
            email="lambert@test.edu",
            title="Professor",
            bio="Test bio"
        )
        self.course_pub = Course.objects.create(
            title="Intro to Python",
            slug="intro-to-python",
            category=self.category,
            instructor=self.instructor,
            summary="Test summary",
            content="Test content",
            price=10.00,
            status="published",
            views_count=50
        )
        self.course_draft = Course.objects.create(
            title="Draft Python",
            slug="draft-python",
            category=self.category,
            instructor=self.instructor,
            summary="Draft summary",
            content="Draft content",
            status="draft"
        )

    def test_custom_manager_published(self):
        """Tests 'Working with QuerySets and Managers' requirement."""
        published = Course.published.all()
        self.assertIn(self.course_pub, published)
        self.assertNotIn(self.course_draft, published)
        self.assertEqual(published.count(), 1)

    def test_course_list_view(self):
        """Tests 'Building List and Detail Views' (ListView)."""
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Intro to Python")
        # Draft should NOT appear in published list
        self.assertNotContains(response, "Draft Python")

    def test_course_detail_view(self):
        """Tests 'Building List and Detail Views' (DetailView)."""
        response = self.client.get(reverse('courses:course_detail', kwargs={'slug': 'intro-to-python'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Intro to Python")
        self.assertContains(response, "Curriculum & Course Outline")

    def test_queryset_explorer_view(self):
        """Tests interactive QuerySet live explorer."""
        response = self.client.get(reverse('courses:queryset_explorer') + '?preset=all_courses')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course.objects.all()")
        self.assertContains(response, "Generated Database SQL Statement")

    def test_seminar_guide_view(self):
        """Tests seminar presentation view."""
        response = self.client.get(reverse('courses:seminar_guide'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unit V: Python Django Web Framework")

    def test_add_review_form(self):
        """Tests user feedback form submission."""
        response = self.client.post(
            reverse('courses:add_review', kwargs={'slug': 'intro-to-python'}),
            {
                'student_name': 'Test Student',
                'rating': 5,
                'comment': 'Excellent lecture!'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.filter(course=self.course_pub).count(), 1)
