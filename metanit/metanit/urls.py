from django.contrib import admin
from django.urls import path, include
from bank import views

action = [
    path('transaction/', views.translate),
    path('getall/', views.get_user_balances),
]

bank = [
    path('profile/', views.get_profile)
]

auth = [
    path('reg/', views.reg, name='reg'),
    path('log/', views.log, name='log'),
    path('logout/', views.logout_v, name='logout')

]

api = [
    path('action/', include(action)),
    path('bank/', include(bank)),
    path('auth/', include(auth)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api))
]
