from django.forms import forms, fields
from django.core.validators import RegexValidator


class PoleNumbersForm(forms.Form):

    upper_code = fields.CharField(
        label='',
        help_text='upper code',
        required=False,
    )

    lower_code = fields.CharField(
        label='',
        help_text='lower code',
        required=False,
    )

    gps_dms_input = fields.CharField(
        label='',
        help_text='GPS location as "Degrees Minutes Seconds"',
        required=False,
    )

    gps_dd_input = fields.CharField(
        label='',
        help_text='GPS location as "Decimal Degrees"',
        required=False,
    )

    google_url = fields.CharField(
        label='',
        help_text='Google Maps share link or full URL address',
        required=False,
    )

    def clean(self):
        cleaned_data = super(PoleNumbersForm, self).clean()
        upper_code = cleaned_data.get('upper_code', '').strip()
        lower_code = cleaned_data.get('lower_code', '').strip()
        gps_dms_input = cleaned_data.get('gps_dms_input', '').strip()
        gps_dd_input = cleaned_data.get('gps_dd_input', '').strip()
        google_url = cleaned_data.get('google_url', '').strip()
        button_show = 'button_show' in self.data
        button_calculate = 'button_calculate' in self.data
        button_read = 'button_read' in self.data
        if button_show:
            gps_dms_input = cleaned_data.pop('gps_dms_input', '') and ''
            gps_dd_input = cleaned_data.pop('gps_dd_input', '') and ''
            google_url = cleaned_data.pop('google_url', '') and ''
        if button_calculate:
            upper_code = cleaned_data.pop('upper_code', '') and ''
            lower_code = cleaned_data.pop('lower_code', '') and ''
            google_url = cleaned_data.pop('google_url', '') and ''
        if button_read:
            upper_code = cleaned_data.pop('upper_code', '') and ''
            lower_code = cleaned_data.pop('lower_code', '') and ''
            gps_dd_input = cleaned_data.pop('gps_dd_input', '') and ''
            gps_dms_input = cleaned_data.pop('gps_dms_input', '') and ''
        if upper_code:
            RegexValidator(
                regex='^\s*?[q-zQ-Y]\s*?\d{1,4}\s*?$',
                message='The first character in the upper code should be a letter between Q and Y. After this there should be from 1 to 4 numerical characters.',
                code='invalid',
            )(upper_code)
        if lower_code:
            RegexValidator(
                regex='^\s*?[a-nA-N]\s*?\d{1,4}\s*?$',
                message=' The first character in the lower code should be a letter between A and N. After this there should be from 1 to 4 numerical characters.',
                code='invalid',
            )(lower_code)
        if gps_dms_input:
            RegexValidator(
                regex='^\d+?\°\d+?\'[\d\.]+?\"N\s+?\d+?\°\d+?\'[\d\.]+?\"W$',
                message='Input value must be a GPS location coordinates separated with space and formatted with degree sign, apostrophe and quotation mark symbols: XX°XX\'XX.X\"N YY°YY\'YY.Y\"W',
                code='invalid',
            )(gps_dms_input)
        if gps_dd_input:
            RegexValidator(
                regex='^[\+\-]?[\d\.]+?\s*?\,\s*?[\-\+]?[\d\.]+?$',
                message='Input value must be a GPS location coordinates separated with comma and formatted as decimal degrees: XX.XXXXX, -YY.YYYYY',
                code='invalid',
            )(gps_dd_input)
        if google_url:
            RegexValidator(
                regex='^https?\:\/\/[\d\w\.\-\/\%\'\+\!\:\=\,\`\@\?]+?$',
                message='Please input a valid URL link',
                code='invalid',
            )(google_url)
        return cleaned_data
