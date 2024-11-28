from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    return render(request,'index.html')
@csrf_exempt
def SignUp(request):
    return render(request,'SignUp.html')

def Home(request):
    # Static data for testing
    height = 170  # Example height in cm
    weight = 70   # Example weight in kg

    
    height_m = height / 100  
    bmi = round(weight / (height_m ** 2), 2) 

    context = {
        'bmi': bmi,
        'height': height,
        'weight': weight,
    }
    return render(request, 'Home.html', context)

def Profile(request):
    return render(request,'Profile.html')