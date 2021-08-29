# coding=utf-8
import mock
import pytest

from django.test import TestCase
from django.conf import settings


class TestPoleNumbersView(TestCase):

    def test_redirect_success(self):
        response = self.client.post('/', data=dict(input='S17J44'))
        assert response.status_code == 302
        assert response.url == 'https://www.google.com/maps/search/?api=1&query=18.252833%2C-63.024'

    @mock.patch('django.contrib.messages.error')
    def test_invalid_input(self, mock_messages_error):
        response = self.client.post('/', data=dict(input='wrong input'), follow=True)
        assert response.status_code == 200
        assert mock_messages_error.call_args.args[1] == 'Please enter a valid Anguilla Pole Numbers'


class TestErrorViews(TestCase):

    def test_404_handler(self):
        response = self.client.get('/notfound/')
        assert response.status_code == 404
