from django.urls import path
from . import views

  

urlpatterns = [
    # Homepage
    path('', views.homepage, name='homepage'),

    # Info section
    path('info/', views.info, name='info'),
    path('info/gym/', views.gym_info, name='gym_info'),
    path('info/facility/', views.facility_info, name='facility_info'),
    path('info/announcement/', views.announcement_info, name='announcement_info'),
    path('info/cost/', views.cost_info, name='cost_info'),
    #login
    path('login/', views.login_view, name='login'),
    #contact
    path('contact/', views.contact_view, name='contact'),
    #sign up
    path('signup/', views.signup_view, name='signup'),



    # Membership management
    path('mem/', views.membership, name='membership'),
    path('mem/renew/', views.renew_membership, name='renew_membership'),
    path('mem/cancel/', views.cancel_membership, name='cancel_membership'),
    path('mem/update/', views.update_membership, name='update_membership'),

    # Member only
    path('memberonly/', views.memberonly, name='memberonly'),
    path('memberonly/bookclass/', views.book_class, name='book_class'),
    path('memberonly/bookactivity/', views.book_activity, name='book_activity'),
    path('memberonly/feedback/', views.feedback, name='feedback'),

    # Staff only
    path('staffonly/', views.staffonly, name='staffonly'),
    path('staffonly/createclass/', views.create_class, name='create_class'),
    path('staffonly/cancelclass/', views.cancel_class, name='cancel_class'),
    path('staffonly/createannouncement/', views.create_announcement, name='create_announcement'),
    path('staffonly/feedback/', views.staff_feedback, name='staff_feedback'),
   
]
