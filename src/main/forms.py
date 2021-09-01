from django.forms import forms, fields
from django.core.validators import RegexValidator


class PoleNumbersForm(forms.Form):

    lat = fields.CharField(
        label='',
        help_text='upper code, for example: S17',
        required=True,
        validators=[RegexValidator(
            regex='^\s*?[q-zQ-Y]\s*?\d\d\d?\s*?$',
            message='The first character in the upper code should be a letter between Q and Y.  After this there should be 2 or 3 numerical characters.',
            code='invalid',
        ), ],
    )

    lon = fields.CharField(
        label='',
        help_text='lower code, for example: J44',
        required=True,
        validators=[RegexValidator(
            regex='^\s*?[a-nA-N]\s*?\d\d\d?\s*?$',
            message=' The first character in the lower code should be a letter between A and N.  After this there should be 2 or 3 numerical characters.',
            code='invalid',
        ), ],
    )
