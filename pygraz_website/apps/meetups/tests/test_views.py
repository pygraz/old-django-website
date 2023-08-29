from http import HTTPStatus

import arrow
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseNotFound
from django.test import TestCase
from django.utils import timezone

from .. import models


class MeetupViewTests(TestCase):
    def setUp(self):
        self.now = timezone.now()
        self.past_meetup = models.Meetup(start_date=self.now - timezone.timedelta(days=2))
        self.past_meetup.save()
        rsvp = models.RSVP(
            meetup=self.past_meetup,
            remote_username="remote_user",
            remote_uid="remote_uid",
            source="meetupcom",
            status="coming",
        )
        rsvp.save()
        self.future_meetup = models.Meetup(start_date=self.now + timezone.timedelta(days=2))
        self.future_meetup.save()

    def tearDown(self):
        self.future_meetup.delete()
        self.past_meetup.delete()

    def test_view_not_existing(self):
        """
        Tests that a request for a not-existing meetup results in a 404 page.
        """
        self.assertEqual(self.client.get("/meetups/123/").status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(self.client.get("/meetups/2015-05-01/").status_code, HTTPStatus.NOT_FOUND)

    def test_view_existing(self):
        """
        Tests that a meetup can be accessed by its URL.
        """
        resp = self.client.get(f"/meetups/{self.past_meetup.pk}/")
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, len(resp.context["rsvps"].coming))

    def test_view_existing_via_date(self):
        """
        The primary URL of a meetup is one containing its date for better SEO.
        """
        date = arrow.get(self.past_meetup.start_date).format("YYYY-MM-DD")
        response = self.client.get(f"/meetups/{date}/")
        self.assertEqual(200, response.status_code)

    def test_upcoming_on_frontpage(self):
        """
        Tests that the next meetup is displayed on the frontpage.
        """
        resp = self.client.get("/")
        self.assertEqual(200, resp.status_code)
        self.assertEqual(self.future_meetup, resp.context["next_meetup"])


class SessionViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="username", password="password", email="test@test.com")
        self.session = models.Session(title="Some session", abstract="abstract", speaker=self.user)
        self.session.save()

    def test_anonymous_view(self):
        resp = self.client.get(f"/meetups/sessions/{self.session.pk}/")
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertFalse(resp.context["can_edit"])
        self.assertFalse(resp.context["can_delete"])

    def test_author_view(self):
        self.client.login(username="username", password="password")
        resp = self.client.get(f"/meetups/sessions/{self.session.pk}/")
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertTrue(resp.context["can_edit"])
        self.assertTrue(resp.context["can_delete"])


class DeleteSessionViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="username", password="password", email="test@test.com")
        self.other_user = User.objects.create_user(
            username="other_username", password="password", email="other@test.com"
        )
        self.session = models.Session(title="Some session", abstract="abstract", speaker=self.user)
        self.session.save()

    def test_anonymous_view(self):
        url = f"/meetups/sessions/{self.session.pk}/delete/"
        resp = self.client.get(url)
        self.assertRedirects(resp, f"/accounts/signin/?next={url}")

    def test_otheruser_view(self):
        self.client.login(username="other_username", password="password")
        url = f"/meetups/sessions/{self.session.pk}/delete/"
        resp = self.client.get(url)
        self.assertEqual(403, resp.status_code)

    def test_author_view(self):
        self.client.login(username="username", password="password")
        url = f"/meetups/sessions/{self.session.pk}/delete/"
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)

        resp = self.client.post(url)
        self.assertEqual(302, resp.status_code)
        self.assertEqual(0, models.Session.objects.count())


class SubmitSessionViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="username", password="password", email="test@test.com")
        self.talk_type = models.SessionType(name="Talk")
        self.talk_type.save()

    def test_loggedin_view(self):
        url = "/meetups/sessions/submit/?next=/"
        self.client.login(username="username", password="password")
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)

        resp = self.client.post(
            url,
            {
                "title": "title",
                "abstract": "abstract",
                "type": self.talk_type.pk,
            },
        )
        self.assertRedirects(resp, "/")
        sessions = list(models.Session.objects.all())
        self.assertEqual(1, len(sessions))
        self.assertEqual("title", sessions[0].title)
        self.assertEqual("abstract", sessions[0].abstract)
        self.assertEqual(self.user, sessions[0].speaker)


class EditSessionViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="username", password="password", email="test@test.com")
        self.other_user = User.objects.create_user(
            username="other_username", password="password", email="other@test.com"
        )
        self.talk_type = models.SessionType(name="Talk")
        self.talk_type.save()
        self.session = models.Session(title="Some session", abstract="abstract", speaker=self.user, type=self.talk_type)
        self.session.save()

    def test_anonymous_view(self):
        url = "/meetups/sessions/1/edit/"
        resp = self.client.get(url)
        self.assertRedirects(resp, f"/accounts/signin/?next={url}")

    def test_author_view(self):
        self.client.login(username="username", password="password")
        url = "/meetups/sessions/1/edit/"
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)

        resp = self.client.post(url, {"title": "New title", "abstract": "New abstract", "type": self.talk_type.pk})
        self.assertEqual(302, resp.status_code)
        session = models.Session.objects.get(pk=self.session.pk)
        self.assertEqual(session.title, "New title")
        self.assertEqual(session.abstract, "New abstract")
