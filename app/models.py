from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Donor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=300, null=True)
    userpic = models.ImageField(upload_to='donor', null=True, blank=True)
    regdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=300, null=True)
    userpic = models.ImageField(upload_to='volunteer', null=True, blank=True)
    idpic = models.ImageField(upload_to='volunteer', null=True, blank=True)
    aboutme = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=20, null=True)
    regdate = models.DateTimeField(auto_now_add=True)
    adminremark = models.CharField(max_length=300, null=True)
    updationdate = models.DateField(null=True)
    def __str__(self):
        return self.user.username

class DonationArea(models.Model):
    areaname = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    creationdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.areaname
DONATION_CHOICES = [
    ('Food Donation', 'Food Donation'),
    ('Cloth Donation', 'Cloth Donation'),
    ('Footwear Donation', 'Footwear Donation'),
    ('Books Donation', 'Books Donation'),
    ('Furniture Donation', 'Furniture Donation'),
    ('School Material Donation', 'School Material Donation'),
    ('Other Donation', 'Other Donation'),
]


class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)

    donationname = models.CharField(
    max_length=100,
    choices=DONATION_CHOICES,
    null=True,
    blank=True
)

    donationpic = models.ImageField(
        upload_to='donation/',
        null=True,
        blank=True
    )

    collectionloc = models.CharField(
        max_length=300,
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        default='Pending'
    )

    donationdate = models.DateField(
        default=date.today
    )

    adminremark = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    volunteer = models.ForeignKey(
        Volunteer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    donationarea = models.ForeignKey(
        DonationArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    volunteerremark = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    updationdate = models.DateField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.donationname or "Unnamed Donation"

class Gallery(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    deliverypic = models.FileField(null=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
   
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)

    reply_message = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    