from django import forms
from courses.models import Review

class ReviewForm(forms.ModelForm):
    """
    ModelForm demonstrating automated form generation from model schema.
    """
    class Meta:
        model = Review
        fields = ['student_name', 'rating', 'comment']
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-900 text-white focus:ring-2 focus:ring-indigo-500 text-sm',
                'placeholder': 'Your Name or Student ID'
            }),
            'rating': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-900 text-white focus:ring-2 focus:ring-indigo-500 text-sm'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-900 text-white focus:ring-2 focus:ring-indigo-500 text-sm',
                'rows': 3,
                'placeholder': 'Write your review or feedback on this course...'
            }),
        }
