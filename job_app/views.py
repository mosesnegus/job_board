from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import *
import bcrypt

# Functions / Handlers
def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )

        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name

        messages.success(request, "You have successfully registered!")
        return redirect('/')

def login(request):

    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')

    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")

    return redirect('/dashboard')


def logout(request):
    request.session.clear()
    return redirect('/')


def update_job(request, job_id):
    errors = {}
    errors = Jobs.objects.validate(request.POST)

    if errors:
        for error_message in errors.values():
            messages.error(request, error_message)
        
        return redirect(f"/jobs/edit/{job_id}")
        
    else:
        job = Jobs.objects.get(id=job_id)

        job.title = request.POST['title']
        job.description = request.POST['description']
        job.location = request.POST['location']

        job.save()

        return redirect(f"/dashboard")

    

def delete_job(request, job_id):
    job = Jobs.objects.get(id=job_id)
    job.delete()

    return redirect('/dashboard')

def add_job(request, job_id):
    user = User.objects.get(id=request.session["user_id"])
    job = Jobs.objects.get(id=job_id)

    user.selected_jobs.add(job)

    return redirect(f'/dashboard')

def give_up_job(request, job_id):
    user = User.objects.get(id=request.session["user_id"])
    job = Jobs.objects.get(id=job_id)

    user.selected_jobs.remove(job)

    return redirect(f'/dashboard')

def create_job(request):
    errors = {}
    errors = Jobs.objects.validate(request.POST)

    if errors:
        for error_message in errors.values():
            messages.error(request, error_message)
    
        return redirect('/create')
        
    else:
        user = User.objects.get(id=request.session['user_id'])

        job = Jobs.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            location = request.POST['location'],
            creator = user,
        )

        user.created_by.add(job)

        return redirect(f'/dashboard')

# Pages / Renders

def index(request):
    return render(request, 'index.html')


def job_page(request, job_id):
    context = {
        'job': Jobs.objects.get(id=job_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "jobs.html", context)

def dashboard_page(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    jobs = Jobs.objects.filter(~Q(current_employee=user))

    context = {
        'user': user,
        'jobs': jobs,
    }

    return render(request, 'dashboard.html', context)

def edit_job_page(request, job_id):
    user = User.objects.get(id=request.session['user_id'])
    job = Jobs.objects.get(id=job_id)

    if 'user_id' not in request.session and job.creator != user:
        return redirect('/dashboard')

    context = {
        'user': user,
        'job': job
    }

    return render(request, 'edit.html', context)

def new_job_page(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')

    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }

    return render(request, 'new.html', context)
