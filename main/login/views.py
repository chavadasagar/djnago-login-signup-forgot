from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import user
import random
import smtplib

# Create your views here.


def login(request):
    return render(request, 'index.html')


def signup(request):
    return render(request, 'signup.html')


def home(request):


    return render(request, 'home.html')


def saveUser(request):

    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    u = user(name=name, email=email, password=password)
    u.save()

    return redirect('login')

def forgot(request):
    return render(request,'forgot.html')

def sendMail(request):
    email = request.POST.get('email')

    global otp
    otp  = random.randint(1,10000)


    # enter email and password and turn on less secure app

    gmail = ''
    password = ""
    

    def sendMail(to,sub,msg):
        print(f"email to {to} send with subject is:{sub} and Message {msg}")
        s = smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(gmail,password)

        s.sendmail(gmail,to,f"subject: {sub}\n\n{msg}")
        s.quit()


    sendMail(email,"reset password",'Your One Time Password is '+str(otp))    



    return render(request,'otp.html',{'otp':otp})
    


def isvaliduser(request):

    if request.method == 'POST':
        try:
            this_email = request.POST.get('email')
            this_password = request.POST.get('password')
            user.objects.get(email=this_email, password=this_password)
            return redirect('home')
        except Exception as e:
            return HttpResponse('wrong email or password')
    

def checkotp(request):
    this_otp = request.POST.get("otp")

    if int(this_otp) == otp:
        return redirect("getchangepassword")
    else:
        return HttpResponse("wrong password")


def getchangepassword(request):
    return render(request,'changepassword.html')

    
def changepassword(request):
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    this_email = request.session['email']
    u = user.objects.get(email=this_email)

    u.password = password2

    u.save()

    del request.session['email']

    return redirect('login')


