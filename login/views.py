from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from .forms import CustomUserCreationForm, UploadImageForm
from django.contrib.auth.decorators import login_required
from .models import ExtractedText
all_extracted_texts = ExtractedText.objects.all() 
import requests


@login_required(login_url='login')
def home(request):
    extracted_text = None
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            files = {'image': image}  # Ensure the key matches what FastAPI expects

            # Update the URL to point to your FastAPI endpoint
            response = requests.post('https://5776-34-127-51-135.ngrok-free.app/process_image', files=files)
            
            if response.status_code == 200:
                extracted_text = response.json().get('extracted_text')
                if extracted_text:
                    if not ExtractedText.objects.filter(text=extracted_text).exists():
                        ExtractedText.objects.create(text=extracted_text)
                
                return render(request, 'login/home.html', {'form': form, 'extracted_text': extracted_text,
                'all_extracted_texts': all_extracted_texts,})
        
            else:
                print(f"Error: {response.status_code}, {response.text}")  # Log error details
    else:
        form = UploadImageForm()
    
    return render(request, 'login/home.html', {'form': form,
        'extracted_text': extracted_text,
        'all_extracted_texts': all_extracted_texts,})





def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            CustomUser = form.save()
            auth_login(request, CustomUser)
            return redirect('login')  # Redirect to a home page or dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'login/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Redirect to a home page or dashboard
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login/login.html', {'form': form})
