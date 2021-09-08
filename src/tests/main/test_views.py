# coding=utf-8
import mock
from django.test import TestCase


class TestPoleNumbersView(TestCase):

    def test_button_show(self):
        response = self.client.post('/', data=dict(
            upper_code='S17',
            lower_code='J44',
            button_show='1',
        ))
        assert response.status_code == 302
        assert response.url == 'https://maps.google.com/maps?&z=23&f=l&mrt=all&t=k&q=18.252833%2C-63.024'

    def test_button_calculate(self):
        response = self.client.post('/', data=dict(
            gps_dd_input='18.252833, -63.024000',
            button_calculate='1',
        ))
        assert response.status_code == 200
        assert response.context['upper_code'] == 'S17'
        assert response.context['lower_code'] == 'J44'
        assert response.context['lat_dd'] == 18.252833
        assert response.context['lon_dd'] == 63.024
        assert response.context['share_link'] == 'https://polemap.ai/s17j44'

    @mock.patch('requests.request')
    def test_button_read(self, request_mock):
        request_mock.return_value = mock.MagicMock(
            url="https://www.google.com/maps/place/18%C2%B015'10.2%22N+63%C2%B001'26.4%22W/@18.252833,-63.0261887,1024m/data=!3m2!1e3!4b1!4m5!3m4!1s0x0:0x0!8m2!3d18.252833!4d-63.024"
        )
        response = self.client.post('/', data=dict(
            google_url='https://goo.gl/maps/nmeJyCn1oGudvLY29',
            button_read='1',
        ))
        assert response.status_code == 200
        assert response.context['upper_code'] == 'S17'
        assert response.context['lower_code'] == 'J44'
        assert response.context['lat_dd'] == 18.252833
        assert response.context['lon_dd'] == 63.024
        assert response.context['share_link'] == 'https://polemap.ai/s17j44'

    def test_invalid_input(self):
        response = self.client.post('/', data=dict(lat='wrong', lon='input'), follow=True)
        assert response.status_code == 200
        assert response.content.count(b'Invalid input received')


class TestErrorViews(TestCase):

    def test_404_handler(self):
        response = self.client.get('/notfound/')
        assert response.status_code == 404
