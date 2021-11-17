from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard_page),
    path('create', views.new_job_page),
    path('jobs/edit/<int:job_id>', views.edit_job_page),
    path('jobs/<int:job_id>', views.job_page),

    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('jobs/create', views.create_job),
    path('jobs/add/<int:job_id>', views.add_job),
    path('jobs/give_up/<int:job_id>', views.give_up_job),
    path('jobs/delete/<int:job_id>', views.delete_job),
    path('jobs/update/<int:job_id>', views.update_job),
]