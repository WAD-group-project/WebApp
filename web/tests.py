from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta
from django.urls import reverse
from models.py import User, Staff, Activity


class LoginTests(TestCase):
    def setUp(self):
        self.valid_user = User.objects.create_user(
            username='testuser', password='password123', renewal_date=now() + timedelta(days=30)
        )
        self.expired_user = User.objects.create_user(
            username='expireduser', password='password123', renewal_date=now() - timedelta(days=1)
        )
        self.nonexistent_user = "nonexistent"

    def test_login_valid_user(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, testuser')

    def test_login_invalid_password(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)
        self.assertContains(response, 'Invalid credentials')

    def test_login_expired_membership(self):
        response = self.client.post('/login/', {'username': 'expireduser', 'password': 'password123'})
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'Membership expired')

    def test_login_nonexistent_user(self):
        response = self.client.post('/login/', {'username': self.nonexistent_user, 'password': 'password123'})
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'User not found')


class AccountCreationTests(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='uniqueuser', password='password123', renewal_date=now() + timedelta(days=30)
        )

    def test_account_creation_with_valid_data(self):
        response = self.client.post('/register/', {
            'username': 'newuser', 'password': 'newpassword123', 'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, 'Account created successfully')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_account_creation_with_missing_email(self):
        response = self.client.post('/register/', {
            'username': 'userwithoutemail', 'password': 'password123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Email is required')
        self.assertFalse(User.objects.filter(username='userwithoutemail').exists())

    def test_account_creation_with_existing_username(self):
        response = self.client.post('/register/', {
            'username': 'uniqueuser', 'password': 'anotherpassword123', 'email': 'anotheremail@example.com'
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Username already exists')


class StaffTests(TestCase):
    def setUp(self):
        self.staff_user = Staff.objects.create(StaffID="STAFF001", JobTitle="Manager")
        self.non_staff_user = User.objects.create_user(username="nonstaff", password="password123")

    def test_staff_only_access(self):
        response = self.client.post('/staffonly/', {'StaffID': 'STAFF001'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, Manager')

    def test_non_staff_access_denied(self):
        response = self.client.post('/staffonly/', {'StaffID': 'INVALIDID'})
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'Access denied')


class MemberBookingTests(TestCase):
    def setUp(self):
        self.valid_member = User.objects.create_user(
            username='validmember', password='password123', renewal_date=now() + timedelta(days=30)
        )
        self.expired_member = User.objects.create_user(
            username='expiredmember', password='password123', renewal_date=now() - timedelta(days=1)
        )
        self.non_member = User.objects.create_user(
            username='nonmember', password='password123'
        )
        self.activity = Activity.objects.create(
            Title="Yoga Class", Description="Morning Yoga", Start=now() + timedelta(days=1),
            End=now() + timedelta(days=1, hours=1), Capacity=10
        )

    def test_valid_member_can_book_class(self):
        self.client.login(username='validmember', password='password123')
        response = self.client.post(reverse("book_class"), {'class_id': self.activity.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Booking successful')
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.Capacity, 9)

    def test_expired_member_cannot_book_class(self):
        self.client.login(username='expiredmember', password='password123')
        response = self.client.post(reverse("book_class"), {'class_id': self.activity.id})
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'Membership expired')
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.Capacity, 10)

    def test_non_member_cannot_book_class(self):
        self.client.login(username='nonmember', password='password123')
        response = self.client.post(reverse("book_class"), {'class_id': self.activity.id})
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'Only members can book classes')
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.Capacity, 10)

    def test_member_can_unbook_class(self):
        self.client.login(username='validmember', password='password123')
        self.activity.Capacity -= 1  # Simulate a booking
        self.activity.save()

        response = self.client.post(reverse("unbook_class"), {'class_id': self.activity.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unbooking successful')
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.Capacity, 10)
