import random
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from MyApp.models import *


def login_get(request):
    return render(request,'login.html')
def adm_login_post(request):
    username=request.POST["username"]
    password = request.POST["password"]

    log=authenticate(username=username,password=password)
    if log is not None:
        login(request,log)
        if log.groups.filter(name='Admin'):
            return redirect('/MyApp/adm_home/')
        elif log.groups.filter(name='Expert'):
           return redirect('/MyApp/expert_home/')
        else:
            return redirect('/MyApp/login_get/')
    else:
        return redirect('/MyApp/login_get/')
#/
# k=User.objects.get(username="muhammedshamilem@gmail.com")
# k.set_password("1234")
# k.save()

@login_required(login_url="/MyApp/login_get/")
def adm_changepassword(request):
    return render(request,'admin/change password.html')
def adm_changepassword_post(request):
    currentpassword=request.POST["currentpassword"]
    newpassword = request.POST["newpassword"]
    confirmpassword = request.POST["confirmpassword"]
    user=request.user
    if not user.check_password(currentpassword):
        messages.error(request,'Invalid Password' )
        return redirect('/MyApp/adm_changepassword/')
    elif (newpassword==confirmpassword):
        user.set_password(confirmpassword)
        user.save()
        return redirect('/MyApp/login_get/')
    else:
        messages.error(request, 'Invalid Password')
        return redirect('/MyApp/adm_changepassword/')






def log_out(request):
    logout(request)
    return redirect('/MyApp/login_get/')

@login_required(login_url="/MyApp/login_get/")
def adm_viewuser(request):

        data = Users.objects.all()
        return render(request, "admin/viewuser.html", {'data': data})

@login_required(login_url="/MyApp/login_get/")
def adm_addexpert(request):
    return render(request,"admin/Add expert.html")

@login_required(login_url="/MyApp/login_get/")
def adm_addexpert_post(request):
    name= request.POST["name"]

    email= request.POST["email"]
    phonenumber= request.POST["phonenumber"]
    place= request.POST["place"]
    post = request.POST["post"]

    pincode = request.POST["pincode"]
    qualificqtion = request.POST["qualification"]
    experience = request.POST["experience"]
    photo = request.FILES["photo"]

    password=1234

    if User.objects.filter(username=email).exists():
        messages.warning(request,'user already exist')
        return redirect('/MyApp/adm_viewexpert/')

    user=User.objects.create_user(username=email,password=password)
    user.groups.add(Group.objects.get(name='Expert'))


    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,photo)
    path=fs.url(date)


    a=Expert()
    a.name=name

    a.emailid=email
    a.phonenumber=phonenumber
    a.place=place

    a.post=post
    a.pincode=pincode
    a.photo=path
    a.qualification=qualificqtion
    a.experience=experience
    a.USER=user
    a.save()

    return redirect( '/MyApp/adm_viewexpert/')


@login_required(login_url="/MyApp/login_get/")
def adm_appreview(request):
    v=Review.objects.all()
    return render(request,"admin/app review.html",{'data':v})


@login_required(login_url="/MyApp/login_get/")
def adm_editexpert(request,id):
    data=Expert.objects.get(id=id)
    return render(request,"admin/edit expert.html",{'data':data})
def adm_editexpert_post(request):
    name = request.POST["name"]

    email = request.POST["email"]
    phonenumber = request.POST["phonenumber"]
    place = request.POST["place"]
    post = request.POST["post"]

    pincode = request.POST["pincode"]
    qualificqtion = request.POST["qualification"]
    experience = request.POST["experience"]
    id = request.POST["id"]
    a = Expert.objects.get(id=id)
    if 'photo' in request.FILES:

        photo = request.FILES["photo"]
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(date, photo)
        path = fs.url(date)
        a.photo = path
        a.save()






    a.name = name

    a.emailid = email
    a.phonenumber = phonenumber
    a.place = place

    a.post = post
    a.pincode = pincode

    a.qualification = qualificqtion
    a.experience = experience

    a.save()

    return redirect('/MyApp/adm_viewexpert/')

@login_required(login_url="/MyApp/login_get/")
def adm_sentreply(request,id):
    return render(request,"admin/Sent Reply.html",{'id':id})
