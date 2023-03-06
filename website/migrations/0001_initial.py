# Generated by Django 4.1 on 2023-02-27 18:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('employee_code', models.IntegerField(blank=True, null=True)),
                ('employee_name', models.CharField(max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Work_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=50, null=True)),
                ('mode_of_recruitment', models.CharField(max_length=50, null=True)),
                ('dob_joining', models.DateField(blank=True, null=True)),
                ('dob_retirement', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PHD_Awarded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scholor_name', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('guide_names', models.TextField(max_length=1000)),
                ('thesis_title', models.TextField(max_length=500)),
                ('registration_date', models.DateField()),
                ('award_date', models.DateField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Personal_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(max_length=50, null=True)),
                ('mother_name', models.CharField(max_length=50, null=True)),
                ('maritial_status', models.CharField(max_length=10, null=True)),
                ('spouse_name', models.CharField(blank=True, default='None', max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(max_length=20, null=True)),
                ('blood_group', models.CharField(max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=100)),
                ('patent_number', models.CharField(max_length=20)),
                ('patent_title', models.TextField(max_length=1000)),
                ('category', models.CharField(max_length=12)),
                ('patent_year', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paper_Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=500)),
                ('author_names', models.TextField(max_length=1000)),
                ('journal_name', models.CharField(max_length=500)),
                ('journal_website', models.CharField(max_length=500, null=True)),
                ('issn', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=100, null=True)),
                ('month_published', models.CharField(max_length=20, null=True)),
                ('year_published', models.CharField(max_length=4)),
                ('volume_number', models.CharField(max_length=20, null=True)),
                ('issue_number', models.CharField(max_length=20)),
                ('pp', models.CharField(max_length=100, null=True)),
                ('doi', models.CharField(max_length=500, null=True)),
                ('ugc_core', models.CharField(max_length=10)),
                ('scopus', models.CharField(max_length=10)),
                ('sci_scie_esci', models.CharField(max_length=10)),
                ('impact_factor', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experience_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teaching_experience', models.IntegerField(null=True)),
                ('research_experience', models.IntegerField(null=True)),
                ('industry_experience', models.IntegerField(null=True)),
                ('pup_teaching_experience', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhar', models.CharField(max_length=12, null=True, unique=True)),
                ('pan_number', models.CharField(max_length=20, null=True, unique=True)),
                ('state', models.CharField(max_length=30, null=True)),
                ('district', models.CharField(max_length=30, null=True)),
                ('pin', models.IntegerField(null=True)),
                ('mobile', models.IntegerField(null=True)),
                ('mobile_alt', models.IntegerField(null=True)),
                ('landline', models.IntegerField(null=True)),
                ('corresponding_address', models.TextField(max_length=500)),
                ('permanent_address', models.TextField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Books_Conference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authors', models.TextField(max_length=1000)),
                ('category', models.CharField(max_length=100)),
                ('title_chap_paper', models.TextField(max_length=500)),
                ('title_book_conf', models.TextField(max_length=500)),
                ('type_conf', models.CharField(max_length=500)),
                ('date', models.DateField()),
                ('isbn', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=100)),
                ('pp', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authors', models.TextField(max_length=1000)),
                ('title', models.TextField(max_length=500)),
                ('publisher', models.CharField(max_length=100)),
                ('isbn', models.CharField(max_length=50)),
                ('year_published', models.CharField(max_length=4)),
                ('affiliating_institute', models.TextField(max_length=2000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bank_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=50, null=True)),
                ('bank_ifsc', models.CharField(max_length=50, null=True)),
                ('bank_account', models.CharField(max_length=50, null=True)),
                ('bank_branch', models.CharField(max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Awards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scholor_name', models.CharField(max_length=100)),
                ('activity', models.CharField(max_length=100)),
                ('award_name', models.CharField(max_length=500)),
                ('authority_name', models.CharField(max_length=500)),
                ('year_awarded', models.CharField(max_length=4)),
                ('level', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
