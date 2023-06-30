from django.forms import forms

from ads.models import Response, Advert
from ads.templatetags.custom_filters import bad_words

from django import forms
from django.forms import ModelForm


class ResponsesForm(ModelForm):
    text = forms.CharField(max_length=512)

    class Meta:
        model = Response
        fields = [
            'text',
            'response_text',
        ]
        widgets = {
            'response_text': forms.HiddenInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")

        for word in bad_words:
            if word in text:
                raise forms.ValidationError("Your text contains obscene language, correct it and try again.")

        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ('title', 'response_text', 'category', 'upload')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'response_text': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'upload': forms.FileInput(attrs={'class': 'form-control'}),
        }
