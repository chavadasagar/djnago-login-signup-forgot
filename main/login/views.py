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
    temail = request.POST.get('email')
    password = request.POST.get('password')

    alluser = user.objects.all()

    for u in alluser:
        if u.email == temail:
            return HttpResponse("This email is already found please try to login <a href='login'>login</a>")



    u = user(name=name, email=temail, password=password)
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

    request.session['email'] = email
    print(request.session['email'])
    

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
        print(otp)
        return redirect("getchangepassword")
    else:
        return HttpResponse("wrong password")


def getchangepassword(request):
    return render(request,'changepassword.html')

    
def changepassword(request):
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')


    if password1 != password2:
        return HttpResponse("password does not match")
    else:
        this_email = request.session['email']
        print(this_email)
        u = user.objects.get(email=this_email)

        u.password = password2
        u.save()
        del u
        del request.session['email']
        return redirect('login')


