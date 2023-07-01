from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from rooms.front_views import FrontRoomListView, FrontReservationListView, FrontUserLoginView
from rooms.views import (
    RoomListView,
    RoomCreateView,
    ReservationListView,
    ReservationCreateView,
    ReservationDetailView,
    UserLoginView,
    UserSignUpView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("rooms/create/", RoomCreateView.as_view(), name="room-create"),
    path("reservations/", ReservationListView.as_view(), name="reservation-list"),
    path(
        "reservations/create", ReservationListView.as_view(), name="reservation-create"
    ),
    path(
        "reservations/<int:pk>/",
        ReservationDetailView.as_view(),
        name="reservation-detail",
    ),
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("front/rooms/", FrontRoomListView.as_view(), name="front-room-list"),
    # path("front/reservations/", FrontReservationListView.as_view(), name="front-reservation-list"),
    # path("front/login/", FrontUserLoginView.as_view(), name="front-login"),
    
]
