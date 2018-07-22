from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

# for user management
from django.contrib.auth.models import User
# for post management
from .models import Post
# for Categories
from .models import Category

from .forms import CreatePostForm
from .forms import CreateCommentForm

# for restricting access to adding post feature
from django.contrib.auth.decorators import login_required

# for user creation
from .forms import CreateUserForm

from django.contrib.auth import authenticate, login, logout

# for signup exception handling
from django.core.exceptions import ValidationError

# complex lookups (for searching)
from django.db.models import Q

# register new user
def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # prepare data in cleaned form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            # if User.objects.filter(username=username).count() > 1:
            #     raise ValidationError('Username already in use!')
            # if User.objects.filter(email=email).count() > 1:
            #     raise ValidationError('Email already exists!')
            # if password != password_confirm:
            #     raise ValidationError('Passwords do not match!')

            # login user after signup
            login(request, user)
            # and redirect to the main page
            return redirect('signup_successful.html')  # doesn't work... yet
    else:
        form = CreateUserForm()

    return render(request, 'blog/signup.html', {'form': form})


# adding posts feature
@login_required
def add(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreatePostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            category = form.cleaned_data['category']
            author = User.objects.get_by_natural_key(request.user.username)
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            published_date = timezone.now()

            # this needs to be fixed to account for new ManyToMany relation with category
            Post.objects.create(category=category, author=author,
                                title=title, content=content,
                                published_date=published_date)

            # redirect to main page
            # todo: redirect to just added post
            return redirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreatePostForm()

    return render(request, 'blog/add.html', {'form': form})


# adding comments feature
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            # get currently logged user
            author = User.objects.get_by_natural_key(request.user.username)
            content = form.cleaned_data['content']
            post.comments.objects.create(author=author, content=content)
            return redirect('/')
    else:
        form = CreateCommentForm()

    return render(request, 'blog/posts.html', {'form': form})


def index(request, category=''):
    list_of_posts = Post.objects.order_by('-published_date')

    if category != '':
        list_of_posts = list_of_posts.filter(category__name__contains=category)

    search = request.GET.get('search')
    if search:
        list_of_posts = list_of_posts.filter(
            Q(category__name__icontains=search) | Q(author__username__icontains=search) |
            Q(title__icontains=search) | Q(content__icontains=search)
        ).distinct()
    page = 'blog/posts.html'
    context = {
        'list_of_posts': list_of_posts
    }
    return render(request, page, context)


def single_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    page = 'blog/single_post.html'
    return render(request, page, {'post': post})


def year(request, year):
    list_of_posts = Post.objects.order_by(
        '-published_date').filter(published_date__year=year)
    page = 'blog/year_posts.html'
    context = {
        'list_of_posts': list_of_posts
    }
    return render(request, page, context)


def year_month(request, year, month):
    list_of_posts = Post.objects.order_by(
        '-published_date').filter(published_date__year=year).filter(published_date__month=month)
    page = 'blog/year_month_posts.html'
    context = {
        'list_of_posts': list_of_posts
    }
    return render(request, page, context)


def category1(request):
    return index(request=request, category='1')


def category2(request):
    return index(request=request, category='2')


def category3(request):
    return index(request=request, category='3')


def category4(request):
    return index(request=request, category='4')


def category5(request):
    return index(request=request, category='5')


def about(request):
    return render(request, 'blog/about.html', {})


def contact(request):
    return render(request, 'blog/contact.html', {})
