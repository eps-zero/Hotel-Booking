# Hotel Booking

Hotel Booking is a Django-based backend web application for managing hotel rooms and reservations.

## Features

- View available rooms based on various filters such as price, capacity, and dates.
- Make room reservations for specific dates.
- Admin panel for managing rooms and reservations.
- User authentication and registration.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/eps-zero/hotel-booking.git
   ```
2. Navigate to the project directory:
   ```
   cd hotel-booking
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Type in terminal:
   ```
   psql -U postgres
   ```
6. Create database:
   ```
   CREATE DATABASE your_database_name;
   ```
7. Create user:
   ```
   CREATE USER your_user_name;
   ```
8. In  file settings.py find section DATABASES and change it to:
   ```
   'ENGINE': 'django.db.backends.postgresql',
   'NAME': 'your_database_name',
   'USER': 'your_username',
   'PASSWORD': 'your_password',
   'HOST': 'localhost',
   'PORT': '5432',
   ```
   In my case it look like this:
   ```
   'ENGINE': 'django.db.backends.postgresql',
   'NAME': 'hotel_booking_data_base',
   'USER': 'admin',
   'PASSWORD': 'mikeTyson',
   'HOST': 'localhost',
   'PORT': '5431',
   ```
9. Apply the database migrations:
   ```
   python manage.py migrate
   ```
10. Create superuser:
      ```
      python manage.py createsuperuser
      ```
11. Start the development server:
      ```
      python manage.py runserver
      ```
11. Open your web browser and visit `http://localhost:8000` to access the application.
   

## Usage
Here is a description for each URL in the README.md file:

   - `/admin/` - This URL is used for accessing the admin interface of the application. It provides a web-based administration panel for managing the site's data.

   - `/rooms/` - This URL is used for accessing the list view of rooms. It is associated with the RoomListView class-based view, which allows filtering of rooms based on various parameters. The view accepts the following optional query parameters:

    - min_price (optional) - Filters rooms by a minimum price per day.
    - max_price (optional) - Filters rooms by a maximum price per day.
    - capacity (optional) - Filters rooms by their capacity.
    - ordering (optional) - Orders the rooms based on a specific criterion, such as price (ascending), -price (descending), capacity (ascending), or -capacity (descending).
    - check_in_date (optional) - Filters rooms based on availability starting from the specified check-in date. The format should be YYYY-MM-DD.
    - check_out_date (optional) - Filters rooms based on availability up to the specified check-out date. The format should be YYYY-MM-DD.

The RoomListView class retrieves the queryset of Room objects and applies the provided filters. It excludes any rooms that are already reserved within the specified date range. The resulting list of rooms is then serialized using the RoomSerializer and returned as a response.

Example usage: `http://localhost:8000/rooms/?min_price=50&capacity=2&ordering=price`

   - `/reservations/` - This URL is used for accessing the list view of reservations. It is associated with the ReservationListView class-based view and displays a list of existing reservations. Only autorized users can see their reservations.

   - `/reservations/create` - This URL is used for creating a new reservation. It is also associated with the ReservationListView class-based view and provides a form for creating a reservation. Only autorized users can create reservations.

   - `/reservations/{your_reservation_id}/` - This URL is used for accessing the detail view of a reservation. The {your_reservation_id} part represents the reservation's primary key. It is associated with the ReservationDetailView class-based view and displays detailed information about a specific reservation.

   - `/signup/` - This URL is used for user sign-up functionality. It is associated with the UserSignUpView class-based view and provides a form for users to create a new account just using username and password.

   - `/login/` - This URL is used for user login functionality. It is associated with the UserLoginView class-based view and provides a form for users to log in to their existing accounts.
   - `/front/rooms` -  directory contains the HTML page responsible for displaying the list of rooms. Users can view available rooms and their details on this page.
   
   - `/front/reservations` - directory houses the HTML page for viewing the list of reservations. Users can see their existing reservations and relevant details on this page.
   
   - `/front/reservations/creat`e directory stores the HTML page used to create a new reservation. Only registered users have the privilege to view this page and create reservations.

## Screens
![Room List](/screens/screen1.png)
![Reservation List](/screens/screen2.png)
![Reservation Create](/screens/screen3.png)

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

   1. Fork the repository.
   2. Create a new branch for your feature or bug fix.
   3. Make your changes and commit them.
   4. Push your changes to your forked repository.
   5. Submit a pull request explaining your changes.