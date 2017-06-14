from django.test import TestCase

from .models import UserProfile, Department

# Create your tests here.


# class UserProfileTest(TestCase):
#
#     def test_create(self):
#         user = UserProfile()
#         user.objects.create_superuser(username='hao', email='1@1.com', password='hao123456')
#         self.assertTrue(user)


class DepartemtTest(TestCase):

    def test_create_department(self):
        department = Department.objects.create(name='阿里爸爸')
        department.save()