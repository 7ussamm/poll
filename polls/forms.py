from django import forms
from .models import Poll, Choices

class Pollform(forms.ModelForm):
    choice1 = forms.CharField(  label='First Choice',
                                max_length=100,
                                min_length=3,
                                widget=forms.TextInput(attrs={'class':'form-control'}))

    choice2 = forms.CharField(  label='Second Choice',
                                max_length=100,
                                min_length=3,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta(): # This how we add extra stuff to a class
        model = Poll
        # fields = '__all__' # to import all variables from Poll class
        fields = ['text', 'choice1', 'choice2']

        # to style text like we did for choice1 and choice2
        # but because we don't have access to text from here and it lives in another class in models.py
        # so we have to do it the way underneath in the widgets dictionary
        widgets = {
            'text': forms.TextInput(attrs={'class':'form-control'})
        }


class EditPollForm(forms.ModelForm):

    class Meta():
        model = Poll
        fields = ['text']
        widgets = {
                    'text': forms.TextInput(attrs={'class':'form-control'})
                }


class AddPollForm(forms.ModelForm):

    class Meta():
        model = Choices
        fields = ['choice_text']
