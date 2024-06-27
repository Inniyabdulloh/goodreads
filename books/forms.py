from django import forms
from .models import Review

class BookReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('comment',)