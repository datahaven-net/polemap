import re
import requests

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import FormView

from main import forms

pole_letters = {
    'a': '63:10',
    'b': '63:09',
    'c': '63:08',
    'd': '63:07',
    'e': '63:06',
    'f': '63:05',
    'g': '63:04',
    'h': '63:03',
    'i': '63:02',
    'j': '63:01',
    'k': '63:00',
    'l': '62:59',
    'm': '62:58',
    'n': '62:57',
    'q': '18:17',
    'r': '18:16',
    's': '18:15',
    't': '18:14',
    'u': '18:13',
    'v': '18:12',
    'w': '18:11',
    'x': '18:10',
    'y': '18:09',
    'z': '18:08',
}

pole_code_map = {
    '63:10': 'a',
    '63:09': 'b',
    '63:08': 'c',
    '63:07': 'd',
    '63:06': 'e',
    '63:05': 'f',
    '63:04': 'g',
    '63:03': 'h',
    '63:02': 'i',
    '63:01': 'j',
    '63:00': 'k',
    '62:59': 'l',
    '62:58': 'm',
    '62:57': 'n',
    '18:17': 'q',
    '18:16': 'r',
    '18:15': 's',
    '18:14': 't',
    '18:13': 'u',
    '18:12': 'v',
    '18:11': 'w',
    '18:10': 'x',
    '18:09': 'y',
    '18:08': 'z',
}


def dd_to_pole_codes(lat_dd, lon_dd):
    lat_head = int(lat_dd)
    lon_head = int(lon_dd)
    lat_tail = ( lat_dd * 1000000.0 - lat_head * 1000000.0 ) / 1000000.0
    lon_tail = ( lon_dd * 1000000.0 - lon_head * 1000000.0 ) / 1000000.0
    lat_min = int(lat_tail * 60.0)
    lon_min = int(lon_tail * 60.0)
    lat_sec = str(int(round(( lat_tail * 60.0 - lat_min ) * 1000.0, 0))).zfill(3).rstrip('0')
    lon_sec = str(int(round(( lon_tail * 60.0 - lon_min ) * 1000.0, 0))).zfill(3).rstrip('0')
    lat_min = str(lat_min).zfill(2)
    lon_min = str(lon_min).zfill(2)
    lat_code = f'{lat_head}:{lat_min}'
    lon_code = f'{lon_head}:{lon_min}'
    lat_letter = pole_code_map.get(lat_code, '')
    lon_letter = pole_code_map.get(lon_code, '')
    if not lat_letter or not lon_letter:
        return None, None
    lat_result = f'{lat_letter}{lat_sec}'.upper()
    lon_result = f'{lon_letter}{lon_sec}'.upper()
    return lat_result, lon_result


