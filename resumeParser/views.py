# Create your views here.
from django.shortcuts import render, redirect
from pyresparser import ResumeParser
from .models import Resume, UploadResumeModelForm
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, FileResponse, Http404
import sqlite3
import os, sys
import csv
from .docxXmlParser import docxXmlParser
from .docxTextExtract import getText
from sqlite3 import Error
from django.conf import settings
from .pdfTextCount import textCount
from .pdfTableCount import pdfTableCount
from .xmlParser import xmlParser
from .pdfText import get_text_info

def homepage(request):
    if request.method == 'POST':
        # pass      
        # Resume.objects.all().delete()
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('resume')
        resumes_data = []
        if file_form.is_valid():
            for file in files:
                try:
                    # saving the file
                    resume = Resume(resume=file)

                    fileExtension = (str(file)).split(".")[-1]
                    if fileExtension != "pdf" and fileExtension != "doc" and fileExtension != "docx":
                        messages.warning(request, 'Please provide .pdf or .doc or .docx resume', '')
                        return redirect('homepage')
                    resume.save()
                    
                    filePath = os.path.join(settings.MEDIA_ROOT, resume.resume.name)
                    # extracting resume entities
                    parser = ResumeParser(os.path.join(filePath))
                    data = parser.get_extracted_data()
                    resumes_data.append(data)
                    resume.name               = data.get('name')
                    resume.doctype            = (str(file)).split(".")[-1]
                    resume.email              = data.get('email')
                    if resume.email is None:
                        resume.email = ''
                    # resume.mobile_number      = data.get('mobile_number')
                    # if data.get('degree') is not None:
                    #     resume.education      = ', '.join(data.get('degree'))
                    # else:
                    #     resume.education      = None
                    # resume.company_names      = data.get('company_names')
                    # resume.college_name       = data.get('college_name')
                    # resume.designation        = data.get('designation')
                    # resume.total_experience   = data.get('total_experience')
                    # if data.get('skills') is not None:
                    #     resume.skills         = ', '.join(data.get('skills'))
                    # else:
                    #     resume.skills         = None
                    # if data.get('experience') is not None:
                    #     resume.experience     = ', '.join(data.get('experience'))
                    # else:
                    #     resume.experience     = None
                    if resume.doctype == "pdf":
                        if sys.platform == 'linux':
                            cmd = "python3.8 " + settings.BASE_DIR + "/mypdf2txt.py -o r1.xml " + os.path.join(filePath)
                        elif sys.platform == 'win32':
                            cmd = "python " + settings.BASE_DIR + "/mypdf2txt.py -o r1.xml " + filePath
                        else:
                            messages.warning(request, 'Compatible with Linux and Windows only', '')
                            return redirect('homepage')
                        os.system(cmd)
                        fonts, imgCount = xmlParser('r1.xml')
                        resume.fonts = fonts
                        resume.imgCount = imgCount
                        resume.linkedin, resume.mobile_number = get_text_info(filePath)
                        # os.system('rm r1.xml')
                        resume.textCount = textCount(filePath)
                        resume.tableCount = pdfTableCount(filePath)
                    else:
                        resume.fonts, resume.tableCount, resume.imgCount = docxXmlParser(filePath)
                        resume.linkedin, resume.mobile_number = getText(filePath)
                    resume.save()
                except IntegrityError as e:
                    print(e)
                    messages.warning(request, 'Duplicate resume found:', file.name)
                    return redirect('homepage')
            resumes = Resume.objects.all()
            messages.success(request, 'Resumes uploaded!')
            context = {
                'resumes': resumes,
            }
            return render(request, 'base.html', context)
    else:
        form = UploadResumeModelForm()
    return render(request, 'base.html', {'form': form})

def exportCSV(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="databaseContent.csv"'
    try:
        # Connect to database
        conn = sqlite3.connect(settings.BASE_DIR+ '/db.sqlite3')

        cursor = conn.cursor()
        cursor.execute("SELECT * from resumeparser_resume")
        csv_writer = csv.writer(response, delimiter="\t")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

    except Error as e:
        print(e)

        # Close database connection
    finally:
        conn.close()
    
    return response