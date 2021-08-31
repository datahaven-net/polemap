from django.forms import forms, fields
from django.core.validators import RegexValidator


class PoleNumbersForm(forms.Form):

    lat = fields.CharField(
        label='upper code:',
        required=True,
        validators=[RegexValidator(
            regex='^\s*?[q-zQ-Y]\s*?\d\d\d?\s*?$',
            message='The first character in the upper code should be a letter between Q and Y with the other 2 or 3 digits numbers.',
            code='invalid',
        ), ],
    )

    lon = fields.CharField(
        label='lower code:',
        required=True,
        validators=[RegexValidator(
            regex='^\s*?[a-nA-N]\s*?\d\d\d?\s*?$',
            message='The first character in the lower code should be a letter between A and N with the other 2 or 3 digits numbers.',
            code='invalid',
        ), ],
    )
