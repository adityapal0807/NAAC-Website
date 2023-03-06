from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('Login',views.login_view,name='login_view'),
    path('Register',views.register_user,name='register_user'),
    path('Logout',views.logout_view,name='logout_view'),
    path('Personal_Details',views.personal_details,name='personal_details'),
    path('Work_Details',views.work_details,name='work_details'),
    path('Contact_Details',views.contact_details,name='contact_details'),
    path('Bank_Details',views.bank_details,name='bank_details'),
    path('Experience_Details',views.experience_details,name='experience_details'),
    path('Patent',views.patent_register,name='patent_register'),
    path('PHD_Awarded',views.phd_awarded,name='phd_awarded'),
    path('Research_Publication',views.research_publication,name='research_publication'),
    path('Awards',views.awards,name='awards'),
    path('Books',views.books,name='books'),
    path('Conference',views.conference,name='conference'),
    path('All Patents',views.patent_display,name='patent_display'),
    path("Ph.D's",views.phd_display,name='phd_display'),
    path('Paper Published',views.research_display,name='research_display'),
    path('Awards List',views.award_display,name='award_display'),
    path('Books List',views.books_display,name='books_display'),
    path('Conference Proceedings',views.conference_display,name='conference_display'),

    # Edit and Delete the data
    path('Edit_Patent/<str:id>',views.edit_patent,name='edit_patent'),
    path('Delete_Patent/<str:id>',views.delete_patent,name='delete_patent'),

    path('Edit_Ph.D/<str:id>',views.edit_phd,name='edit_phd'),
    path('Delete_Ph.D/<str:id>',views.delete_phd,name='delete_phd'),

    path('Edit_Research Paper/<str:id>',views.edit_research,name='edit_research'),
    path('Delete_Research/<str:id>',views.delete_research,name='delete_research'),

    path('Edit_Award/<str:id>',views.edit_award,name='edit_award'),
    path('Delete_Award/<str:id>',views.delete_award,name='delete_award'),

    path('Edit_Book/<str:id>',views.edit_book,name='edit_book'),
    path('Delete_Book/<str:id>',views.delete_book,name='delete_book'),

    path('Edit_Conference/<str:id>',views.edit_conference,name='edit_conference'),
    path('Delete_Conference/<str:id>',views.delete_conference,name='delete_conference'),

    #Download CSVS
    path('Patent_Download',views.patent_download,name='patent_download'),
    path('Research_Paper_Download',views.research_download,name='research_download'),
    path('PhD_Download',views.phd_download,name='phd_download'),
    path('Award_Download',views.award_download,name='award_download'),
    path('Books_Download',views.books_download,name='books_download'),
    path('Conference_Download',views.conference_download,name='conference_download'),
    


  
    ]