class PoleNumbersView(FormView):

    template_name = 'main/input_form.html'
    form_class = forms.PoleNumbersForm
    error_message = 'Please enter a valid pole codes from Anguilla'

    def form_valid(self, form):
        lat_input = form.cleaned_data.get('upper_code', '').strip().lower()
        lon_input = form.cleaned_data.get('lower_code', '').strip().lower()
        gps_dms_input = form.cleaned_data.get('gps_dms_input', '').strip().upper()
        gps_dd_input = form.cleaned_data.get('gps_dd_input', '').strip()
        google_url = form.cleaned_data.get('google_url', '').strip()
        button_show = 'button_show' in form.data
        button_calculate = 'button_calculate' in form.data
        button_read = 'button_read' in form.data

        if button_calculate:
            lat_dd = None
            lon_dd = None
            if gps_dd_input:
                lat_dd, lon_dd = gps_dd_input.split(',')
                try:
                    lat_dd = abs(float(lat_dd.strip()))
                    lon_dd = abs(float(lon_dd.strip()))
                except:
                    messages.error(self.request, 'Input string is not a valid GPS location in Decimal Degrees format')
                    return self.form_invalid(form)
            if gps_dms_input:
                re_result = re.match('^(\d+?)\°(\d+?)\'([\d\.]+?)\"N\s+?(\d+?)\°(\d+?)\'([\d\.]+?)\"W$', gps_dms_input.strip().upper())
                if not re_result:
                    messages.error(self.request, 'Input string is not a valid GPS location in Degrees Minutes Seconds format')
                    return self.form_invalid(form)
                try:
                    lat_deg = re_result.group(1)
                    lat_min = re_result.group(2)
                    lat_sec = re_result.group(3)
                    lon_deg = re_result.group(4)
                    lon_min = re_result.group(5)
                    lon_sec = re_result.group(6)
                    lat_dd = round(float(lat_deg) + ( float(lat_min) + float(lat_sec) / 60.0 ) / 60.0, 6)
                    lon_dd = round(float(lon_deg) + ( float(lon_min) + float(lon_sec) / 60.0 ) / 60.0, 6)
                except:
                    messages.error(self.request, 'Input string is not a valid GPS location in Degrees Minutes Seconds format')
                    return self.form_invalid(form)
            if not lat_dd or not lon_dd:
                messages.error(self.request, 'Please enter GPS location located in Anguilla')
                return self.form_invalid(form)

            lat_result, lon_result = dd_to_pole_codes(lat_dd, lon_dd)
            if not lat_result or not lon_result:
                messages.error(self.request, 'Entered GPS location is not located in Anguilla')
                return self.form_invalid(form)

            ctx = self.get_context_data(form=form)
            ctx['upper_code'] = lat_result
            ctx['lower_code'] = lon_result
            ctx['lat_dd'] = lat_dd
            ctx['lon_dd'] = lon_dd
            ctx['share_link'] = 'https://polemap.ai/{}{}'.format(lat_result.lower(), lon_result.lower())
            self.template_name = 'main/result_page.html'
            return self.render_to_response(ctx)

        if button_read:
            try:
                resp = requests.request('GET', google_url)
                resp.raise_for_status()
            except:
                messages.error(self.request, 'Provided URL address is not valid')
                return self.form_invalid(form)
            re_result = re.match('.+?/maps/place/.+?/\@[\+\-]?[0-9]{1,2}\.?[0-9]{0,8}\,[\+\-]?[0-9]{1,2}\.?[0-9]{0,8}\,[0-9\w]+?/data.+?\!3d([\+\-]?[0-9]{2}\.?[0-9]{0,8})\!4d([\+\-\d\.]+)', resp.url)
            if not re_result:
                re_result = re.match('.+?/maps/place/.+?/\@([\+\-]?[\d\.]+?)\,([\+\-]?[\d\.]+?)\,\d+?\w/.+?', resp.url)
            if not re_result:
                messages.error(self.request, 'Provided URL address is not a valid Google Maps location')
                return self.form_invalid(form)
            print(re_result.groups())
            try:
                lat_dd = abs(float(re_result.group(1)))
                lon_dd = abs(float(re_result.group(2)))
            except:
                messages.error(self.request, 'Provided URL address is not a valid Google Maps location')
                return self.form_invalid(form)

            lat_result, lon_result = dd_to_pole_codes(lat_dd, lon_dd)
            if not lat_result or not lon_result:
                messages.error(self.request, 'Entered GPS location is not located in Anguilla')
                return self.form_invalid(form)

            ctx = self.get_context_data(form=form)
            ctx['upper_code'] = lat_result
            ctx['lower_code'] = lon_result
            ctx['lat_dd'] = lat_dd
            ctx['lon_dd'] = lon_dd
            ctx['share_link'] = 'https://polemap.ai/{}{}'.format(lat_result.lower(), lon_result.lower())
            self.template_name = 'main/result_page.html'
            return self.render_to_response(ctx)

        if button_show:
            if not lat_input or not lon_input:
                messages.error(self.request, 'Please enter both upper and lower pole codes')
                return self.form_invalid(form)
            try:
                num1 = lat_input
                num2 = lon_input
                letter1 = num1[0]
                letter2 = num2[0]
                digits1 = num1[1:].strip()
                digits2 = num2[1:].strip()
            except:
                return self.form_invalid(form)
            if letter2 in 'qrstuvwxyz':
                l_temp = letter2
                d_temp = digits2
                letter2 = letter1
                digits2 = digits1
                letter1 = l_temp
                digits1 = d_temp
            val1 = pole_letters.get(letter1)
            val2 = pole_letters.get(letter2)
            if not val1 or not val2:
                return self.form_invalid(form)
            try:
                head1, _, tail1 = val1.partition(':')
                head2, _, tail2 = val2.partition(':')
                tail1 += '.' + digits1
                tail2 += '.' + digits2
                lat = round(float(head1) + float(tail1) / 60.0, 6)
                lon = round(-1.0 * (float(head2) + float(tail2) / 60.0), 6)
            except:
                return self.form_invalid(form)
            return HttpResponseRedirect(f'https://maps.google.com/maps?&z=23&f=l&mrt=all&t=k&q={lat}%2C{lon}')

        messages.error(self.request, 'Invalid input received')
        return self.form_invalid(form)


def handler404(request, exception, template_name="main/404_error.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response


def handler500(request, template_name="main/500_error.html"):
    response = render(request, template_name)
    response.status_code = 500
    return response
