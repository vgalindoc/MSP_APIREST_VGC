from django.test import TestCase
from django.contrib.auth import get_user_model
 
class ModelTests(TestCase):
   
    def test_create_user_with_email_successful(self):
        email = 'vgalindoc@email.com'
        password = 'testuservgc'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
       
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
 
    def test_new_user_email_normalized(self):
        sample_emails = [
            ['VgalindoC@email.com','vgalindoc@email.com'],
            ['vgal1ndoC@email.COM','vgalindoc@email.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email,'testnormalized')
            self.assertEqual(user.email, expected)
           
    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','testnoemail')
           
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
        'vgalindoc@email.com',
        'testsuperuservgc',
        )
       
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
 
