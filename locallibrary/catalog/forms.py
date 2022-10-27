
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gtl


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3)."
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check is data is not in the past
        if data < datetime.date.today():
            raise ValidationError(gtl('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+delta weeks from today)
        delta = 4
        if data > datetime.date.today() + datetime.timedelta(weeks=delta):
            raise ValidationError(
                gtl(f'Invalid date - renewal more than {delta} weeks ahead')
            )

        return data
        