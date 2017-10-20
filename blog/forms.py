from django import forms

from .models import Crawler

class CrawlerForm(forms.ModelForm):

    class Meta:
        model = Crawler
        fields = ('search',)
