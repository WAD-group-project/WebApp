from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model

Member = get_user_model()  # Ensure we get the correct user model

from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta
from your_app.models import User  # Directly use your custom User model

class LoginTests(TestCase):

    def setUp(self):
        # Create a sample user with valid credentials and renewal date
        self.valid_user = User.objects.create(
            Username='testuser',
            password='password123',  # Store raw password for testing
            renewal_date=now() + timedelta(days=30)
        )
        self.valid_user.save()

        # Create a user with an expired membership
        self.expired_user = User.objects.create(
            Username='expireduser',
            password='password456',
            renewal_date=now() - timedelta(days=1)
        )
        self.expired_user.save()

    def test_login_valid_user(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, testuser')

    def test_login_invalid_password(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertContains(response, 'Invalid credentials')

    def test_login_expired_membership(self):
        response = self.client.post('/login/', {
            'username': 'expireduser',
            'password': 'password456'
        })
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'Membership expired. Please renew.')

    def test_login_nonexistent_user(self):
        response = self.client.post('/login/', {
            'username': 'nonexistent',
            'password': 'password789'
        })
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'User not found')



class AccountCreationTests(TestCase):

    def setUp(self):
        # Create a sample user for uniqueness testing
        self.existing_user = User.objects.create(
            Username='uniqueuser',
            password='password123',
            renewal_date=now() + timedelta(days=30)
        )
        self.existing_user.save()

    def test_account_creation_with_valid_data(self):
        response = self.client.post('/register/', {
            'username': 'validuser',
            'password': 'strongpassword123',
            'email': 'validuser@example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, 'Account created successfully')
        self.assertTrue(User.objects.filter(Username='validuser').exists())

    def test_account_creation_with_missing_data(self):
        response = self.client.post('/register/', {
            'username': 'userwithmissingemail',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Email field is required')
        self.assertFalse(User.objects.filter(Username='userwithmissingemail').exists())

    def test_account_creation_with_invalid_email(self):
        response = self.client.post('/register/', {
            'username': 'userwithinvalidemail',
            'password': 'password123',
            'email': 'notanemail'
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Enter a valid email address')
        self.assertFalse(User.objects.filter(Username='userwithinvalidemail').exists())

    def test_create_account_with_existing_username(self):
        response = self.client.post('/register/', {
            'username': 'uniqueuser',
            'password': 'newpassword123',
            'email': 'newemail@example.com'
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Username already exists')

    def test_create_account_with_new_username(self):
        response = self.client.post('/register/', {
            'username': 'newuniqueuser',
            'password': 'anotherpassword123',
            'email': 'anotheruser@example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, 'Account created successfully')
        self.assertTrue(User.objects.filter(Username='newuniqueuser').exists())


