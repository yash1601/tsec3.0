from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, AccountForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from subprocess import run,PIPE,Popen
from .models import *
import sys
import requests
from bs4 import BeautifulSoup

# #######################VIiew and end points#########################################################333

@login_required(login_url='login')
def index(request):
    jobs = Job.objects.all()
    email = request.user.email
    email=email.split('@')[0]
    context={
        'jobs':jobs,
        'email':email
    }
    return render(request,'index.html', context)



# #######################################Login and authenitication######################################################
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    account = Account.objects.get(user=user)
    allquestions=[]
    row = []
    all_article=[]
    row2=[]
    addedjobs = account.jobs.all()
    #print(addedjobs)
    for j in addedjobs:
        allquestions+= j.questions.all()
        all_article+=j.articles.all()
    
    #print(all_article)

    #allquestions = account.jobs.questions.all()
    solvedquestions = account.solved.all()
    x = len(solvedquestions)
    y = len(allquestions)
    y=y-x
    email = request.user.email
    email=email.split('@')[0]
    context ={
        'addedjobs':addedjobs,
        'allquestions':allquestions,
        'solvedquestions':solvedquestions,
        'all_article':all_article,
        'x':x,
        'y':y,
        'email':email,
    }
    return render(request,'dashboard.html', context)


def loginpage(request):
    Job.objects.all().delete()
    Article.objects.all().delete()
    Question.objects.all().delete()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            records=[]
            popular_company=['Google','Microsoft','Amazon']
            # print(popular_company)

            def get_url(position,location):
                template='https://in.indeed.com/jobs?q={}&l={}'
                url=template.format(position,location)
                return url

            def article_url(company):
                template_article='https://www.geeksforgeeks.org/tag/{}/'
                url_article=template_article.format(company)
                return url_article


            def get_record(card):
                atag=card.h2.a
                jobtitle=atag.get('title').strip()
                joburl='http://www.indeed.com'+atag.get('href')
                company=card.find('span','company').text.strip()
                joblocation=card.find('div','recJobLoc').get('data-rc-loc')
                summary=card.find('div','summary').text.strip()
                if(card.find('span','salaryText') is not None):
                    salary=card.find('span','salaryText').text.strip()
                else:
                    salary=''
                record=(jobtitle,company,joblocation,summary,salary,joburl)
                return record

            def getquestion_url(company):
                question_template='https://www.geeksforgeeks.org/{}-topics-interview-preparation/'
                question_url=question_template.format(company)
                return question_url

        ##############################Pushing Job Opportunities####################################################
            for company in popular_company:
                location=''
                url=get_url((company).replace(' ','+'),location)
                response=requests.get(url)
                soup=BeautifulSoup(response.text,'html.parser')
                cards=soup.find_all('div','jobsearch-SerpJobCard')
                records = []
                for card in cards:
                    record=get_record(card)
                    records.append(record)
        
                for k in records[:5]:
                    job=Job.objects.create(title=k[0], company=k[1],location=k[2] ,description=k[3],salary=k[4],url=k[5])
                    job.save()


        ##############################Pushing Articles####################################################
            #company='google'
            for company in popular_company:
                url_article=article_url(company)
                response=requests.get(url_article)
                soup=BeautifulSoup(response.text,'html.parser')
                divi=soup.find_all('div',{'class':'content'})
                articles=[]
                for i in divi:
                    try:
                        content=i.text.split('Read More')[0]
                        title=i.a.text
                        links=i.a['href']
                        text=content.replace(title,'')
                        article=(title,text,links)
                        articles.append(article)
                    except:
                        pass
                for k in articles[0:5]:
                    article=Article.objects.create(title=k[0], text=k[1],url=k[2])
                    article.save()
                    jobs=Job.objects.filter(company=company)
                    for j in jobs:
                        j.articles.add(article)
                        j.save()
            

        ##############################Pushing Questions####################################################
            for company in popular_company:
                url=getquestion_url(company)
                response=requests.get(url)
                soup=BeautifulSoup(response.text,'html.parser')
                divi=soup.find('div',{'class':'entry-content'})
                questions=[]
                for tag in divi.find_all('a'):
                    link=tag['href']
                    text=link.replace('http://www.geeksforgeeks.org/','').replace('/','')
                    question=(text,link)
                    questions.append(question)
                # print("***************************************************************************")
                # print(questions, company)
                # print("***************************************************************************")
                for i in range(3):
                    questions.pop(0)

                for k in questions[0:5]:
                    question1=Question.objects.create(title=k[0],url=k[1])
                    question1.save()
                    jobs=Job.objects.filter(company=company)

                    for j in jobs:
                        j.questions.add(question1)
                        j.save()


            return redirect('jobs')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


# #######################################Sign-Up###########################################
def register(request):
    form = CreateUserForm()
    form2 = AccountForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form2 = AccountForm(request.POST)
        if form.is_valid() and form2.is_valid():
            user = form.save()

            account = form2.save(commit=False)
            account.user = user

            account.save()
            messages.success(request, 'Registered successfully')
            return redirect('login')

    context = {'form': form,
               'form2': form2,
               }

    return render(request, 'register.html', context)

@login_required(login_url='login')
def addjob(request, pk):
    user = request.user
    account = Account.objects.get(user=user)
    job = Job.objects.get(id=pk)
    account.jobs.add(job)
    account.save()
    return redirect('dashboard')


@login_required(login_url='login')
def jobpage(request,pk):
    j = Job.objects.get(id=pk)
    allquestions = j.questions.all()
    user = request.user
    print(user)
    account = Account.objects.get(user=user)
    solved = account.solved.all()
    unsolved = []
    for i in allquestions:
        for j in solved:
            if j == i:
                break
        if j == i:
            continue
        unsolved.append(i)

    # email=request.user.email
    # email=email.split('@')[0]
    # print(email)
    email = request.user.email
    email=email.split('@')[0]
    context = {
        'unsolved':unsolved,
        'email':email,
    }

    return render(request, 'jobpage.html', context)

@login_required(login_url='login')
def solve(request, pk):
    user = request.user
    account = Account.objects.get(user=user)
    q = Question.objects.get(id=pk)
    account.solved.add(q)
    account.save()
    return redirect('dashboard')

@login_required(login_url='login')
def modalform(request):
    if request.POST:
        note = request.POST.get('note')
        print(note)
        return redirect('jobs')


@login_required(login_url='login')
def interviews(request):
    email = request.user.email
    email=email.split('@')[0]
    context={
        'email':email
    }
    return render(request,'interviews.html', context)