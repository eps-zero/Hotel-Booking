from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from rooms.front_views import (
    FrontRoomListView,
    FrontReservationListView,
    FrontReservationCreateView,
    FrontReservationDetailView,
    FrontSignupView,
    FrontLoginView,
    FrontLogoutView,
)
from rooms.views import (
    RoomListView,
    ReservationListView,
    ReservationCreateView,
    SignupView,
    LoginView,
    LogoutView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("reservations/", ReservationListView.as_view(), name="reservation-list"),
    path(
        "reservations/create",
        ReservationCreateView.as_view(),
        name="reservation-create",
    ),
    path(
        "reservations/<int:pk>/",
        FrontReservationDetailView.as_view(),
        name="reservation-detail",
    ),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("front/rooms/", FrontRoomListView.as_view(), name="front-room-list"),
    path(
        "front/reservations/",
        FrontReservationListView.as_view(),
        name="front-reservation-list",
    ),
    path(
        "front/reservations/create",
        FrontReservationCreateView.as_view(),
        name="front-reservation-create",
    ),
    path("front/signup/", FrontSignupView.as_view(), name="front-signup"),
    path("front/login/", FrontLoginView.as_view(), name="front-login"),
    path("front/logout/", FrontLogoutView.as_view(), name="front-logout"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
