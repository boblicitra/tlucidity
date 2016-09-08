from django.shortcuts import render
from django.views.generic import *
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse
#from django.core.urlresolvers import reverse_lazy
from climats.models import *
from entries.models import Entry
from django.contrib.auth.models import User
import csv
import datetime


def timeadmin(request):
    return render(request, 'climats/timeadmin.html')


class ExportEntryView(ListView):
    model = Entry
    template_name = 'climats/export_list.html'


def updatevals(request):
    return render(request, 'climats/updatevals.html')


def updateval(request):
    current_results = ''
    textfile="static/val/company.txt"
    with open ( textfile, "r" ) as inputF:
        lines = csv.reader (inputF, delimiter="|")
        for nextCo in lines:
            fnum = 0
            for nextCol in nextCo:
                fnum = fnum + 1
                if fnum == 1:
                    f1 = nextCol
                if fnum == 2:
                    f2 = nextCol
            nextComp = Company (code=f1, name=f2)
            nextComp.save()

    textfile="static/val/tk.txt"
    with open ( textfile, "r" ) as inputF:
        lines = csv.reader (inputF, delimiter="|")
        rnum = 0
        for nextTk in lines:
            rnum += 1
            fnum = 0
            for nextCol in nextTk:
                fnum = fnum + 1
                if fnum == 1:
                    f1 = nextCol
                if fnum == 2:
                    f2 = nextCol
                if fnum == 3:
                    f3 = nextCol
                if fnum == 4:
                    f4 = nextCol
                if fnum == 5:
                    f5 = nextCol
                if fnum == 6:
                    f6 = nextCol
            nextTk = Timekeeper (code=f1, first_name=f2, middle_ini=f3, last_name=f4, full_name=f5, status=f6)
            nextTk.save()
            
        current_results += 'Processed '
        text_result1 = 'Processed '
        current_results += str(rnum)
        text_result1 += str(rnum)
        current_results += ' timekeeper records. \n'
        text_result1 += ' timekeeper records. '

    textfile="static/val/client.txt"
    with open ( textfile, "r" ) as inputF:
        lines = csv.reader (inputF, delimiter="|")
        rnum = 0
        for nextCl in lines:
            rnum += 1
            fnum = 0
            for nextCol in nextCl:
                fnum = fnum + 1
                if fnum == 1:
                    f1 = nextCol
                if fnum == 2:
                    f2 = nextCol
                if fnum == 3:
                    f3 = nextCol
                if fnum == 4:
                    f4 = nextCol
            cccc = f1+f2
            ddcc = f3+"("+f2+")"
            cfk = Company.objects.get(pk=f1)
            nextCl = Client (code=cccc, number=f2, name=f3, status=f4, company=cfk, client_list_name=ddcc)
            nextCl.save()
            
        current_results += 'Processed '
        text_result2 = 'Processed '
        current_results += str(rnum)
        text_result2 += str(rnum)
        current_results += ' client records. \n'
        text_result2 += ' client records. '

    textfile="static/val/case.txt"
    with open ( textfile, "r" ) as inputF:
        lines = csv.reader (inputF, delimiter="|")
        rnum = 0
        for nextCa in lines:
            rnum += 1
            fnum = 0
            for nextCol in nextCa:
                fnum = fnum + 1
                if fnum == 1:
                    f1 = nextCol
                if fnum == 2:
                    f2 = nextCol
                if fnum == 3:
                    f3 = nextCol
                if fnum == 4:
                    f4 = nextCol
                if fnum == 5:
                    f5 = nextCol
                if fnum == 6:
                    f6 = nextCol
            cccc = f1+f2+f3
            ddcc = f5+"("+f3+")"
            cfk = Company.objects.get(pk=f1)
            clfk = Client.objects.get(pk=f1+f2)
            nextCa = Case (code=cccc, matter_id=f4, number=f3, name=f5, status=f6, client=clfk, company=cfk, case_list_name=ddcc)
            nextCa.save()
            
        current_results += 'Processed '
        text_result3 = 'Processed '
        current_results += str(rnum)
        text_result3 += str(rnum)
        current_results += ' matter records. \n'
        text_result3 += ' matter records. '

    textfile="static/val/activity.txt"
    with open ( textfile, "r" ) as inputF:
        lines = csv.reader (inputF, delimiter="|")
        rnum = 0
        for nextAc in lines:
            fnum = 0
            for nextCol in nextAc:
                fnum = fnum + 1
                if fnum == 1:
                    f1 = nextCol
                if fnum == 2:
                    f2 = nextCol
                if fnum == 3:
                    f3 = nextCol
            cccc = f1+f2
            nextAc = Activity (code=f2, description=f3)
            if f1 == "CH":
                nextAc.save()
            if f1 == "CH":
                rnum += 1
            
        current_results += 'Processed '
        text_result4 = 'Processed '
        current_results += str(rnum)
        text_result4 += str(rnum)
        current_results += ' activity code records. \n'
        text_result4 += ' activity code records. '
    
    textfile="static/val/task.txt"
    with open ( textfile, "r" ) as inputF:
        lines = csv.reader (inputF, delimiter="|")
        for nextTa in lines:
            fnum = 0
            for nextCol in nextTa:
                fnum = fnum + 1
                if fnum == 1:
                    f1 = nextCol
                if fnum == 2:
                    f2 = nextCol
                if fnum == 3:
                    f3 = nextCol
            cccc = f1+f2
            nextTa = Task (set_code_code=cccc, set_code=f1, code=f2, description=f3,)
            nextTa.save()

    datime = datetime.datetime.now()                              
    time4results = datime.strftime("%A, %d %B %Y %I:%M%p")       
    current_results += 'Completed successfully on '
    current_results += time4results 
    name4log = request.user.username
    log_entry = Import_Log (ran_by=name4log, results=current_results)
    log_entry.save()

    return render(request, 'climats/updateval.html',
        {'import_stage': 4,
         'end_text1': text_result1,
         'end_text2': text_result2,
         'end_text3': text_result3,
         'end_text4': text_result4
        })

