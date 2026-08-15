from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)

from .models import (
    Donor,
    Volunteer,
    Donation,
    DonationArea,
    Gallery,
    ContactMessage,
)

from .forms import (
    UserCreationForm,
    DonorSignupForm,
    UserForm,
    VolunteerSignupForm,
    LoginForm,
    MyPasswordChangeForm,
    DonationNowForm,
    DonationAreaForm,
)




# Create your views here.
def index(request):
    return render(request, "app/index.html")
def about(request):
    return render(request,"app/about.html")
def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        try:

            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
            )

            messages.success(
                request,
                "Your message has been sent successfully. "
                "We will get back to you soon."
            )

            return redirect("contact")

        except Exception as e:

            print("CONTACT MESSAGE ERROR:", e)

            messages.error(
                request,
                "Sorry, your message could not be sent."
            )

    return render(request, "app/contact.html")


def gallery(request):
    gallery = Gallery.objects.all()
    return render(request, "app/gallery.html", {
        "gallery": gallery
    })

class login_admin(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "app/login-admin.html", {"form": form})

    def post(self, request):
        form = LoginForm(request=request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user.is_staff:
                login(request, user)
                messages.success(request, "Admin Login Successful.")
                return redirect("index_admin")
            else:
                messages.error(request, "You are not authorized as an admin.")

        return render(request, "app/login-admin.html", {"form": form})
    


class login_donor(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "app/login-donor.html", {"form": form})

    def post(self, request):
        form = LoginForm(request=request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if Donor.objects.filter(user=user).exists():
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect("index_donor")
            else:
                messages.error(request, "This account is not registered as a donor.")

        return render(request, "app/login-donor.html", {"form": form})

class login_volunteer(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "app/login-volunteer.html", {"form": form})

    def post(self, request):
        form = LoginForm(request=request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if Volunteer.objects.filter(user=user).exists():
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect("index_volunteer")
            else:
                messages.error(request, "This account is not registered as a Volunter.")

        return render(request, "app/login-volunteer.html", {"form": form})
  


class signup_donor(View):

    def get(self, request):
        form1 = UserForm()
        form2 = DonorSignupForm()
        return render(request, "app/signup_donor.html", {
            "form1": form1,
            "form2": form2,
        })

    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = DonorSignupForm(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            try:
                user = User.objects.create_user(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1']
                )

                Donor.objects.create(
                    user=user,
                    contact=request.POST['contact'],
                    userpic=request.FILES.get('userpic'),
                    address=request.POST['address']
                )

                messages.success(request, "Congratulations!! Donor Profile Created Successfully")

            except Exception as e:
                print("Exception:", e)
                messages.error(request, str(e))

        return render(request, "app/signup_donor.html", {
            "form1": form1,
            "form2": form2,
        })
    
class signup_volunteer(View):

    def get(self, request):
        form1 = UserForm()
        form2 = VolunteerSignupForm()
        return render(request, "app/signup_volunteer.html", {
            "form1": form1,
            "form2": form2,
        })

    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = VolunteerSignupForm(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            try:
                user = User.objects.create_user(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1']
                )

                Volunteer.objects.create(
                    user=user,
                    contact=request.POST['contact'],
                    address=request.POST['address'],
                    userpic=request.FILES.get('userpic'),
                    idpic=request.FILES.get('idpic'),
                    aboutme=request.POST['aboutme'],
                    status='Pending'
                )

                messages.success(
                    request,
                    "Congratulations!! Volunteer Profile Created Successfully."
                )
                return redirect("login_volunteer")

            except Exception as e:
                print(e)
                messages.error(request, str(e))

        return render(request, "app/signup_volunteer.html", {
            "form1": form1,
            "form2": form2,
        })


def index_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')

    totaldonations = Donation.objects.count()
    totaldonors = Donor.objects.count()
    totalvolunteers = Volunteer.objects.count()

    totalpendingdonations = Donation.objects.filter(
        status='Pending'
    ).count()

    totalaccepteddonations = Donation.objects.filter(
        status='Accepted'
    ).count()

    totaldelivereddonations = Donation.objects.filter(
        status='Donation Delivered Successfully'
    ).count()

    totaldonationareas = DonationArea.objects.count()

    context = {
        'totaldonations': totaldonations,
        'totaldonors': totaldonors,
        'totalvolunteers': totalvolunteers,
        'totalpendingdonations': totalpendingdonations,
        'totalaccepteddonations': totalaccepteddonations,
        'totaldelivereddonations': totaldelivereddonations,
        'totaldonationareas': totaldonationareas,
    }

    return render(request, "app/index-admin.html", context)


# admin dashboard
def pending_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Pending')
    return render(request, "app/pending-donation.html", locals())


def accepted_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Accepted')
    return render(request, "app/accepted-donation.html", locals())


def rejected_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Reject')
    return render(request, "app/rejected-donation.html", locals())


def volunteerallocated_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Volunteer Allocated')
    return render(request, "app/volunteerallocated-donation.html", locals())


def donationrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Donation Received')
    return render(request, "app/donationrec-admin.html", locals())


def donationnotrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Donation not Received')
    return render(request, "app/donationnotrec-admin.html", locals())


def donationdelivered_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.filter(status='Donation Delivered Successfully')
    return render(request, "app/donationdelivered-admin.html", locals())


def all_donations(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation = Donation.objects.all()
    return render(request, "app/all-donations.html", locals())
def delete_donation(request, pid):
    donation = get_object_or_404(Donation, id=pid)
    donation.delete()
    return redirect('all_donations')

def manage_donor(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')

    donor = Donor.objects.all()

    return render(request, "app/manage-donor.html", {
        "donor": donor
    })

def new_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.filter(status='Pending')
    
    return render(request, "app/new-volunteer.html", locals())


def accepted_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.filter(status='Accept')
    return render(request, "app/accepted-volunteer.html", locals())


def rejected_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.filter(status='Reject')
    return render(request, "app/rejected-volunteer.html", locals())


def all_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer = Volunteer.objects.all()
    return render(request, "app/all-volunteer.html", locals())

def delete_volunteer(request, pid):
    volunteer = get_object_or_404(Volunteer, id=pid)
    volunteer.user.delete()
    return redirect('all_volunteer')


class add_area(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login-admin')

        form = DonationAreaForm()

        return render(request, "app/add-area.html", {
            "form": form
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login-admin')

        form = DonationAreaForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Area Added Successfully"
            )

            return redirect("add_area")

        return render(request, "app/add-area.html", {
            "form": form
        })


class edit_area(View):
    def get(self, request, pid):
        form = DonationAreaForm()
        area = DonationArea.objects.get(id=pid)
        return render(request, "app/edit-area.html", locals())
    def post(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        form = DonationAreaForm(request.POST)
        area = DonationArea.objects.get(id=pid)
        areaname = request.POST['areaname']
        description = request.POST['description']
        area.areaname = areaname
        area.description = description
        try:
            area.save()
            messages.success(request, 'Area Updated Successfully')
            return redirect('manage_area')
        except:
            messages.warning(request, 'Area Not Updated')
            return render(request, 'edit-area.html')


def manage_area(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')

    area = DonationArea.objects.all()
    return render(request, "app/manage-area.html", {"area": area})

def delete_area(request, pid):
    area = get_object_or_404(DonationArea, id=pid)
    area.delete()
    return redirect('manage_area')


class changepwd_admin(View):

    def get(self, request):
        form = MyPasswordChangeForm(request.user)
        return render(request, 'app/changepwd-admin.html', {'form': form})

    def post(self, request):
        form = MyPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully.")
            return redirect("changepwd_admin")

        messages.error(request, "Please correct the errors below.")

        return render(request, 'app/changepwd-admin.html', {'form': form})
    


def logout(request):
   
    return redirect("index")


# admin view details
class accepted_donationdetail(View):

    def get(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')

        donation = Donation.objects.get(id=pid)
        donationarea = DonationArea.objects.all()
        volunteer = Volunteer.objects.filter(status='Accept')

        return render(request, "app/accepted-donationdetail.html", {
            "donation": donation,
            "donationarea": donationarea,
            "volunteer": volunteer,
        })

    def post(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')

        donation = Donation.objects.get(id=pid)

        donationareaid = request.POST.get("donationareaid")
        volunteerid = request.POST.get("volunteerid")
        adminremark = request.POST.get("adminremark")

      

        try:
            da = DonationArea.objects.get(id=donationareaid)
            v = Volunteer.objects.get(id=volunteerid)

            donation.donationarea = da
            donation.volunteer = v
            donation.adminremark = adminremark
            donation.status = "Volunteer Allocated"
            donation.volunteerremark = "Not Updated Yet"
            donation.updationdate = date.today()
            donation.save()

      

            messages.success(request, "Volunteer Allocated Successfully")

        except Exception as e:
            print("ERROR:", e)
            messages.warning(request, "Failed to Allocate Volunteer")

        return redirect("accepted_donation")
        
def delete_donor(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('manage_donor')

# =========================================================
# CONTACT MESSAGE MANAGEMENT
# =========================================================

def contact_messages(request):

    if not request.user.is_authenticated:
        return redirect('/login-admin')

    if not request.user.is_staff:
        return redirect('/login-admin')

    contactmessage = ContactMessage.objects.all().order_by('-created_at')

    return render(
        request,
        "app/contact-messages.html",
        {
            "contactmessage": contactmessage
        }
    )
class contact_message_detail(View):

    def get(self, request, pid):

        if not request.user.is_authenticated:
            return redirect('/login-admin')

        if not request.user.is_staff:
            return redirect('/login-admin')

        contactmessage = get_object_or_404(
            ContactMessage,
            id=pid
        )

        # Mark message as read
        contactmessage.is_read = True
        contactmessage.save()

        return render(
            request,
            "app/contact-message-detail.html",
            {
                "contactmessage": contactmessage
            }
        )

    def post(self, request, pid):

        if not request.user.is_authenticated:
            return redirect('/login-admin')

        if not request.user.is_staff:
            return redirect('/login-admin')

        contactmessage = get_object_or_404(
            ContactMessage,
            id=pid
        )

        reply_message = request.POST.get("reply_message")

        if not reply_message:

            messages.error(
                request,
                "Please write a reply before sending."
            )

            return redirect(
                "contact_message_detail",
                pid=contactmessage.id
            )

        try:

            email = EmailMessage(
                subject="Re: " + contactmessage.subject,

                body=reply_message,

                from_email=settings.DEFAULT_FROM_EMAIL,

                to=[contactmessage.email],
            )

            email.send(fail_silently=False)

            contactmessage.reply_message = reply_message
            contactmessage.is_replied = True
            contactmessage.is_read = True
            contactmessage.replied_at = timezone.now()

            contactmessage.save()

            messages.success(
                request,
                "Reply sent successfully."
            )

        except Exception as e:

            print("REPLY EMAIL ERROR:", e)

            messages.error(
                request,
                "The reply could not be sent. "
                "Please check your email settings."
            )

        return redirect(
            "contact_message_detail",
            pid=contactmessage.id
        )

# donor dashboard
def index_donor(request):

    donor = Donor.objects.get(user=request.user)

    donationcount = Donation.objects.filter(
        donor=donor
    ).count()

    acceptedcount = Donation.objects.filter(
        donor=donor,
        status="Accepted"
    ).count()

    rejectedcount = Donation.objects.filter(
        donor=donor,
        status="Reject"
    ).count()

    pendingcount = Donation.objects.filter(
        donor=donor,
        status="Pending"
    ).count()

    deliveredcount = Donation.objects.filter(
        donor=donor,
        status="Donation Delivered Successfully"
    ).count()

    return render(
        request,
        "app/index-donor.html",
        {
            "donationcount": donationcount,
            "acceptedcount": acceptedcount,
            "rejectedcount": rejectedcount,
            "pendingcount": pendingcount,
            "deliveredcount": deliveredcount,
        }
    )
    


class donate_now(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('/login-donor')

        form = DonationNowForm()

        return render(request, 'app/donate-now.html', {
            'form': form
        })

    def post(self, request):

        if not request.user.is_authenticated:
            return redirect('/login-donor')

        form = DonationNowForm(request.POST, request.FILES)

        if form.is_valid():

            donation = form.save(commit=False)

            donation.donor = Donor.objects.get(user=request.user)

            donation.status = "Pending"

            donation.save()

            messages.success(request, "Donation submitted successfully.")

            return redirect('/donate-now')

        return render(request, 'app/donate-now.html', {
            'form': form
        })
def view_volunteerdetail(request, pid):

    if not request.user.is_authenticated:
        return redirect('/login-admin')

    volunteer = get_object_or_404(
        Volunteer,
        id=pid
    )

    if request.method == "POST":

        volunteer.status = request.POST.get("status")

        volunteer.adminremark = request.POST.get(
            "adminremark"
        )

        volunteer.updationdate = timezone.now()

        volunteer.save()

        messages.success(
            request,
            "Volunteer information updated successfully."
        )

        return redirect(
            "view_volunteerdetail",
            pid=volunteer.id
        )

    return render(
        request,
        "app/view-volunteerdetail.html",
        {
            "volunteer": volunteer
        }
    )
class view_donordetail(View):

    def get(self, request, pid):

        if not request.user.is_authenticated:
            return redirect('/login-admin')

        donor = get_object_or_404(
            Donor,
            id=pid
        )

        return render(
            request,
            "app/view-donordetail.html",
            {
                "donor": donor
            }
        )
class view_donationdetail(View):

    def get(self, request, pid):

        if not request.user.is_authenticated:
            return redirect('/login-admin')

        donation = get_object_or_404(
            Donation,
            id=pid
        )

        return render(
            request,
            "app/view-donationdetail.html",
            {
                "donation": donation
            }
        )

    def post(self, request, pid):

        if not request.user.is_authenticated:
            return redirect('/login-admin')

        donation = get_object_or_404(
            Donation,
            id=pid
        )

        status = request.POST.get("status")
        adminremark = request.POST.get("adminremark")

        if status == "accept":
            donation.status = "Accepted"

        elif status == "reject":
            donation.status = "Reject"

        donation.adminremark = adminremark
        donation.updationdate = date.today()

        donation.save()

        return redirect(
            "view_donationdetail",
            pid=donation.id
        )

def donation_history(request):

    if not request.user.is_authenticated:
        return redirect('donorlogin')

    donor = Donor.objects.get(user=request.user)

    donations = Donation.objects.filter(donor=donor)

    return render(request, "app/donation-history.html", {
        'donation': donations
    })


class profile_donor(View):

    def get(self, request):
        user = request.user
        donor = get_object_or_404(Donor, user=user)

        form1 = UserForm(instance=user)
        form2 = DonorSignupForm(instance=donor)

        return render(request, "app/profile-donor.html", {
            'form1': form1,
            'form2': form2,
            'donor': donor
        })


    def post(self, request):

        user = request.user
        donor = get_object_or_404(Donor, user=user)

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        userpic = request.FILES.get('userpic')


        # Update User table
        user.first_name = firstname
        user.last_name = lastname
        user.save()


        # Update Donor table
        donor.contact = contact
        donor.address = address

        if userpic:
            donor.userpic = userpic

        donor.save()


        messages.success(request, "Profile updated successfully!")

        return redirect('profile_donor')


class changepwd_donor(View):
    def get(self, request):
        form = MyPasswordChangeForm(request.user)
        return render(request, 'app/changepwd-donor.html', {'form': form})

    def post(self, request):
        form = MyPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully.")
            return redirect("changepwd_donor")

        messages.error(request, "Please correct the errors below.")

        return render(request, 'app/changepwd-donor.html', {'form': form})


# volunteer dashboard
def index_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')

    user = request.user
    volunteer = Volunteer.objects.get(user=user)

    print("Logged user:", user.username)
    print("Volunteer ID:", volunteer.id)

    all_donations = Donation.objects.filter(volunteer=volunteer)

   

    for d in all_donations:
        print("Donation ID:", d.id, "Status:", d.status)


    totalCollectionReq = Donation.objects.filter(
        volunteer=volunteer,
        status='Volunteer Allocated'
    ).count()

    totalRecDonation = Donation.objects.filter(
        volunteer=volunteer,
        status='Donation Received'
    ).count()

    totalNotRecDonation = Donation.objects.filter(
        volunteer=volunteer,
        status='Donation Not Received'
    ).count()

    totalDonationDelivered = Donation.objects.filter(
        volunteer=volunteer,
        status='Donation Delivered Successfully'
    ).count()
 

    context = {
        'totalCollectionReq': totalCollectionReq,
        'totalRecDonation': totalRecDonation,
        'totalNotRecDonation': totalNotRecDonation,
        'totalDonationDelivered': totalDonationDelivered,
    }

    return render(request, 'app/index-volunteer.html', context)
   


def collection_req(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')

    volunteer = Volunteer.objects.get(user=request.user)

    donation = Donation.objects.filter(
        volunteer=volunteer,
        status='Volunteer Allocated'
    )

    return render(request, "app/collection-req.html",{"donation": donation})


def donationrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation = Donation.objects.filter(volunteer=volunteer, status='Donation Received')
    return render(request, 'app/donationrec-volunteer.html', locals())



def donationnotrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation = Donation.objects.filter(volunteer=volunteer, status='Donation Not Received') 

    return render(request, "app/donationnotrec-volunteer.html", locals())


def donationdelivered_volunteer(request):

    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation = Donation.objects.filter(volunteer=volunteer, status='Donation Delivered Successfully')
    return render(request, "app/donationdelivered-volunteer.html", locals())


class profile_volunteer(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login_volunteer")

        user = request.user
        volunteer = get_object_or_404(Volunteer, user=user)

        form1 = UserForm(instance=user)
        form2 = VolunteerSignupForm(instance=volunteer)

        return render(request, "app/profile-volunteer.html", {
            "form1": form1,
            "form2": form2,
            "volunteer": volunteer,
        })

    def post(self, request):

        user = request.user
        volunteer = get_object_or_404(Volunteer, user=user)

        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.save()


        volunteer.contact = request.POST.get('contact')
        volunteer.address = request.POST.get('address')
        volunteer.aboutme = request.POST.get('aboutme')


        # Upload Profile Picture
        userpic = request.FILES.get('userpic')

        if userpic:
            volunteer.userpic = userpic


        # Upload ID Picture
        idpic = request.FILES.get('idpic')

        if idpic:
            volunteer.idpic = idpic


        volunteer.save()


        messages.success(request, "Profile updated successfully!")

        return redirect('profile_volunteer')

    


class changepwd_volunteer(View):
    def get(self, request):
        form = MyPasswordChangeForm(request.user)
        return render(request, 'app/changepwd-volunteer.html', {'form': form})

    def post(self, request):
        form = MyPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully.")
            return redirect("changepwd_volunteer")

        messages.error(request, "Please correct the errors below.")

        return render(request, 'app/changepwd-volunteer.html', {'form': form})
    


# view details
def donationdetail_donor(request, pid):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    donation = Donation.objects.get(id=pid)
    return render(request, "app/donationdetail-donor.html", locals())


class donationcollection_detail(View):

    def get(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-volunteer')

        donation = get_object_or_404(
            Donation,
            id=pid
        )

        return render(
            request,
            "app/donationcollection-detail.html",
            {
                "donation": donation
            }
        )


    def post(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-volunteer')

        donation = get_object_or_404(
            Donation,
            id=pid
        )

        status = request.POST.get('status')
        volunteerremark = request.POST.get('volunteerremark')

        try:
            donation.status = status
            donation.volunteerremark = volunteerremark
            donation.updationdate = date.today()
            donation.save()

            messages.success(
                request,
                "Volunteer Status Updated Successfully"
            )

            return redirect(
                "donationcollection_detail",
                pid=donation.id
            )

        except Exception as e:
            print(e)

            messages.error(
                request,
                "Failed to update donation"
            )

            return redirect(
                "donationcollection_detail",
                pid=donation.id
            )


class donationrec_detail(View):

    def get(self, request, pid):
        if not request.user.is_authenticated:
            return redirect("login_volunteer")

        donation = get_object_or_404(Donation, id=pid)

        return render(
            request,
            "app/donationrec-detail.html",
            {
                "donation": donation,
            }
        )

    def post(self, request, pid):
        if not request.user.is_authenticated:
            return redirect("login_volunteer")

        donation = get_object_or_404(Donation, id=pid)

        deliverypic = request.FILES.get("deliverypic")

        try:
            # Only allow delivery when donation has been received
            if donation.status == "Donation Received":

                if not deliverypic:
                    messages.error(
                        request,
                        "Please upload the delivery picture."
                    )

                    return render(
                        request,
                        "app/donationrec-detail.html",
                        {
                            "donation": donation,
                        },
                    )

                # Update donation status
                donation.status = "Donation Delivered Successfully"
                donation.updationdate = date.today()
                donation.save()

                # Create Gallery record
                Gallery.objects.create(
                    donation=donation,
                    deliverypic=deliverypic
                )

                messages.success(
                    request,
                    "Donation Delivered Successfully."
                )

            return redirect(
                "donationrec_detail",
                pid=donation.id
            )

        except Exception as e:
            print("DELIVERY ERROR:", e)

            messages.error(
                request,
                "Something went wrong."
            )

            return render(
                request,
                "app/donationrec-detail.html",
                {
                    "donation": donation,
                },
            )