from django.urls import path
from rooms.views import RoomListCreateView, RoomDetailView, ReservationListCreateView, ReservationDetailView
from rooms.api_views import RoomListAPIView, RoomCreateAPIView, RoomDetailAPIView, ReservationCreateAPIView, ReservationDetailAPIView

urlpatterns = [
    path('rooms/', RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('api/rooms/', RoomListAPIView.as_view(), name='room-list'),
    path('api/rooms/create/', RoomCreateAPIView.as_view(), name='room-create'),
    path('api/rooms/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),
    path('api/reservations/create/', ReservationCreateAPIView.as_view(), name='reservation-create'),
    path('api/reservations/<int:pk>/', ReservationDetailAPIView.as_view(), name='reservation-detail'),
]