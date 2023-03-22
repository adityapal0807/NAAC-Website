from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    employee_code = models.CharField(blank=True,null=True,max_length=50)
    employee_name = models.CharField(max_length=50,null=True)
    aadhar_number = models.CharField(max_length=12)
    password_reset_token = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.employee_code} , {self.employee_name} , {self.aadhar_number}"
    

class Personal_Detail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    father_name = models.CharField(max_length=50,null=True)
    mother_name = models.CharField(max_length=50,null=True)
    maritial_status = models.CharField(max_length=10,null=True)
    spouse_name = models.CharField(max_length=20,default='None',blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=20,null=True)
    blood_group = models.CharField(max_length=10,null=True)

    def __str__(self):
        return f"{self.user.employee_code}"

class Work_Detail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    designation = models.CharField(max_length=50,null=True)
    mode_of_recruitment = models.CharField(max_length=50,null=True)
    dob_joining = models.DateField(blank=True,null=True)
    dob_retirement = models.DateField(blank=True,null=True)

    def __str__(self):
        return f"{self.user.employee_code}"

class Contact_Detail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    aadhar = models.CharField(max_length=12,null=True,unique=True)
    pan_number = models.CharField(max_length=20,null=True,unique=True)
    state = models.CharField(max_length=30,null=True)
    district = models.CharField(max_length=30,null=True)
    pin = models.IntegerField(null=True)
    mobile = models.IntegerField(null=True)
    mobile_alt = models.IntegerField(null=True)
    landline = models.IntegerField(null=True)
    corresponding_address = models.TextField(max_length=500)
    permanent_address = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.user.employee_code}"

class Bank_Detail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=50,null=True)
    bank_ifsc = models.CharField(max_length=50,null=True)
    bank_account = models.CharField(max_length=50,null=True)
    bank_branch = models.CharField(max_length=50,null=True)

    def __str__(self):
        return f"{self.user.employee_code}"

class Experience_Detail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    teaching_experience = models.IntegerField(null=True)
    research_experience = models.IntegerField(null=True)
    industry_experience = models.IntegerField(null=True)
    pup_teaching_experience = models.IntegerField(null=True)
    
    def __str__(self):
        return f"{self.user.employee_code}"
    
class Patent(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    patent_number = models.CharField(max_length=20)
    patent_title = models.TextField(max_length=1000)
    category = models.CharField(max_length=12)
    patent_year = models.DateField()

    def __str__(self):
        return f"{self.author_name} patented {self.patent_title}"
    
class PHD_Awarded(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    scholor_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    guide_names = models.TextField(max_length=1000)
    thesis_title = models.TextField(max_length=500)
    registration_date = models.DateField()
    award_date = models.DateField(null=True)

    def __str__(self):
        return f"Ph.D to {self.scholor_name}"

class Paper_Publication(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField(max_length=500)
    author_names = models.TextField(max_length=1000)
    journal_name = models.CharField(max_length=500)
    journal_website = models.CharField(max_length=500,null=True)
    issn = models.CharField(max_length=50)
    publisher = models.CharField(max_length=100,null=True)
    month_published = models.CharField(max_length=20,null=True)
    year_published = models.CharField(max_length=4)
    volume_number = models.CharField(max_length=20,null=True)
    issue_number = models.CharField(max_length=20)
    pp = models.CharField(max_length=100,null=True)
    doi = models.CharField(max_length=500,null=True)
    ugc_core = models.CharField(max_length=10)
    scopus = models.CharField(max_length=10)
    sci_scie_esci =  models.CharField(max_length=10)
    impact_factor = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return f"{self.title} paper by {self.author_names}"

class Awards(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    scholor_name = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)
    award_name = models.CharField(max_length=500)
    authority_name = models.CharField(max_length=500)
    year_awarded = models.CharField(max_length=4)
    level = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.scholor_name} awarded"

class Books(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    authors = models.TextField(max_length=1000)
    title = models.TextField(max_length=500)
    publisher = models.CharField(max_length=100)
    isbn = models.CharField(max_length=50)
    year_published = models.CharField(max_length=4)
    affiliating_institute = models.TextField(max_length=2000)

    def __str__(self):
        return f"{self.authors} book on {self.title}"

class Books_Conference(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    authors = models.TextField(max_length=1000)
    category = models.CharField(max_length=100)
    title_chap_paper = models.TextField(max_length=500)
    title_book_conf = models.TextField(max_length=500)
    type_conf = models.CharField(max_length=500)
    date = models.DateField()
    isbn = models.CharField(max_length=50)
    publisher = models.CharField(max_length=100)
    pp = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category} on {self.title_book_conf}"

class CSV_Download(models.Model):
    csv = models.FileField(upload_to='csv_files')
    
    



