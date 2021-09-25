# coding=utf-8
import mock
from django.test import TestCase

from main import views


class TestCalculations(TestCase):

    def test_pole_codes_to_dd(self):
        assert views.pole_codes_to_dd('V99', 'I91') == (18.2165, -63.0485, )
        assert views.pole_codes_to_dd('U00', 'I91') == (18.216667, -63.0485, )
        assert views.pole_codes_to_dd('V1', 'I9') == (18.201667, -63.048333, )
        assert views.pole_codes_to_dd('V9998', 'I9100') == (18.216663, -63.0485, )
        assert views.pole_codes_to_dd('V9999', 'I9100') == (18.216665, -63.0485, )
        assert views.pole_codes_to_dd('V1001', 'I9100') == (18.201668, -63.0485, )
        assert views.pole_codes_to_dd('V1000', 'I9100') == (18.201667, -63.0485, )
        assert views.pole_codes_to_dd('V0999', 'I9100') == (18.201665, -63.0485, )
        assert views.pole_codes_to_dd('V0099', 'I9100') == (18.200165, -63.0485, )
        assert views.pole_codes_to_dd('S17', 'J44') == views.pole_codes_to_dd('J44', 'S17')

    def test_dd_to_pole_codes(self):
        assert views.dd_to_pole_codes(18.2528361, 63.024001, 1) == ('S2', 'J4', )
        assert views.dd_to_pole_codes(18.2528361, 63.024001, 2) == ('S17', 'J44', )
        assert views.dd_to_pole_codes(18.2528362, 63.024002, 3) == ('S170', 'J440', )
        assert views.dd_to_pole_codes(18.2528361, 63.024001, 4) == ('S1702', 'J4401', )
        assert views.dd_to_pole_codes(18.216667, -63.0485, 1) == ('U0', 'I9', )
        assert views.dd_to_pole_codes(18.216667, -63.0485, 2) == ('U00', 'I91', )
        assert views.dd_to_pole_codes(18.216667, -63.0485, 3) == ('U000', 'I910', )
        assert views.dd_to_pole_codes(18.216667, -63.0485, 4) == ('U0000', 'I9100', )
        assert views.dd_to_pole_codes(18.216666, -63.0485, 1) == ('U0', 'I9', )
        assert views.dd_to_pole_codes(18.216666, -63.0485, 2) == ('U00', 'I91', )
        assert views.dd_to_pole_codes(18.216666, -63.0485, 3) == ('U000', 'I910', )
        assert views.dd_to_pole_codes(18.216666, -63.0485, 4) == ('U0000', 'I9100', )
        assert views.dd_to_pole_codes(18.216665, -63.0485, 1) == ('U0', 'I9', )
        assert views.dd_to_pole_codes(18.216665, -63.0485, 2) == ('U00', 'I91', )
        assert views.dd_to_pole_codes(18.216665, -63.0485, 3) == ('U000', 'I910', )
        assert views.dd_to_pole_codes(18.216665, -63.0485, 4) == ('V9999', 'I9100', )
        assert views.dd_to_pole_codes(18.201665, -63.0485, 1) == ('V1', 'I9', )
        assert views.dd_to_pole_codes(18.201665, -63.0485, 2) == ('V10', 'I91', )
        assert views.dd_to_pole_codes(18.201665, -63.0485, 3) == ('V100', 'I910', )
        assert views.dd_to_pole_codes(18.201665, -63.0485, 4) == ('V0999', 'I9100', )

    def test_dd_to_dms(self):
        assert views.dd_to_dms(18.2528361, 63.024001) == ('18°15\'10.2\"N', '63°01\'26.4\"W')


class TestPoleCodeGoogleMapsView(TestCase):

    def test_success(self):
        response = self.client.get('/s17j44')
        assert response.status_code == 302
        assert response.url == 'https://maps.google.com/maps?&z=23&f=l&mrt=all&t=k&q=18.252833%2C-63.024'

    def test_reversed_input_order(self):
        response = self.client.get('/j44s17')
        assert response.status_code == 302
        assert response.url == 'https://maps.google.com/maps?&z=23&f=l&mrt=all&t=k&q=18.252833%2C-63.024'