def adm_sentreply_post(request):
    id=request.POST["id"]
    reply=request.POST["reply"]

    Complaints.objects.filter(id=id).update(reply=reply,status="Replied")
    return redirect('/MyApp/adm_viewcomplaint/#a')

@login_required(login_url="/MyApp/login_get/")
def adm_viewcomplaint(request):
    v=Complaints.objects.all()
    return render(request,"admin/viewcomplaint.html",{'data':v})

@login_required(login_url="/MyApp/login_get/")
def adm_viewexpert(request):
    v=Expert.objects.all()
    return render(request,"admin/viewExpert.html",{'data':v})
def adm_deleteexpert(request,id):
    Expert.objects.filter(id=id).delete()
    return redirect('/MyApp/adm_viewexpert/')
@login_required(login_url="/MyApp/login_get/")
def adm_home(request):
    return render(request,"admin/home_index.html")

@login_required(login_url="/MyApp/login_get/")
def expert_addvideo(request):
    return render(request,"expert/Add Video.html")
def expert_addvideo_post(request):
    title =request.POST["title"]
    video = request.FILES["video"]

    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d%H%M%S') + '.mp4'
    fs.save(date,video)
    path = fs.url(date)

    v=Video()
    v.title=title
    v.video=path
    v.date=datetime.now().today()
    v.EXPERT=Expert.objects.get(USER_id=request.user)
    v.save()

    return redirect('/MyApp/expert_viewvideo/')
@login_required(login_url="/MyApp/login_get/")
def expert_editvideo(request,id):
    data=Video.objects.get(id=id)
    return render(request,"expert/Edit Video.html",{'data':data})
def expert_editvideo_post(request):
    title=request.POST["title"]


    id=request.POST['id']

    v= Video.objects.get(id=id)
    if 'video' in request.FILES:
        video = request.POST["video"]
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.mp4'
        fs.save(date, video)
        path = fs.url(date)
        v.video = path
        v.save()
    v.title = title

    v.date = datetime.now().today()
    v.EXPERT = Expert.objects.get(USER_id=request.user)
    v.save()


    return redirect('/MyApp/expert_viewvideo')
@login_required(login_url="/MyApp/login_get/")
def expert_deletevideo(request,id):
    Video.objects.filter(id=id).delete()
    return redirect('/MyApp/expert_viewvideo/')

@login_required(login_url="/MyApp/login_get/")
def expert_viewprofile(request):
    d=request.user
    data=Expert.objects.get(USER=d)
    return render(request,"expert/View Profile.html",{'data':data})
@login_required(login_url="/MyApp/login_get/")
def expert_viewvideo(request):
    data=Video.objects.all()
    return render(request,"expert/View Video.html",{'data':data})
@login_required(login_url="/MyApp/login_get/")
def expert_viewuser(request):
    data=Users.objects.all()
    return render(request,"expert/viewuser.html",{'data':data})
@login_required(login_url="/MyApp/login_get/")
def expert_home(request):
    return render(request,"expert/home_index.html")

@login_required(login_url="/MyApp/login_get/")
def expert_ViewRequest(requestt):
    data=request.objects.filter(EXPERT__USER_id=requestt.user.id,Status='pending')
    print(data,"ppppppppppppppp")
    return render(requestt,"expert/viewrequest.html",{'data':data})
@login_required(login_url="/MyApp/login_get/")
def expert_ViewApprovedRequest(requestt):
    data=request.objects.filter(EXPERT__USER_id=requestt.user.id,Status='Approved')
    print(data,"ppppppppppppppp")
    return render(requestt,"expert/view Approved request.html",{'data':data})
@login_required(login_url="/MyApp/login_get/")
def expert_ViewRejectedRequest(requestt):
    data=request.objects.filter(EXPERT__USER_id=requestt.user.id,Status='Rejected')
    print(data,"ppppppppppppppp")
    return render(requestt,"expert/view Rejected request.html",{'data':data})


@login_required(login_url="/MyApp/login_get/")
def expert_ApproveRequest(requestt,id):
    request.objects.filter(id=id).update(Status="approved")
    return redirect('/MyApp/expert_ViewRequest/')
