# coding=utf-8
from django.test import TestCase


class TestPoleNumbersView(TestCase):

    def test_redirect_success(self):
        response = self.client.post('/', data=dict(lat='S17', lon='J44'))
        assert response.status_code == 302
        assert response.url == 'https://maps.google.com/maps?&z=23&f=l&mrt=all&t=k&q=18.252833%2C-63.024'

    def test_invalid_input(self):
        response = self.client.post('/', data=dict(lat='wrong', lon='input'), follow=True)
        assert response.status_code == 200
        assert response.context['field_errors'] == ['The first character in the upper code should be a letter between Q and Y.  After this there should be 2 or 3 numerical characters.']


class TestErrorViews(TestCase):

    def test_404_handler(self):
        response = self.client.get('/notfound/')
        assert response.status_code == 404
