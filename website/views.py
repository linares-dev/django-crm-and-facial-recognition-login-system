from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
    # Get all Record(s)
    records = Record.objects.all()

    # Check to see if user is logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # validate user credentials - authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.success(request, "Login Error. Try Again.")
            return redirect('home')
    else:
        return render(request, 'website/home.html', {"records": records})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        # get form
        form = SignUpForm(request.POST)
        # validate form data
        if form.is_valid():
            form.save()
            # Login authenticated user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Successfully registered')
            redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'website/register.html', {'form': form})
    return render(request, 'website/register.html', {'form': form})


def client_record(request, pk):
    if request.user.is_authenticated:
        # get record
        record = Record.objects.get(id=pk)
        return render(request, 'website/record.html', {"record": record})
    else:
        messages.success(request, "You must be logged in to view the page...")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, "deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to view the page...")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'website/add_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated")
            return redirect('home')
        return render(request, 'website/update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

