import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

# Get the custom user model
User = get_user_model()


@pytest.mark.django_db
def test_render_signup_view_get(client):
    """Test GET request to the SignUp page."""
    response = client.get(reverse('SignUp'))
    assert response.status_code == 200
    assert 'SignUp.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_render_signup_view_post(client):
    """Test POST request to create a new user."""
    response = client.post(
        reverse('SignUp'),
        data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'age': 25,
            'height': 170,
            'weight': 70,
        },
    )
    assert response.status_code == 302  # Redirect after successful signup
    assert response.url == reverse('Home')
    user = User.objects.get(username='testuser')
    assert user.email == 'testuser@example.com'


@pytest.mark.django_db
def test_render_login_view_get(client):
    """Test GET request to the LogIn page."""
    response = client.get(reverse('LogIn'))
    assert response.status_code == 200
    assert 'LogIn.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_render_login_view_post(client, django_user_model):
    """Test POST request to log in a user."""
    user = django_user_model.objects.create_user(username='testuser', password='testpassword123')
    response = client.post(reverse('LogIn'), data={'username': 'testuser', 'password': 'testpassword123'})
    assert response.status_code == 302  # Redirect after successful login
    assert response.url == reverse('Profile')


@pytest.mark.django_db
def test_render_home_page(client):
    """Test the Home page rendering."""
    response = client.get(reverse('Home'))
    assert response.status_code == 200
    assert 'Home.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_render_about_page(client):
    """Test the About page rendering."""
    response = client.get(reverse('About'))
    assert response.status_code == 200
    assert 'About.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_load_profile_user_data(client, django_user_model):
    """Test the Profile page with user data."""
    user = django_user_model.objects.create_user(
        username='testuser', password='testpassword123', email='testuser@example.com', age=25, height=170, weight=70
    )
    client.login(username='testuser', password='testpassword123')
    response = client.get(reverse('Profile'))
    assert response.status_code == 200
    assert 'Profile.html' in [t.name for t in response.templates]
    assert response.context['bmi'] == 24.22  # BMI = weight / (height/100)^2


@pytest.mark.django_db
def test_download_workout_plan(client, django_user_model, tmpdir):
    """Test downloading a workout plan based on BMI."""
    # Create a temporary workout plan file
    workout_dir = tmpdir.mkdir("WorkoutPlans")
    workout_dir.join("Fat_Loss_Workout_Plan.pdf").write("Fake PDF content")

    user = django_user_model.objects.create_user(username='testuser', password='testpassword123', height=170, weight=90)
    client.login(username='testuser', password='testpassword123')

    # Ensure the workout file is served
    response = client.get(reverse('download_workout_plan'))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'
    assert 'Fat_Loss_Workout_Plan.pdf' in response['Content-Disposition']


@pytest.mark.django_db
def test_update_profile(client, django_user_model):
    """Test updating a user's profile with new data."""
    user = django_user_model.objects.create_user(username='testuser', password='testpassword123', age=25, height=170, weight=70)
    client.login(username='testuser', password='testpassword123')

    response = client.post(
        reverse('update_profile'),
        data=json.dumps({'age': 30, 'height': 175, 'weight': 80}),
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.json()['message'] == 'Profile updated successfully'

    user.refresh_from_db()
    assert user.age == 30
    assert user.height == 175
    assert user.weight == 80