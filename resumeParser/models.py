from django.db import models
from django import forms
from django.forms import ClearableFileInput

# Create your models here.
class Resume(models.Model):
    resume        = models.FileField('Upload Resumes', upload_to='resumes/')
    doctype       = models.CharField('Type', max_length=255, null=True, blank=True)
    name          = models.CharField('Name', max_length=255, null=True, blank=True)
    email         = models.CharField('Email', max_length=255, null=True, blank=True)
    mobile_number = models.CharField('Mobile Number',  max_length=255, null=True, blank=True)
    fonts         = models.CharField('Fonts', max_length=600, null=True, blank=True)
    linkedin      = models.CharField('LinkedInLink', max_length=255, null=True, blank=True)
    textCount     = models.CharField('textCount', max_length=600, null=True, blank=True)
    tableCount    = models.PositiveIntegerField('tableCount', null=True, blank=True)
    imgCount      = models.PositiveIntegerField('imgCount', null=True, blank=True)
    # education     = models.CharField('Education', max_length=255, null=True, blank=True)
    # skills        = models.CharField('Skills', max_length=1000, null=True, blank=True)
    # company_name  = models.CharField('Company Name', max_length=1000, null=True, blank=True)
    # college_name  = models.CharField('College Name', max_length=1000, null=True, blank=True)
    # designation   = models.CharField('Designation', max_length=1000, null=True, blank=True)
    # experience    = models.CharField('Experience', max_length=1000, null=True, blank=True)
    # uploaded_on   = models.DateTimeField('Uploaded On', auto_now_add=True)
    # total_experience  = models.CharField('Total Experience (in Years)', max_length=1000, null=True, blank=True)

class UploadResumeModelForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume']
        widgets = {
            'resume': ClearableFileInput(attrs={'multiple': True}),
        }