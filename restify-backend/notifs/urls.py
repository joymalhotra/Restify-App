from django.urls import path
from notifs.views import AllUnreadNotificationAPIView,ReadAllNotificationAPIView

app_name = 'notifs'
urlpatterns = [
    path('all/', AllUnreadNotificationAPIView.as_view(), name='all-notifs'),
    path('read_all/', ReadAllNotificationAPIView.as_view(), name='all-notifs'),

]
