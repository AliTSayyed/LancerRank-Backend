"""
URL configuration for trust_pilot_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from trust_pilot_backend import views

urlpatterns = [
    path('api/reviews/', views.review_list),
    path('api/reviews/<int:id>', views.review_details),
    path('api/freelancers/', views.freelancer_list),
    path('api/freelancers/<int:id>', views.freelancer_details),
    path('api/users/', views.user_list),
    path('api/users/<int:id>', views.user_details),
    path('api/reviews/freelancers/<int:id>', views.freelancer_reviews),
    path('api/reviews/users/<int:id>', views.user_reviews),
    path('api/sort_and_filter_reviews/', views.sort_and_filter_reviews),
    path('admin/', admin.site.urls),
]