class TestPoleCodeInfoView(TestCase):

    def test_success(self):
        response = self.client.get('/s17j44/info')
        assert response.status_code == 200
        assert response.context['upper_code'] == 'S17'
        assert response.context['lower_code'] == 'J44'
        assert response.context['lat_dd'] == 18.252833
        assert response.context['lon_dd'] == -63.024
        assert response.context['lat_dms'] == '18°15\'10.2\"N'
        assert response.context['lon_dms'] == '63°01\'26.4\"W'
        assert response.context['share_link'] == 'https://polemap.ai/s17j44'
        assert response.context['google_url'] == 'https://maps.google.com/maps?&z=23&f=l&mrt=all&t=k&q=18.252833%2C-63.024'

    def test_reversed_input_order(self):
        response = self.client.get('/j44s17/info')
        assert response.status_code == 200
        assert response.context['upper_code'] == 'S17'
        assert response.context['lower_code'] == 'J44'
        assert response.context['lat_dd'] == 18.252833
        assert response.context['lon_dd'] == -63.024
        assert response.context['lat_dms'] == '18°15\'10.2\"N'
        assert response.context['lon_dms'] == '63°01\'26.4\"W'
        assert response.context['share_link'] == 'https://polemap.ai/s17j44'
        assert response.context['google_url'] == 'https://maps.google.com/maps?&z=23&f=l&mrt=all&t=k&q=18.252833%2C-63.024'

    def test_bad_input(self):
        response = self.client.get('/wronginput/info')
        assert response.status_code == 302
        assert response.url == '/'


class TestPoleNumbersView(TestCase):

    def test_button_show(self):
        response = self.client.post('/', data=dict(
            upper_code='S17',
            lower_code='J44',
            button_show='',
        ))
        assert response.status_code == 302
        assert response.url == '/s17j44'

    def test_button_gps(self):
        response = self.client.post('/', data=dict(
            upper_code='S17',
            lower_code='J44',
            button_gps='',
        ))
        assert response.status_code == 302
        assert response.url == '/s17j44/info'

    def test_button_calculate_dd(self):
        response = self.client.post('/', data=dict(
            gps_dd_input='18.252833, -63.024000',
            button_calculate='',
        ))
        assert response.status_code == 302
        assert response.url == '/18.252833,63.024/result'

    def test_button_calculate_dms(self):
        response = self.client.post('/', data=dict(
            gps_dms_input='18°15\'10.2\"N 63°01\'26.4\"W',
            button_calculate='',
        ))
        assert response.status_code == 302
        assert response.url == '/18.252833,-63.024/result'


    def test_button_calculate_high_precision(self):
        response = self.client.post('/', data=dict(
            gps_dd_input='18.252835, -63.024001',
            button_calculate='',
            high_precision='',
        ))
        assert response.status_code == 302
        assert response.url == '/18.252835,63.024001/result'

    @mock.patch('requests.request')
    def test_button_read(self, request_mock):
        request_mock.return_value = mock.MagicMock(
            url="https://www.google.com/maps/place/18%C2%B015'10.2%22N+63%C2%B001'26.4%22W/@18.252833,-63.0261887,1024m/data=!3m2!1e3!4b1!4m5!3m4!1s0x0:0x0!8m2!3d18.252833!4d-63.024"
        )
        response = self.client.post('/', data=dict(
            google_url='https://goo.gl/maps/nmeJyCn1oGudvLY29',
            button_read='',
        ))
        assert response.status_code == 302
        assert response.url == '/18.252833,-63.024/result'

    @mock.patch('requests.request')
    def test_button_read_high_precision(self, request_mock):
        request_mock.return_value = mock.MagicMock(
            url="https://www.google.com/maps/place/18%C2%B015'10.2%22N+63%C2%B001'26.4%22W/@18.252833,-63.0261887,1024m/data=!3m2!1e3!4b1!4m5!3m4!1s0x0:0x0!8m2!3d18.252836!4d-63.02401"
        )
        response = self.client.post('/', data=dict(
            google_url='https://goo.gl/maps/nmeJyCn1oGudvLY29',
            button_read='',
            high_precision='',
        ))
        assert response.status_code == 302
        assert response.url == '/18.252836,-63.02401/result'

    def test_invalid_input(self):
        response = self.client.post('/', data=dict(lat='wrong', lon='input'), follow=True)
        assert response.status_code == 200
        assert response.content.count(b'Invalid input received')


class TestErrorViews(TestCase):

    def test_404_handler(self):
        response = self.client.get('/notfound/')
        assert response.status_code == 404
