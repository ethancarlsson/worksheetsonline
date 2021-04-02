from django.test import TestCase

from .models import OriginalWorksheet, Profile, CustomUser

from time import time

class TestHelpers:

    def create_new_user(self, username='test_man', password='Sexypssword69'):
        return CustomUser.objects.get_or_create(username=username, password=password)[0]

    def create_new_user_2(self, username='test_man2', password='Sexypssword699'):
        return CustomUser.objects.get_or_create(username=username, password=password)[0]


    def create_worksheet(self):
        worksheet = OriginalWorksheet.objects.get_or_create(
            name='worksheet',
            original_text='something___ /n otherthing____',
            worksheet_owner=self.create_new_user()
            )[0]
        return worksheet

    def create_profile(self):
        user = self.create_new_user_2()
        return Profile.objects.get(user=user)



