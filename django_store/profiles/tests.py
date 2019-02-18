from django.test import TestCase

from .models import User, Customer


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('test@test.ru', 'test', first_name='Pavel', last_name="Mametev")
        User.objects.create_superuser('admin@admin.ru', 'admin', first_name='Super', last_name='Admin')
    
    def test_user_get_full_name(self):
        """User returns correct his first name and last name"""
        user = User.objects.get(email='test@test.ru')

        self.assertEqual(user.get_full_name(), 'Pavel Mametev')

    def test_user_get_short_name(self):
        """User returns correct first name"""
        user = User.objects.get(email='test@test.ru')

        self.assertEqual(user.get_short_name(), 'Pavel')

    def test_user_is_staff(self):
        """User is created with .create_user shouldn't has is_staff equal True"""
        user = User.objects.get(email='test@test.ru')

        self.assertEqual(user.is_staff, False)

    def test_user_is_superuser(self):
        """User is created with .create_user shouldn't has is_superuser equal True"""
        user = User.objects.get(email='test@test.ru')

        self.assertEqual(user.is_superuser, False)

    def test_admin_is_staff(self):
        """Admin is created with .create_superuser should has is_staff equal True"""
        admin = User.objects.get(email='admin@admin.ru')

        self.assertEqual(admin.is_staff, True)

    def test_admin_is_superuser(self):
        """User is created with .create_superuser should has is_superuser equal True"""
        admin = User.objects.get(email='admin@admin.ru')

        self.assertEqual(admin.is_superuser, True)

    def test_auto_create_customer_to_user(self):
        """Customer should be auto created with a user"""
        user = User.objects.get(email='test@test.ru')

        self.assertTrue(isinstance(user.customer, Customer))
