from django.contrib import admin
from courses.models import Category, Instructor, Course, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ('name', 'slug', 'course_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = "Total Courses"


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    """Admin configuration for Instructor model."""
    list_display = ('name', 'email', 'title')
    search_fields = ('name', 'email', 'title')


class ReviewInline(admin.TabularInline):
    """Tabular inline displaying reviews directly within Course edit view."""
    model = Review
    extra = 1
    fields = ('student_name', 'rating', 'comment', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Demonstrating advanced Django Admin customization:
    - list_display: customizable columns
    - list_filter: right-hand filter sidebar
    - search_fields: free-text search
    - prepopulated_fields: auto-fills slug from title in real-time
    - date_hierarchy: date drill-down navigation
    - inlines: nested tabular inline records
    - actions: bulk actions (e.g. Publish / Draft)
    """
    list_display = ('title', 'category', 'instructor', 'difficulty', 'price', 'status', 'views_count', 'created_at')
    list_filter = ('status', 'difficulty', 'category', 'created_at')
    search_fields = ('title', 'summary', 'content', 'instructor__name')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [ReviewInline]
    actions = ['make_published', 'make_draft']

    @admin.action(description="Mark selected courses as Published")
    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='published')
        self.message_user(request, f"{rows_updated} course(s) successfully marked as Published.")

    @admin.action(description="Mark selected courses as Draft")
    def make_draft(self, request, queryset):
        rows_updated = queryset.update(status='draft')
        self.message_user(request, f"{rows_updated} course(s) moved to Draft.")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for Review model."""
    list_display = ('course', 'student_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('student_name', 'comment', 'course__title')
