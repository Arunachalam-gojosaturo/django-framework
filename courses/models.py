from django.db import models
from django.urls import reverse
from courses.managers import PublishedCourseManager

class Category(models.Model):
    """
    Demonstrates model schema design, unique SlugField, and Meta options.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="book", help_text="Emoji or icon identifier")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses:category_list', kwargs={'slug': self.slug})


class Instructor(models.Model):
    """Instructor profile entity."""
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=150, help_text="e.g. Senior Python Specialist")
    bio = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Main entity demonstrating:
    - Field types (CharField, SlugField, ForeignKey, TextField, DecimalField, IntegerField)
    - Relationships (ForeignKey with on_delete=models.CASCADE and related_name)
    - Model choices (status, difficulty)
    - Default manager vs. Custom Manager (objects vs published)
    - Canonical URL generation via get_absolute_url()
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')
    summary = models.CharField(max_length=300, help_text="Short card synopsis")
    content = models.TextField(help_text="Detailed syllabus and curriculum description")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager()               # The default manager: Course.objects.all()
    published = PublishedCourseManager()     # Custom Manager: Course.published.all()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', 'status']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})


class Review(models.Model):
    """
    Demonstrates One-to-Many relationship (Course has many Reviews)
    and aggregating data with QuerySets.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)], default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}★ by {self.student_name} on {self.course.title}"
