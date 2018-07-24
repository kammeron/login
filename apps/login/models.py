from __future__ import unicode_literals
from django.db import models
import re, bcrypt

# Create your models here.
class UserManager(models.Manager):
	def registration_validator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['first_name']) < 2:
			errors['first_name'] = 'First name should be at least 2 characters'
		if len(postData['last_name']) < 2:
			errors['last_name'] = 'Last name should be at least 2 characters'
		if len(postData['email']) < 1:
			errors['email'] = 'Please fill out email'
		elif not EMAIL_REGEX.match(postData['email']):
			errors['email_valid'] = 'Email is not valid!'
		if len(User.objects.filter(email = postData['email'])) > 0:
			errors['existing_email'] = 'Email is already in use.'
		if len(postData['password']) < 8:
			errors['password_length'] = 'Password must be at least 8 characters'
		if postData['password'] != postData['password_confirm']:
			errors['password_confirm'] = 'Passwords do not match'
		return errors

	def login_validator(self, postData):
		errors = {}
		user = User.objects.filter(email = postData['email'])
		if len(user) < 1:
			errors['unknown'] = 'Invalid credentials'
		else:
			if bcrypt.checkpw(postData['password'].encode(), user.values()[0]['password'].encode()) == False:
				errors['badpw'] = 'Wrong password'
		return errors

	def update_validator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['first_name']) < 2:
			errors['first_name'] = 'First name should be at least 2 characters'
		if len(postData['last_name']) < 2:
			errors['last_name'] = 'Last name should be at least 2 characters'
		if len(postData['email']) < 1:
			errors['email'] = 'Please fill out email'
		elif not EMAIL_REGEX.match(postData['email']):
			errors['email_valid'] = 'Email is not valid!'
		if len(User.objects.filter(email = postData['email'])) > 0:
			errors['existing_email'] = 'Email is already in use.'
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	objects = UserManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class QuoteManager(models.Manager):
	def validator(self, postData):
		errors = {}
		if len(postData['author']) < 3:
			errors['author'] = 'Author should be at least 3 characters'
		if len(postData['quote']) < 10:
			errors['quote'] = 'Quote should be at least 10 characters'
		if len(Quote.objects.filter(content = postData['quote'])) > 0:
			errors['existing_email'] = 'Quote is already posted.'
		return errors

class Quote(models.Model):
	author = models.CharField(max_length=255)
	content = models.CharField(max_length=1000)
	user = models.ForeignKey(User, related_name="user")
	like = models.ManyToManyField(User, related_name="like")
	objects = QuoteManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)