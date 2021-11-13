from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import *


def index(request):
    all_group = Charity.objects.annotate(total=Count('donor'))
    return render(request, "index.html", {'all_group': all_group})


def donors_list(request, myid):
    ch_types = Charity.objects.filter(id=myid).first()
    donor = Donor.objects.filter(chariti=ch_types)
    return render(request, "donors_list.html", {'donor': donor})


def donors_details(request, myid):
    details = Donor.objects.filter(id=myid)[0]
    return render(request, "donors_details.html", {'details': details})


def request_fund(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST['address']
        ch_type = request.POST['ch_type']
        date = request.POST['date']
        blood_requests = RequestFund.objects.create(name=name, email=email, phone=phone, state=state,
                                                    city=city, address=address,
                                                    chariti=Charity.objects.get(name=ch_type), date=date)
        msub = "You Fund Request Has been received"
        msg = "Dear " + name + ",\n.we will contact you if any donor finds your request.\n\nIf you have any questions please contact us at niharmarkana5@gmail.com.\n\nSincerely,"

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        blood_requests.save()
        send_mail(msub, msg, email_from, recipient_list)
        return render(request, "index.html")
    return render(request, "request_fund.html")


def see_all_request(request):
    requests = RequestFund.objects.all()
    return render(request, "see_all_request.html", {'requests': requests})


def become_donor(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST['address']
        gender = request.POST['gender']
        ch_type = request.POST['ch_type']
        date = request.POST['date']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')

        user = User.objects.create_user(
            username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        donors = Donor.objects.create(donor=user, phone=phone, state=state, city=city, address=address,
                                      gender=gender, chariti=Charity.objects.get(name=ch_type), date_of_birth=date,
                                      image=image)

        msub = "Thank you For Registering with Uthhaan Foundation"
        msg = "Dear " + username + ",\nThank you for registering with Uthhaan Foundation. We appreciate you and your willingness to help us make a difference with the goal of the Uthhaan Foundation. Because of your donation we were able to help our society.\n\nIf you have any questions please contact us at niharmarkana5@gmail.com.\n\nSincerely,"

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        user.save()
        donors.save()
        send_mail(msub, msg, email_from, recipient_list)
        return render(request, "index.html")
    return render(request, "become_donor.html")


def Login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/profile")
            else:
                thank = True
                return render(request, "login.html", {"thank": thank})
    return render(request, "login.html")


def Logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login')
def profile(request):
    donor_profile = Donor.objects.get(donor=request.user)
    return render(request, "profile.html", {'donor_profile': donor_profile})


@login_required(login_url='/login')
def edit_profile(request):
    donor_profile = Donor.objects.get(donor=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST['address']
        ch_type = request.POST['ch_type']

        donor_profile.donor.email = email
        donor_profile.phone = phone
        donor_profile.state = state
        donor_profile.city = city
        donor_profile.address = address
        donor_profile.ch_type = Charity.objects.get(name=ch_type)
        donor_profile.save()
        donor_profile.donor.save()

        try:
            image = request.FILES['image']
            donor_profile.image = image
            donor_profile.save()
        except:
            pass
        alert = True
        return render(request, "edit_profile.html", {'alert': alert})
    return render(request, "edit_profile.html", {'donor_profile': donor_profile})


@login_required(login_url='/login')
def change_status(request):
    donor_profile = Donor.objects.get(donor=request.user)
    if donor_profile.ready_to_donate:
        donor_profile.ready_to_donate = False
        donor_profile.save()
    else:
        donor_profile.ready_to_donate = True
        donor_profile.save()
    return redirect('/profile')


@login_required(login_url='/login')
def see_all_donations(request):
    requests = Donation_list.objects.all()
    req = User.objects.all()
    return render(request, "donation_list.html", {'requests': requests, 'req': req})


def add_donation(request):
    if request.method == "POST":
        name = request.POST['name']
        date = request.POST['date']
        amount = request.POST['amount']
        blood_group = request.POST['blood_group']
        state = request.POST['state']
        city = request.POST['city']
        donation_add = Donation_list.objects.create(name=name, date=date, amount=amount,
                                                    chariti=Charity.objects.get(name=blood_group),
                                                    state=state, city=city)
        donation_add.save()
        return render(request, "index.html")
    return render(request, "profile.html")


def make_donation(request):
    if request.method == "POST":
        name = request.POST['name']
        date = request.POST['date']
        amount = request.POST['amount']
        email = request.POST['email']
        ch_type = request.POST['ch_type']
        state = request.POST['state']
        city = request.POST['city']
        first_name = ""
        last_name = ""
        password = ""
        image = ""
        gender = ""
        phone = ""
        donation_add = Donation_list.objects.create(name=name, date=date, amount=amount, email=email,
                                                    chariti=Charity.objects.get(name=ch_type),
                                                    state=state, city=city)

        donation_add.save()
        msub = "Thank you for your support"
        msg = "Dear," + name + ",\n Thank you for your generous donation worth " + amount + " to Uthhaan Foundation.We are thrilled to have your support. Through your donation we have been able to accomplish our organization goal and continue working towards purpose of Uthhaan Foundation\n\nThank You"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(msub, msg, email_from, recipient_list)
        return render(request, "index.html")
    return render(request, "make_donation.html")


def forgotpwd(request):
    if request.method == "POST":
        form = forgotpwdForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            u = User.objects.get(email=email)
            msub = "Forgot Password"
            msg = "please Clcik on below link to reset your password. \n\n http://127.0.0.1:8000/reset_password/" + u.username
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(msub, msg, email_from, recipient_list)
            return HttpResponse("Please check your mail")
        else:
            context = {'form': form}
            messages.error(request, 'There is Error in your information...kindly refill the form')
            render(request, 'forgotpwd.html', context)
    form = forgotpwdForm()
    context = {'form': form}
    return render(request, 'forgotpwd.html', context)


def reset_password(request, username):
    if request.method == "POST":
        form = resetpwdForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
            msub = "Succesfully Reset Your Password"
            msg = "Your password has been changed"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [u.email, ]
            send_mail(msub, msg, email_from, recipient_list)
            return redirect("http://127.0.0.1:8000/login/")
        else:
            context = {'form': form}
            messages.error(request, 'There is Error in your information...kindly refill the form')
            render(request, 'resetpwdform.html', context)
    form = resetpwdForm()
    context = {'form': form}
    return render(request, 'resetpwdform.html', context)
