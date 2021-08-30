from __future__ import unicode_literals

from django.urls import path

from main import views as main_views


handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'

urlpatterns = [
    path('', main_views.PoleNumbersView.as_view(), name='pole_numbers'),
]
