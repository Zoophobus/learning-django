from django.db import models
from django.contrib import admin
import re
from django.utils import timezone

# Create your models here.

def json_default_value():
    return [[-1,-1]]

class Alignment(models.Model):
    object_creation_date = models.DateTimeField('Key as date-time field',default=timezone.now)
    alignment_name = models.CharField(max_length=20,unique=True,primary_key=True)

class Sequence(models.Model):
    DNA = 'DNA'
    RNA = 'RNA'
    AMINO = 'AMINO-ACID'
    type_of_code = models.CharField(
            max_length=10,
            choices=[
                (DNA,'DNA'),
                (RNA,'RNA'),
                (AMINO,'Amino-acid'),
                ],
            default=DNA,
            )
    REF = 'REFERENCE'
    READ = 'READ'
    type_of_sequence = models.CharField(
            max_length=11,
            choices=[
                (REF, 'REFERENCE'),
                (READ, 'READ'),
                ],
            default=READ,
            )
    sequence_name = models.CharField(max_length=20,unique=True,primary_key=True)
    sequence = models.TextField(max_length=1000)
    publication_date = models.DateTimeField('date published')
    coding_regions = models.JSONField(default=json_default_value)
    start_offset = models.IntegerField(verbose_name="Sequence offset from the reference")
    alignment = models.ForeignKey(Alignment,models.SET_NULL,blank=True,null=True)

    def name(self):
        return re.sub(r'_',' ', self.sequence_name.capitalize())
    def __str__(self):
        return re.sub(r'_',' ', self.sequence_name.capitalize())
    def correct_sequence(self):
        def is_amino_acid(aa):
            valid_aa={'Phe','Leu','Ser','Tyr','Stop','Cys','Trp','Pro','His','Gln','Arg','Ile','Met','Thr','Asn','Lys','Val','Ala','Asp','Glu','Gly'}
            if not aa in valid_aa:
                return False 
            return True 

        if self.type_of_code == 'DNA' and re.search(r'[^ACTGN-]',self.sequence):
            return False
        elif self.type_of_code == 'RNA' and re.search(r'[^ACUGN-]',self.sequence):
            return False
        elif self.type_of_code == 'AMINO-ACID':
            for aa in self.sequence.split(','):
                if not is_amino_acid(aa):
                    return False

        return True
        
