from django.db import models

# Create your models here.
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'

        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'

        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


    objects = UserManager()

class JobsManager(models.Manager):
    def validate(self, postData):
        errors = {}

        if len(postData['title']) < 3:
            errors['title'] = "Title must be provided and should be at least 3 characters."
        if len(postData['description']) < 3:
            errors['description'] = "Description must be provided and should be at least 3 characters."
        if len(postData['location']) < 3:
            errors['location'] = "Location must be provided and should be at least 3 characters."

        return errors


class Jobs(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="created_by", on_delete=models.CASCADE)
    current_employee = models.ForeignKey(User, related_name="selected_jobs", on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)

    objects = JobsManager()