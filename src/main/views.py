import re

from django import shortcuts
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from main import forms


class PoleNumbersView(FormView):

    template_name = 'main/pole_numbers.html'
    form_class = forms.PoleNumbersForm
    # success_url = reverse_lazy('pole_numbers')
    error_message = 'Please enter a valid Anguilla Pole Numbers'

    def form_valid(self, form):
        pole_numbers_input = form.cleaned_data.get('input').strip().lower()
        if not pole_numbers_input:
            messages.error(self.request, self.error_message)
            return self.render_to_response(self.get_context_data(form=form))
        result = re.match('^(\w\s?\d\d\d?)\s?(\w\s?\d\d\d?)$', pole_numbers_input)
        if not result:
            messages.error(self.request, self.error_message)
            # return self.render_to_response(self.get_context_data(form=form))
            # return super().form_invalid(form)
            # messages.error(self.request, self.error_message)
            # return HttpResponseRedirect(self.request.path_info)
            # return self.render_to_response(self.get_context_data(form=form))
            return self.render_to_response(self.get_context_data(form=form))
        try:
            num1 = result.group(1)
            num2 = result.group(2)
            letter1 = num1[0]
            letter2 = num2[0]
            digits1 = num1[1:].strip()
            digits2 = num2[1:].strip()
        except:
            messages.error(self.request, self.error_message)
            return self.render_to_response(self.get_context_data(form=form))
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
        }
        val1 = pole_letters.get(letter1)
        val2 = pole_letters.get(letter2)
        if not val1 or not val2:
            messages.error(self.request, self.error_message)
            return self.render_to_response(self.get_context_data(form=form))
        try:
            head1, _, tail1 = val1.partition(':')
            head2, _, tail2 = val2.partition(':')
            tail1 += '.' + digits1
            tail2 += '.' + digits2
            lat = round(float(head1) + float(tail1) / 60.0, 6)
            lon = round(-1.0 * (float(head2) + float(tail2) / 60.0), 6)
        except:
            messages.error(self.request, self.error_message)
            return self.render_to_response(self.get_context_data(form=form))
        return HttpResponseRedirect('https://www.google.com/maps/search/?api=1&query={}%2C{}'.format(lat, lon))


def handler404(request, exception, template_name="main/404_error.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response


def handler500(request, template_name="main/500_error.html"):
    response = render(request, template_name)
    response.status_code = 500
    return response
