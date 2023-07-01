from django.shortcuts import render, redirect, get_object_or_404
from .views import RoomListView, ReservationListView, UserLoginView
from .serializers import RoomSerializer, ReservationSerializer, UserSerializer
from .models import Reservation
from rest_framework.authtoken.models import Token


class FrontRoomListView(RoomListView):

    def get(self, request):
        queryset = self.get_queryset()
        serializer = RoomSerializer(queryset, many=True)
        data = serializer.data
        
        return render(request, 'roomList.html', {'rooms': data})
    
# class FrontReservationListView(ReservationListView):

#     def get(self, request):
#         token = request.auth
#         if not token or not Token.objects.filter(key=token).exists():
#             return redirect('front-login')
         
#         queryset = Reservation.objects.all()
#         serializer = ReservationSerializer(queryset, many=True)
#         data = serializer.data
        
#         return render(request, 'reservationList.html', {'reservations': data})


# class FrontUserLoginView(UserLoginView):
    
#     def post(self, request):
#         response = self.post(request)
#         serializer = UserSerializer(response, many=True)
#         data = serializer.data

#         return render(request, 'login.html', {'data': data})
