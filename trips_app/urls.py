"""trips_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from trips.views import AddFavoriteTrip, CreateTrip, DeleteTrip, MyFavoriteTripList, ProfileView, Register, TripDetails, TripList, UpdateProfile, UpdateDeleteTrip, UserTokenApiView, UserTripList, WantToGoTrip

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth APIs 
    path('register/', Register.as_view(), name='register'),
    path('login/', UserTokenApiView.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # profile APIs
    path('profile/<int:profile_id>/', ProfileView.as_view()),
    path('my-profile/', UpdateProfile.as_view()),

    # Trips APIs 
    path('trips/', TripList.as_view()),
    path('new-trip/', CreateTrip.as_view()),
    path('my-trips/', UserTripList.as_view()),
    path('trips/my-favorite/', MyFavoriteTripList.as_view()),
    path('trips/add-favorite/<int:trip_id>/', AddFavoriteTrip.as_view()),
    path('trips/want-to/<int:trip_id>/', WantToGoTrip.as_view()),
    path('trip/<int:trip_id>', UpdateDeleteTrip.as_view()), # user can delete , update and view their own trips must be owned by them
    path('trip/details/<int:trip_id>', TripDetails.as_view()), # anyone can view the trip details ... shouldnt be authintecated and the trip shoulnt be owned by the viewer

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
