from __future__ import unicode_literals

from django.urls import path
from django.conf.urls import include, url

from front import views as front_views


handler404 = 'front.views.handler404'
handler500 = 'front.views.handler500'

urlpatterns = [
    path('', front_views.PoleNumbersView.as_view(), name='pole_numbers'),
]
