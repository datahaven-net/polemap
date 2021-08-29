from django.forms import forms, fields


class PoleNumbersForm(forms.Form):

    input = fields.CharField()
