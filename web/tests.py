from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model

Member = get_user_model()  # Ensure we get the correct user model

class LoginTests(TestCase):

    def setUp(self):
        # Create a sample member with valid credentials and renewal date
        self.valid_user = Member.objects.create(username='testuser', renewal_date=now() + timedelta(days=30))
        self.valid_user.set_password('password123')  # Hash the password correctly
        self.valid_user.save()

        # Create an expired member
        self.expired_user = Member.objects.create(username='expireduser', renewal_date=now() - timedelta(days=1))
        self.expired_user.set_password('password456')
        self.expired_user.save()

    def test_login_valid_user(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)  # Adjust if your view redirects
        self.assertContains(response, 'Welcome, testuser')

    def test_login_invalid_password(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)  # Adjust based on your view
        self.assertContains(response, 'Invalid credentials')

    def test_login_expired_membership(self):
        response = self.client.post('/login/', {'username': 'expireduser', 'password': 'password456'})
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'Membership expired. Please renew.')

    def test_login_nonexistent_user(self):
        response = self.client.post('/login/', {'username': 'nonexistent', 'password': 'password789'})
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'User not found')



class AccountCreationTests(TestCase):

    def setUp(self):
        # Create a sample member with a unique username for testing uniqueness
        self.existing_user = Member.objects.create(
            username='uniqueuser',
            password='password123',
            renewal_date=now() + timedelta(days=30)  # Renewal date 30 days from now
        )

    def test_account_creation_with_valid_data(self):
        # Test creating an account with valid data
        response = self.client.post('/register/', {
            'username': 'validuser',
            'password': 'strongpassword123',
            'email': 'validuser@example.com'
        })
        self.assertEqual(response.status_code, 201)  # Adjust for expected success code
        self.assertContains(response, 'Account created successfully')
        self.assertTrue(Member.objects.filter(username='validuser').exists())

    def test_account_creation_with_missing_data(self):
        # Test creating an account with missing required fields (e.g., email)
        response = self.client.post('/register/', {
            'username': 'userwithmissingemail',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 400)  # Adjust for expected error code
        self.assertContains(response, 'Email field is required')
        self.assertFalse(Member.objects.filter(username='userwithmissingemail').exists())

    def test_account_creation_with_invalid_email(self):
        # Test creating an account with an invalid email format
        response = self.client.post('/register/', {
            'username': 'userwithinvalidemail',
            'password': 'password123',
            'email': 'notanemail'
        })
        self.assertEqual(response.status_code, 400)  # Adjust for expected error code
        self.assertContains(response, 'Enter a valid email address')
        self.assertFalse(Member.objects.filter(username='userwithinvalidemail').exists())

    def test_create_account_with_existing_username(self):
        # Attempt to create an account with a duplicate username
        response = self.client.post('/register/', {
            'username': 'uniqueuser',  # Existing username
            'password': 'newpassword123',
            'email': 'newemail@example.com'
        })
        self.assertEqual(response.status_code, 400)  # Replace with expected failure code
        self.assertContains(response, 'Username already exists')

    def test_create_account_with_new_username(self):
        # Attempt to create an account with a new, unique username
        response = self.client.post('/register/', {
            'username': 'newuniqueuser',
            'password': 'anotherpassword123',
            'email': 'anotheruser@example.com'
        })
        self.assertEqual(response.status_code, 201)  # Replace with expected success code
        self.assertContains(response, 'Account created successfully')
        self.assertTrue(Member.objects.filter(username='newuniqueuser').exists())

