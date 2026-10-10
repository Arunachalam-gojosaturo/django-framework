from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Administration site for models
    path('admin/', admin.site.urls),

    # Main Application routes (List & Detail views, QuerySets, Seminar)
    path('', include('courses.urls', namespace='courses')),
]
