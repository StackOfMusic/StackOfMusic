from django import forms

from instrument.models import Instrument


class MusicSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word', max_length=100, required=False)
    instruments = forms.ModelMultipleChoiceField(Instrument.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
