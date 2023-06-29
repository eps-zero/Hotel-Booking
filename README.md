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
   git clone https://github.com/your-username/hotel-booking.git
   ```
2. Navigate to the project directory:
   ```
   cd hotel-booking
   ```
3. nstall the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Type in terminal:
   ```
   psql -U postgres
   ```
5. Create database:
   ```
   CREATE DATABASE your_database_name;
   ```
6. Create user:
   ```
   CREATE USER your_user_name;
   ```
7. In  file settings.py find section DATABASES and change it to:
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
8. Apply the database migrations:
   ```
   python manage.py migrate
   ```
9. Create superuser:
   ```
   python manage.py createsuperuser
   ```
10. Start the development server:
   ```
   python manage.py runserver
   ```
11. Open your web browser and visit http://localhost:8000 to access the application.
   

## Usage

   Access the home page to view available rooms and make reservations.
   Register an account or log in to access additional features.
   Use the admin panel to manage rooms and reservations.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

   1. Fork the repository.
   2. Create a new branch for your feature or bug fix.
   3. Make your changes and commit them.
   4. Push your changes to your forked repository.
   5. Submit a pull request explaining your changes.
