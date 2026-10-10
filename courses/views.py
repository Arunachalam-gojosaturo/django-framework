from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Avg, Count, Q
from django.contrib import messages
from courses.models import Course, Category, Instructor, Review
from courses.forms import ReviewForm

# ==============================================================================
# 1. CLASS-BASED VIEWS (CBVs) - Primary Syllabus Requirement
# ==============================================================================

class CourseListView(ListView):
    """
    Demonstrating:
    - ListView: Built-in generic display view
    - get_queryset(): QuerySet filtering, searching, and chaining
    - get_context_data(): Enriching template context with extra variables
    - Pagination: Built-in paginate_by attribute
    """
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 6

    def get_queryset(self):
        # Using Custom Manager: Course.published.all() instead of Course.objects.all()
        qs = Course.published.select_related('category', 'instructor').annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )

        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            qs = qs.filter(difficulty=difficulty)

        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(instructor__name__icontains=query)
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().annotate(total_courses=Count('courses'))
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['total_published'] = Course.published.count()
        return context


class CourseDetailView(DetailView):
    """
    Demonstrating:
    - DetailView: Generic view to retrieve and display a single object
    - Retrieving objects by slug URL parameter
    - Tracking views count
    - Accessing reverse foreign key relations (course.reviews.all())
    """
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        # Increments views counter upon single object retrieval
        obj = super().get_object(queryset=queryset)
        Course.objects.filter(pk=obj.pk).update(views_count=obj.views_count + 1)
        obj.views_count += 1
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['form'] = ReviewForm()
        context['avg_rating'] = self.object.reviews.aggregate(Avg('rating'))['rating__avg'] or 5.0
        context['related_courses'] = (
            Course.published
            .filter(category=self.object.category)
            .exclude(id=self.object.id)[:3]
        )
        return context


# ==============================================================================
# 2. FUNCTION-BASED VIEWS (FBVs) - For Seminar Comparison
# ==============================================================================

def course_list_fbv(request):
    """
    Equivalent Function-Based View (FBV) to demonstrate the contrast
    between explicit procedural rendering and Class-Based Views.
    """
    courses = Course.published.all().select_related('category', 'instructor')
    categories = Category.objects.all()
    return render(request, 'courses/course_list_fbv.html', {
        'courses': courses,
        'categories': categories,
        'view_type': 'Function-Based View (FBV)'
    })


def course_detail_fbv(request, slug):
    """
    Demonstrates get_object_or_404() helper function for object retrieval.
    """
    course = get_object_or_404(Course, slug=slug, status='published')
    return render(request, 'courses/course_detail_fbv.html', {
        'course': course,
        'view_type': 'Function-Based View (FBV)'
    })


# ==============================================================================
# 3. INTERACTIVE QUERYSET & MANAGER EXPLORER (Live Seminar Demo!)
# ==============================================================================

def queryset_explorer_view(request):
    """
    Interactive playground allowing the speaker in a seminar to execute
    diverse QuerySets live and visually display:
    1. The Python ORM code snippet
    2. The generated raw SQL statement
    3. The resulting objects & count
    4. An explanation of the underlying Django concept
    """
    preset = request.GET.get('preset', 'all_courses')

    querysets_map = {
        'all_courses': {
            'title': '1. Retrieving All Objects (Default Manager)',
            'code': 'Course.objects.all()',
            'explanation': 'Retrieves all courses regardless of status. Uses the default "objects" manager.',
            'qs_factory': lambda: Course.objects.all()
        },
        'custom_manager': {
            'title': '2. Custom Model Manager (Course.published.all())',
            'code': 'Course.published.all()',
            'explanation': 'Demonstrates Custom Manager "published" defined in managers.py. Automatically pre-filters where status="published".',
            'qs_factory': lambda: Course.published.all()
        },
        'filter_lookup': {
            'title': '3. Filtering with Field Lookups',
            'code': 'Course.objects.filter(difficulty="beginner")',
            'explanation': 'Uses .filter() with keyword argument lookup to match beginner level courses.',
            'qs_factory': lambda: Course.objects.filter(difficulty='beginner')
        },
        'exclude_condition': {
            'title': '4. Excluding Objects',
            'code': 'Course.objects.exclude(status="draft")',
            'explanation': 'Uses .exclude() to omit all draft records from the result set.',
            'qs_factory': lambda: Course.objects.exclude(status='draft')
        },
        'order_and_slice': {
            'title': '5. Ordering and Python Slicing (LIMIT/OFFSET)',
            'code': 'Course.objects.order_by("-views_count")[:3]',
            'explanation': 'Orders results by views descending and applies [:3] slice, which Django converts to SQL LIMIT 3.',
            'qs_factory': lambda: Course.objects.order_by('-views_count')[:3]
        },
        'relational_lookup': {
            'title': '6. Relationship Spanning (__ double underscore)',
            'code': 'Course.objects.filter(category__name="Python & Backend")',
            'explanation': 'Uses category__name to perform an INNER JOIN across ForeignKey relationships without writing manual SQL.',
            'qs_factory': lambda: Course.objects.filter(category__name__icontains='Python')
        },
        'aggregation': {
            'title': '7. QuerySet Aggregation',
            'code': 'Course.objects.aggregate(total=Count("id"), avg_views=Avg("views_count"))',
            'explanation': 'Performs mathematical summarization across rows returning a dictionary.',
            'qs_factory': None  # Special aggregate case
        },
        'single_object': {
            'title': '8. Retrieving a Single Object (.get())',
            'code': 'Course.objects.get(id=1)',
            'explanation': 'Retrieves an exact single instance. Raises DoesNotExist if not found, or MultipleObjectsReturned if more than one match.',
            'qs_factory': None
        }
    }

    selected_meta = querysets_map.get(preset, querysets_map['all_courses'])
    result_items = []
    generated_sql = ""
    result_count = 0
    extra_data = None

    if preset == 'aggregation':
        extra_data = Course.objects.aggregate(
            total=Count('id'),
            avg_views=Avg('views_count')
        )
        generated_sql = "SELECT COUNT(id), AVG(views_count) FROM courses_course;"
        result_count = 1
    elif preset == 'single_object':
        try:
            item = Course.objects.first()
            if item:
                result_items = [item]
                result_count = 1
                generated_sql = f"SELECT * FROM courses_course WHERE id = {item.id} LIMIT 1;"
        except Exception as e:
            extra_data = str(e)
    else:
        qs = selected_meta['qs_factory']()
        result_count = qs.count() if hasattr(qs, 'count') else len(qs)
        result_items = list(qs)
        # Capture generated SQL
        try:
            generated_sql = str(qs.query)
        except Exception:
            generated_sql = "N/A (Evaluated QuerySet)"

    return render(request, 'courses/queryset_explorer.html', {
        'presets': querysets_map,
        'current_preset': preset,
        'meta': selected_meta,
        'results': result_items,
        'result_count': result_count,
        'generated_sql': generated_sql,
        'extra_data': extra_data,
    })


# ==============================================================================
# 4. ACTION VIEWS & SEMINAR GUIDE
# ==============================================================================

def add_review_view(request, slug):
    """Handles submission of a review via POST."""
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.save()
            messages.success(request, f"Thank you, {review.student_name}! Your review has been published.")
        else:
            messages.error(request, "Please correct the errors below.")
    return redirect('courses:course_detail', slug=slug)


class SeminarGuideView(TemplateView):
    """Interactive slide and presentation dashboard directly embedded in the web app."""
    template_name = 'courses/seminar_guide.html'
