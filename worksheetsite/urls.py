"""worksheetsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

from fill_the_blanks import views


urlpatterns = [
    path('the_admin_page/', admin.site.urls),

    path('', views.WriteWorksheet.as_view(), name='home'),

    path('', include('worksheetsite.auth_urls')),

    path('<pk>/', views.FinishedWorksheet.as_view(), name='finished_worksheet'),

    path('<pk>/<slug>/', views.ReadWorksheet.as_view(), name='read_worksheet'),
    path('<pk>/<slug>/edit/', views.EditWorksheet.as_view(), name='edit_worksheet'),

    path('<pk>/<slug>/student/', views.StudentWorksheetView.as_view(), name='student_worksheet'),

    path('<pk>/<slug>/profile/', views.ProfileView.as_view(), name='profile'),

]
