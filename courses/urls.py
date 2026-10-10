from django.urls import path
from courses.views import (
    CourseListView,
    CourseDetailView,
    course_list_fbv,
    course_detail_fbv,
    queryset_explorer_view,
    add_review_view,
    SeminarGuideView,
)

app_name = 'courses'

urlpatterns = [
    # 1. Primary Class-Based List and Detail Views
    path('', CourseListView.as_view(), name='course_list'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/<slug:slug>/review/', add_review_view, name='add_review'),

    # 2. Interactive QuerySet & Manager Explorer (for Seminar presentation)
    path('querysets/', queryset_explorer_view, name='queryset_explorer'),

    # 3. Dedicated Seminar Presentation Deck
    path('seminar/', SeminarGuideView.as_view(), name='seminar_guide'),

    # 4. Function-Based Views (for FBV vs CBV comparison)
    path('fbv/list/', course_list_fbv, name='course_list_fbv'),
    path('fbv/course/<slug:slug>/', course_detail_fbv, name='course_detail_fbv'),
]
