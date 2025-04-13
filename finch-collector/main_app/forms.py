from django import forms
from .models import Feeding, Photo

class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['url', 'title']        