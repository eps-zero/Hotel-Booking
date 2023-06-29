from django.urls import path
from django.contrib import admin
from rooms.views import RoomListView, RoomCreateView, RoomDetailView, ReservationListView, ReservationCreateView, ReservationDetailView, UserLoginView, UserSignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/create/', RoomCreateView.as_view(), name='room-create'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),
    path('reservations/create', ReservationListView.as_view(),
         name='reservation-create'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(),
         name='reservation-detail'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
]
