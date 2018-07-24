from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
	return render(request, 'login/index.html')

def register(request):
	# add function to search database if 
	errors = User.objects.registration_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
		user = User.objects.filter(email = request.POST['email'])
		request.session['user_id'] = user.values()[0]['id']
		request.session['user_first_name'] = user.values()[0]['first_name']
		request.session['user_last_name'] = user.values()[0]['last_name']
		request.session['user_email'] = user.values()[0]['email']
		return redirect('/quotes')

def login(request):
	if request.method == 'POST':
		errors = User.objects.login_validator(request.POST)
		if len(errors):
			for key, value in errors.items():
				messages.error(request, value)
			print(errors)
			return redirect('/')
		else:
			user = User.objects.filter(email = request.POST['email'])
			request.session['user_id'] = user.values()[0]['id']
			request.session['user_first_name'] = user.values()[0]['first_name']
			request.session['user_last_name'] = user.values()[0]['last_name']
			request.session['user_email'] = user.values()[0]['email']
			print(request.session.values())
			return redirect('/quotes')

def logout(request):
	request.session.flush()
	return redirect('/')

def quotes(request):
	if 'user_id' in request.session:
		context = {
		'quotes' : Quote.objects.all(),
		'users' : User.objects.all().values(),
		}
		return render(request, 'login/quotes.html', context)
	else:
		return redirect('/')

def add_quote(request):
	if 'user_id' in request.session:
		errors = Quote.objects.validator(request.POST)
		if len(errors):
			for key, value in errors.items():
				messages.error(request, value)
			print(errors)
			return redirect('/quotes')
		else:
			Quote.objects.create(author=request.POST['author'], content=request.POST['quote'], user=User.objects.get(id=request.session['user_id']))
			return redirect('/quotes')
	else:
		return redirect('/')

def delete_quote(request, quote_id):
	q = Quote.objects.get(id=quote_id)
	q.delete()
	return redirect('/quotes')

def edit_user(request, user_id):
	if 'user_id' in request.session:
		context = {
		'user' : User.objects.get(id=user_id),
		}
		return render(request, 'login/edit_user.html', context)
	else:
		return redirect('/')

def user_page(request, user_id):
	if 'user_id' in request.session:
		context = {
		'users' : User.objects.get(id=user_id),
		}
		return render(request, 'login/user_page.html', context)
	else:
		return redirect('/')

def edit_process(request):
	if 'user_id' in request.session:
		errors = User.objects.update_validator(request.POST)
		if len(errors):
			for key, value in errors.items():
				messages.error(request, value)
			print(errors)
			return redirect('/quotes')
		else:
			b = User.objects.get(id=request.session['user_id'])
			print(b)
			b.first_name = request.POST['first_name']
			b.last_name = request.POST['last_name']
			b.email = request.POST['email']
			b.save()
			user = User.objects.get(id=request.session['user_id']).__dict__
			request.session['user_id'] = user['id']
			request.session['user_first_name'] = user['first_name']
			request.session['user_last_name'] = user['last_name']
			request.session['user_email'] = user['email']
			return redirect('/quotes')
	else:
		return redirect('/')

def like_process(request, quote_id):
	if 'user_id' in request.session:
		this_user = User.objects.get(id=request.session['user_id'])
		this_quote = Quote.objects.get(id=quote_id)
		this_quote.like.add(this_user)
		return redirect('/quotes')
	else:
		return redirect('/')