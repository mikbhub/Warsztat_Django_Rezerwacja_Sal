from django.test import TestCase
from django.urls import reverse
from rezerwacje.models import Auditorium, Reservation
import datetime
from django.utils import timezone


# Create your tests here.
def create_auditorium(*args, **kwargs):
    return Auditorium.objects.create(*args, **kwargs)


def create_reservation(days, auditorium):
    time = timezone.now() + datetime.timedelta(days=days)
    return Reservation.objects.create(date=time, auditorium=auditorium)


class ShowSearchResultsTests(TestCase):

    def test_no_auditoriums(self):
        response = self.client.get(reverse('search:search-results'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No free Auditoriums are available for given date.")
        self.assertQuerysetEqual(response.context['auditoriums'], [])

    def test_past_reservation(self):
        """
        Auditorium is already reserved for day in the past. User wants to reserve today.
        """
        auditorium = create_auditorium(name="Bacha Macha", capacity=300)
        reservation = create_reservation(days=-2, auditorium=auditorium)
        today = timezone.now().date()
        response = self.client.get(reverse('search:search-results')+f'?date={today}')
        self.assertQuerysetEqual(
            response.context['auditoriums'],
            ['<Auditorium: Bacha Macha>']
        )

    def test_today_reservation(self):
        """
        Auditorium is already reserved for today. User wants to reserve today.
        """
        auditorium = create_auditorium(name="Bacha Macha", capacity=300)
        reservation = create_reservation(days=0, auditorium=auditorium)
        today = timezone.now().date()
        response = self.client.get(reverse('search:search-results') + f'?date={today}')
        self.assertQuerysetEqual(
            response.context['auditoriums'],
            []
        )

    def test_future_reservation(self):
        """
        Auditorium is already reserved for today. User wants to reserve for tomorrow.
        """
        auditorium = create_auditorium(name="Bacha Macha", capacity=300)
        reservation = create_reservation(days=0, auditorium=auditorium)
        tomorrow = timezone.now().date() + datetime.timedelta(1)
        response = self.client.get(reverse('search:search-results') + f'?date={tomorrow}')
        self.assertQuerysetEqual(
            response.context['auditoriums'],
            ['<Auditorium: Bacha Macha>']
        )
