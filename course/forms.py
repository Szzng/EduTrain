from django import forms
from .models import CourseReview


class ReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ['comment']

        labels = {
            'comment': '',
        }

        widgets = {
            'comment': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': '연수에 대한 한 마디',
                }
            ),
        }
