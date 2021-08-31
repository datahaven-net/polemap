from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView

from main import forms


class PoleNumbersView(FormView):

    template_name = 'main/pole_numbers.html'
    form_class = forms.PoleNumbersForm
    error_message = 'Please enter a valid pole codes from Anguilla'

    def form_valid(self, form):
        lat_input = form.cleaned_data.get('lat').strip().lower()
        lon_input = form.cleaned_data.get('lon').strip().lower()
        try:
            num1 = lat_input
            num2 = lon_input
            letter1 = num1[0]
            letter2 = num2[0]
            digits1 = num1[1:].strip()
            digits2 = num2[1:].strip()
        except:
            return self.render_to_response(self.get_context_data(form=form))
        if letter2 in 'qrstuvwxyz':
            l_temp = letter2
            d_temp = digits2
            letter2 = letter1
            digits2 = digits1
            letter1 = l_temp
            digits1 = d_temp
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
        val1 = pole_letters.get(letter1)
        val2 = pole_letters.get(letter2)
        if not val1 or not val2:
            return self.render_to_response(self.get_context_data(form=form))
        try:
            head1, _, tail1 = val1.partition(':')
            head2, _, tail2 = val2.partition(':')
            tail1 += '.' + digits1
            tail2 += '.' + digits2
            lat = round(float(head1) + float(tail1) / 60.0, 6)
            lon = round(-1.0 * (float(head2) + float(tail2) / 60.0), 6)
        except:
            return self.render_to_response(self.get_context_data(form=form))
        return HttpResponseRedirect('https://maps.google.com/maps?&z=23&f=l&mrt=all&t=k&q={}%2C{}'.format(
            lat,
            lon,
        ))


def handler404(request, exception, template_name="main/404_error.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response


def handler500(request, template_name="main/500_error.html"):
    response = render(request, template_name)
    response.status_code = 500
    return response
