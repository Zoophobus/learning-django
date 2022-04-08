from django import forms
from django.utils import timezone

from .models import Sequence

class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields=['sequence_name','type_of_code','type_of_sequence','sequence','publication_date','start_offset','coding_regions']
        widgets={
                'publication_date' : forms.DateTimeInput(attrs={
                    'type' : 'datetime-local',
                    'class' : 'form-control'},
                    format='%y-%m-%dT%H:%M'),
                }


class SequencesListForm(forms.Form):
    sequences_list = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Sequence.objects.filter(publication_date__lte=timezone.now()),
        to_field_name="sequence_name",
        initial=0,
        )
