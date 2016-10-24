from django.shortcuts import render
from django.views.generic import *
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse
#from django.core.urlresolvers import reverse_lazy
from climats.models import *
from entries.models import Entry, Expthru
from entries.forms import ExpthruForm
from django.contrib.auth.models import User
from django.conf import settings
from tlucidity.get_userobj import get_userobj
import csv
import datetime
import os


def timeadmin(request):
    return render(request, 'climats/timeadmin.html')


def Exported(request):
    now = datetime.datetime.now()
    sufix = now.strftime("%y%m%d%H%M%S")
    opath = settings.BASE_DIR + '/Exports/'
    comps = 0
    coss = ''
    tec = 0
    summary = ''
    usobj = get_userobj()
    who = usobj.username
    entlist = Expthru.objects.get(user = usobj).key_list
    ent_list = [int(x) for x in entlist.split(',') if x]
    for cos in Company.objects.all():
        output = opath+cos.code+"/"+cos.code + sufix
        cec=0      
        for key in ent_list:
            released = Entry.objects.get(id=key)
            if released.company == cos:
                if cec == 0:
                    ofile = open ( output, "w" )
                    ofile.write ("###\n")
                cec = cec + 1 
                tec = tec + 1 
                tk = released.who.code
                ofile.write ("TK="+tk+"\n")
                sd = released.work_date
                fd = sd.strftime("%m%d%y")
                ofile.write ("SD="+fd+"\n")
                cm = released.matter
                ofile.write ("CC="+cm+"\n")
                hr = released.hours
                ofile.write ("HR="+str(hr)+"\n")
                a1 = released.activity_code1
                if a1:
                    ofile.write ("A1="+a1.code+"\n")
                a2 = released.activity_code2
                if a2:
                    ofile.write ("A2="+a2.code+"\n")
#               ta = released.task_code
#               ofile.write ("TA="+tk+"\n")
                tx = released.narrative
                if tx:
                    ofile.write ("TX="+tx+"\n")
                ofile.write ("##\n")
                Entry.objects.filter(id=key).update(exported_date=now)
                Entry.objects.filter(id=key).update(exported=True)
                Entry.objects.filter(id=key).update(status='E')
        if cec > 0:
            ofile.close()
            comps = comps + 1
            if cos.code == 'CH':
                os.system('/usr/lib/send4ch')
            if cos.code == 'CO':
                os.system('/usr/lib/send4co')
            if cos.code == 'ST':
                os.system('/usr/lib/send4st')
            if cos.code == 'GM':
                os.system('/usr/lib/send4gm')
            if cos.code == 'GS':
                os.system('/usr/lib/send4gs')
            coss = coss + ' ' + cos.code + ' '
    if comps > 0:
        summary = str(tec)
        if tec == 1:
            summary = summary + ' entry was'
        else:
            summary = summary + ' entries were '
        summary = summary + 'exported for ' + coss
        return render(request, 'climats/exported.html', {'comps': comps, 'results': summary})
    else:
        return render(request, 'climats/exported.html', {'comps': comps, 'results': err_summy})


def Exportlist(request):
    if request.method == 'GET':
        elist = ''
        comps = 0
        summary = ''
        usobj = get_userobj()
        thru = Expthru.objects.get(user = usobj).thru_date
        for cos in Company.objects.all():
            centry = 0
            chour = 0
            for released in Entry.objects.filter(status='R', work_date__range=["1959-08-23", thru], company=cos):
                if elist == '':
                    elist = str(released.id)
                else:
                    elist = elist + ',' + str(released.id)
                centry = centry + 1
                chour = chour + released.hours
            if centry > 0:
                tcr = '{:<26}'.format(cos.name)
                tcr = tcr + '{:>6}'.format(centry) + '{:>10}'.format(chour)
                summary = summary + tcr + '\n'
                comps = comps + 1
        if comps > 0 :
            Expthru.objects.filter(user = usobj).update(key_list=elist)
            return render(request, 'climats/export_list.html', {'comps': comps, 'summy': summary, 'through':thru})
    return render(request, 'climats/export_list.html', {'comps': 0, 'through':thru})


class ExpthrView(CreateView):

    model = Expthru
    form_class = ExpthruForm
    template_name = 'climats/exports.html'

    def get_success_url(self):
        return reverse('export-list')


def updatevals(request):
    return render(request, 'climats/updatevals.html')


def updateval(request):
    current_results = ''
    vpath = settings.BASE_DIR + '/climats/val/'
    textfile = vpath + 'company.txt'
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

    textfile = vpath + 'tk.txt'
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

    textfile = vpath + 'client.txt'
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

    textfile = vpath + 'case.txt'
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

    textfile = vpath + 'activity.txt'
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
    
    textfile = vpath + 'task.txt'
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
    current_results += ' (GMT)'
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

