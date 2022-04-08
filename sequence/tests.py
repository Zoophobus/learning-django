from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.db.models.query import QuerySet

# required App classes
from .models import Sequence, Alignment
from .views import fetchSequencesForComparison

# Create your tests here.



class SequenceTests(TestCase):
    client = Client()
    def test_sequence_type_with_correct_sequence(self):
        self.assertIs(Sequence(type_of_code='DNA',sequence='ACGTAGAC'),True)
        self.assertIs(Sequence(type_of_code='RNA',sequence='ACGUAGAC'),True)
    def test_sequence_type_with_incorrect_sequence(self):
        self.assertIs(Sequence(type_of_code='DNA',sequence='ACGUAGAC'),False)
        self.assertIs(Sequence(type_of_code='RNA',sequence='ACGTAGAC'),False)
    def test_compare_dna_with_dna(self):
        dnA = Sequence(sequence_name='test_seq_1',type_of_code='DNA',sequence='ACTAC')
        dnB = Sequence(sequence_name='test_seq_2',type_of_code='DNA',sequence='ACTAT')
        sqLst = list(dnA.sequence_name,dnB.sequence_name) 
        outcome = fetchSequencesForComparison(sqLst)
        self.assertIsInstance(outcome,QuerySet)
    def test_compare_dna_with_rna(self):
        dnA = Sequence(sequence_name='test_seq_1',type_of_code='DNA',sequence='ACTAC')
        dnB = Sequence(sequence_name='test_seq_2',type_of_code='RNA',sequence='ACTAT')
        sqLst = list(dnA.sequence_name,dnB.sequence_name) 
        outcome = fetchSequencesForComparison(sqLst)
        self.assertFalse(outcome,QuerySet)