@login_required(login_url="/MyApp/login_get/")
def expert_RejectRequest(requestt,id):
    request.objects.filter(id=id).update(Status="rejected")
    return redirect('/MyApp/expert_ViewRequest/')


@login_required(login_url="/MyApp/login_get/")
def expert_changepassword(request):
    return render(request,'expert/change password.html')
def expert_changepassword_post(request):
    currentpassword=request.POST["currentpassword"]
    newpassword = request.POST["newpassword"]
    confirmpassword = request.POST["confirmpassword"]
    user=request.user
    if not user.check_password(currentpassword):
        messages.error(request,'Invalid Password' )
        return redirect('/MyApp/expert_changepassword/')
    elif (newpassword==confirmpassword):
        user.set_password(confirmpassword)
        user.save()
        return redirect('/MyApp/login_get/')
    else:
        messages.error(request, 'Invalid Password')
        return redirect('/MyApp/expert_changepassword/')




# user


def user_singup(request):
    name=request.POST['name']
    emailid = request.POST['emailid']
    phonenumber = request.POST['phonenumber']
    place = request.POST['place']
    pincode = request.POST['pincode']
    post = request.POST['post']
    photo = request.FILES['photo']
    password=request.POST['password']


    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,photo)
    path=fs.url(date)

    a=User.objects.create_user(username=emailid,password=password)
    a.groups.add(Group.objects.get(name='User'))
    a.save()

    obj=Users()
    obj.name=name
    obj.emailid=emailid
    obj.phonenumber=phonenumber
    obj.place=place
    obj.pincode=pincode
    obj.post=post
    obj.photo=path
    obj.USER=a
    obj.save()
    return JsonResponse({'status':'ok'})

def user_login(request):
    username=request.POST['username']
    password=request.POST['password']

    if not username or not password:
        return JsonResponse({'status':'no'})

    check=authenticate(request,username=username,password=password)
    if check is not None :
        login(request,check)
        if check.groups.filter(name='User').exists():
            return JsonResponse({'status':'ok','lid':check.id})
        elif check.groups.filter(name='Expert').exists():
            return JsonResponse({'status':'ok','lid':check.id})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})

def user_changepassword_post(request):
    currentpassword=request.POST["currentpassword"]
    newpassword = request.POST["newpassword"]
    confirmpassword = request.POST["confirmpassword"]
    lid = request.POST["lid"]

    user=User.objects.get(id=lid)
    if not user.check_password(currentpassword):
        return JsonResponse({'status': 'no'})
    elif (newpassword==confirmpassword):
        user.set_password(confirmpassword)
        user.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'no'})

def user_view_profile(request):
    lid = request.POST["lid"]
    data=  Users.objects.get(USER=lid)
    return JsonResponse({
        'status': 'ok',
        'name':data.name,
        'emailid':data.emailid,
        'phonenumber':data.phonenumber,
        'place':data.place,
        'pincode': data.pincode,
        'post': data.post,
        'photo': data.photo,
    })

def user_editprofile(request):
    lid = request.POST["lid"]
    name = request.POST['name']
    emailid = request.POST['emailid']
    phonenumber = request.POST['phonenumber']
    place = request.POST['place']
    pincode = request.POST['pincode']
    post = request.POST['post']

    data=Users.objects.get(USER=lid)
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(date, photo)
        path = fs.url(date)
        data.photo = path
        data.save()


    data.name = name
    data.emailid = emailid
    data.phonenumber = phonenumber
    data.place = place
    data.pincode = pincode
    data.post = post
    data.save()
    return JsonResponse({'status': 'ok'})



def user_sendcomplaint(request):
    lid = request.POST["lid"]
    complaint = request.POST['complaint']

    data = Complaints()
    data.date = datetime.now().today()
    data.complaint = complaint
    data.status = 'pending'
    data.reply = 'pending'
    data.USER = Users.objects.get(USER=lid)
    data.save()

    return JsonResponse({'status': 'ok'})


def user_viewreply(request):
    lid=request.POST['lid']
    data = Complaints.objects.filter(USER__USER_id=lid)
    l = []
    for i in data:
        l.append({
            'date': i.date,
            'complaint': i.complaint,
            'status': i.status,
            'reply': i.reply,


        })

    # print(l)
    return JsonResponse({'status': 'ok','data':l})
