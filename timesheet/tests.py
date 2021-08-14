from django.test import TestCase
from timesheet.models import TimesheetModel
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime 


class TimesheetModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        TimesheetModel.objects.create(date=datetime.now(), from_hour="8:20", to_hour='17:30', description='Test', author=user)

        user2 = User.objects.create(username='testuser2')
        user2.set_password('12345')
        user2.save()

        user3 = User.objects.create(username='testuser3')
        user3.set_password('12345')
        user3.save()

    def test_timesheet_view_overview(self):
        response = self.client.get(reverse('overview_timesheet'))
        self.assertEqual(response.status_code, 302)

        login = self.client.login(username='testuser', password='12345')
        self.assertEqual(login, True)
        response = self.client.get(reverse('overview_timesheet'))
        self.assertEqual(response.status_code, 200)

    def test_timesheet_view_creates(self):
        response = self.client.get(reverse('timesheet_view_create'))
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser', password='12345')
        self.assertEqual(login, True)
        response = self.client.get(reverse('timesheet_view_create'))
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='12345')
        self.assertEqual(login, True)
        response = self.client.get(reverse('timesheet_view_create'))
        self.assertEqual(response.status_code, 200)
        self.client.post('/create/', {'from_hour': "6:20", 'to_hour':"17:30", 'description':'Test'})
        self.assertEqual(TimesheetModel.objects.last().description, "Test")

    
    def test_timesheet_view_update(self):
        user = User.objects.get(username='testuser')
        obj = TimesheetModel.objects.filter(author=user.id)

        response = self.client.get(f'/update/{obj[0].id}/')
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser', password='12345')
        self.assertEqual(login, True)
        response = self.client.get(f'/update/{obj[0].id}/')
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username='testuser3', password='12345')
        self.assertEqual(login, True)
        response = self.client.get(f'/update/{obj[0].id}/')
        self.assertEqual(response.status_code, 403)

    