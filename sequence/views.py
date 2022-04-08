from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
import re

# from the Sequence app
from .models import Sequence, Alignment
from .forms import SequenceForm, SequencesListForm

# Create your views here.

# if the sequences can't be saved to the database we need to be able to send them
# to the view
def index(request,selected=[]):
    list_form = SequencesListForm(request.GET)
    add = SequenceForm()
    return render(request,'sequence/index.html',
            {
                'add' : add,
                'latest_list' : list_form, 
                'selected' : selected,
                'view_alignment' : False,
                }
            )

    # TODO make changes to this method so that it takes a list
def results(request):
    sequences = []
    print(request.POST)
    print(request.GET)
    sequence = get_object_or_404(Sequence)
    return render(request,'sequence/results.html',
            {
                'sequence' : sequence,
                }
            )

def delete(request,seq_id):
    if request.method == 'POST':
        sequence = get_object_or_404(Sequence,pk=seq_id)
        sequence.delete()
        latest_list = Sequence.objects.order_by('-publication_date')
        return render(request,'sequence/index.html',
            {
                'latest_list' : latest_list,
                'view_alignment' : False,
                }
            )

def add(request):
    if request.method == 'POST':
        add = SequenceForm(request.POST)
        if add.is_valid():
            data = add.cleaned_data
            seq = Sequence(type_of_code= data['type_of_code'], type_of_sequence=data['type_of_sequence'],sequence_name=data['sequence_name'],sequence=data['sequence'],publication_date = data['publication_date'],coding_regions=data['coding_regions'],start_offset=data['start_offset'])
            seq.save()
            add.save(commit=False)
            list_form = Sequence.objects.all() #SequencesListForm(request.GET)
            return HttpResponseRedirect(reverse('sequence:index'),{'form' : add,'latest_list' : list_form, 'selected' : [], 'view_alignment' : False})
    add = SequenceForm()
    list_form = SequencesListForm(request.GET)
    return HttpResponseRedirect(reverse('sequence:index'),{'form' : add, 'latest_list' : list_form})
 
def select(request):
# the sequences_list should here contain the a string that itself will have
# the list of sequence_names (also the primary key for the sequence database
    #selected_list = request.GET.get('selected_sequences')
    # the above gets a single instance, not a list, or selection of
    # instances BEFORE CONTINUING I NEED TO THOROUGHLY READ THROUGH THE
    # DJANGO FORMS DOCUMENTATION
    add = SequenceForm()
    list_form = SequencesListForm(request.GET)
    if request.method == 'POST':
        form_data = request.POST
        sequence_keys = form_data.getlist('sequences_list')
        if 'view' in form_data:
            # To get the list of different sequences to view we will
            # create a new Alignment instance, whose name is the time
            # of creation
            alignment_for_comparison = fetchSequencesForComparison(sequence_keys)
            print(alignment_for_comparison)
            return render(request,'sequence/index.html', {'selected': sequence_keys, 'latest_list' : list_form, 'add' : add, 'view_alignment' : alignment_for_comparison})
        elif 'delete' in form_data:
            for key in sequence_keys:
                sequence = get_object_or_404(Sequence,pk=key)
                sequence.delete()
            return HttpResponseRedirect(reverse('sequence:index'),{'selected' : sequence_keys, 'latest_list' : list_form, 'form' : add, 'view_alignment' : False})
    return HttpResponseRedirect(reverse('sequence:index'),{'latest_list' : list_form, 'form' : add, 'view_alignment' : False})

def fetchSequencesForComparison(sequence_keys):
    class CustomException(Exception):
        pass
    algn = Alignment(alignment_name=str(timezone.now()))
    algn.save()
    sqType = None
    no_alignment= False
    for key in sequence_keys:
        try:
            print(key)
            print("{} seq_type".format(sqType))
            seq = get_object_or_404(Sequence,pk=key)
            print(seq)
            if sqType != None and sqType != seq.type_of_code:
                raise CustomException
            seq.alignment = algn
            sqType = seq.type_of_code
            seq.save()
        except CustomException:
            return False
    print("{} returning the alignment".format(algn))
    return Sequence.objects.filter(alignment=algn)