def user_ViewRequestStatus(requestt):
    lid=requestt.POST['lid']
    data = request.objects.filter(CUSTOMER__USER_id=lid)
    l = []
    for i in data:
        l.append({
            'id': i.id,
            'date': i.date,
            'expertname': i.EXPERT.name,
            'status': i.Status,
            'phonenumber': i.EXPERT.phonenumber,
            'expertemail': i.EXPERT.emailid,


        })

    # print(l)
    return JsonResponse({'status': 'ok','data':l})


def user_sendreview(request):
    lid = request.POST["lid"]
    review = request.POST['review']
    rating = request.POST['rating']

    data = Review()
    data.CUSTOMER = Users.objects.get(USER=lid)
    data.date = datetime.now().today()
    data.review = review
    data.rating = rating
    data.save()
    return JsonResponse({'status': 'ok'})


def user_viewexpert(requesta):
    lid=requesta.POST["lid"]

    data = Expert.objects.all()
    l=[]
    for i in data:
        if request.objects.filter(EXPERT_id=i.id,CUSTOMER__USER_id=lid).exists():
            l.append({
                'id':i.id,
                'name':i.name,
                'emailid':i.emailid,
                'phonenumber':i.phonenumber,
                'place':i.place,
                'pincode':i.pincode,
                'post':i.post,
                'photo':i.photo,
                'qualification':i.qualification,
                'experience':i.experience,
                'rsts':'yes'

            })
        else:
            l.append({
                'id': i.id,
                'name': i.name,
                'emailid': i.emailid,
                'phonenumber': i.phonenumber,
                'place': i.place,
                'pincode': i.pincode,
                'post': i.post,
                'photo': i.photo,
                'qualification': i.qualification,
                'experience': i.experience,
                'rsts': 'no'

            })

    return JsonResponse({'status': 'ok','data':l})



def user_viewvideo(request):

    data = Video.objects.all()
    l = []
    for i in data:
        l.append({
            'title': i.title,
            'date': i.date,
            'EXPERT': i.EXPERT.name,
            'video': i.video,


        })

    print(l)
    return JsonResponse({'status': 'ok','data':l})


def user_viewlogs(request):
    lid=request.POST['lid']

    data = Logs.objects.filter(CUSTOMER__USER_id=lid)
    l = []
    for i in data:
        l.append({
            'date': i.date,
            'time': i.time,
            'ipaddress': i.ipaddress,
            'result': i.result,

        })

    print(l)
    return JsonResponse({'status': 'ok','data':l})


def send_request(requesta):
    lid=requesta.POST['lid']
    eid=requesta.POST['eid']

    a=request()
    a.CUSTOMER=Users.objects.get(USER_id=lid)
    a.EXPERT_id=eid
    a.date=datetime.now().today()
    a.Status='pending'
    a.save()



    return JsonResponse({'status': 'ok'})


def web_forgetpassword(request):
    return render(request,"forgetpassword.html")


def forgotpassword_post(request):


    email=request.POST['email']

    if User.objects.filter(email=email).exists():

        import random
        new_pass = random.randint(00000, 99999)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("idpsvirus@gmail.com", "niqh jjtu vgmh smwh")  # App Password
        to = email
        subject = "Test Email"
        body = "Your new password is " + str(new_pass)
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("s@gmail.com", to, msg)  # Disconnect from the server
        server.quit()

        user = User.objects.get(username=email)
        user.set_password(str(new_pass))
        user.save()

        return redirect('/MyApp/login_get/')
    else:
        messages.warning(request, 'email not  exists')
        return redirect('/MyApp/forgot_password/')



def android_forget_password_post(request):
    email = request.POST.get('email')
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email is required'})

    try:
        user = User.objects.get(username=email)
        print(email)

        # Generate new password
        new_pass = str(random.randint(1000, 9999))
        user.password = make_password(str(new_pass))
        user.save()

        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "idpsvirus@gmail.com"
        app_password = "niqh jjtu vgmh smwh"

        subject = "Your New Password"
        body = f"Your new password is: {new_pass}"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)
        server.quit()

        return JsonResponse({'status': 'ok', 'message': 'Password sent to your email'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Email send error: {str(e)}'})