from django.db import models

class PublishedCourseQuerySet(models.QuerySet):
    """Custom QuerySet enabling reusable method chaining."""
    def published(self):
        return self.filter(status='published').order_by('-created_at')

    def by_difficulty(self, difficulty):
        return self.filter(difficulty=difficulty).order_by('-created_at')

    def popular(self, min_views=100):
        return self.filter(views_count__gte=min_views).order_by('-views_count')

class PublishedCourseManager(models.Manager):
    """
    Custom Model Manager demonstrating:
    'Working with QuerySets and Managers' from Unit V.
    Provides Course.published.all() which pre-filters active records.
    """
    def get_queryset(self):
        return PublishedCourseQuerySet(self.model, using=self._db).filter(status='published').order_by('-created_at')

    def beginner_courses(self):
        return self.get_queryset().filter(difficulty='beginner')

    def popular(self):
        return self.get_queryset().filter(views_count__gte=100).order_by('-views_count')
