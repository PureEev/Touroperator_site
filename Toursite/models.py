from django.db import models

class aircraft(models.Model):
    aircraft_id = models.IntegerField(primary_key=True, db_column='aircraft_id')
    name = models.TextField(db_column='name')
    seats_number = models.IntegerField(db_column='seats_number')
    class Meta:
        managed = False
        db_table = 'aircraft'

class airline(models.Model):
    airlines_id = models.IntegerField(primary_key=True, db_column='airlines_id')
    airlines = models.TextField(db_column='airlines')
    class Meta:
        managed = False
        db_table = 'airlines'

class tour_booking_history(models.Model):
    tour_id = models.IntegerField(primary_key=True, db_column='tour_id')
    number_people = models.IntegerField(db_column='number_people')
    tour_order_number_id = models.IntegerField(db_column='tour_order_number_id')
    action = models.CharField(max_length=45, db_column='action')
    amount = models.IntegerField(db_column='amount')
    class Meta:
        managed = False
        db_table = 'tour_booking_history'
class WeeklyFlightSchedule(models.Model):
    WFS_id = models.AutoField(primary_key=True, db_column='WFS_id')  # Идентификатор города отправления
    week_day = models.TextField(db_column='week_day')    # Идентификатор города прибытия
    time = models.TextField(db_column='time')
    price = models.IntegerField(db_column='price')
    aircraft_id = models.IntegerField(db_column='aircraft_id')
    departure_city_id = models.IntegerField(db_column='departure_city_id')
    arrival_city_id = models.TextField(db_column='arrival_city_id')
    airline_id = models.IntegerField(db_column='airline_id')
    flight_duration = models.TextField(db_column='flight_duration')
    class Meta:
        managed = False
        db_table = 'weekly_flight_schedule'

class flight_shedule(models.Model):
    flight_id = models.IntegerField(primary_key=True, db_column='flight_id')
    date = models.DateField(db_column= 'date')
    tickets_number = models.IntegerField(db_column='tickets_number')
    WFS_id = models.IntegerField(db_column='WFS_id')
    flight_number = models.IntegerField(db_column='flight_number')

    class Meta:
        managed = False
        db_table = 'flight_schedule'

class History(models.Model):
    Tour_id = models.IntegerField(db_column='Tour_id')
    Flight_id = models.IntegerField(db_column='Flight_id')
    date = models.DateField(db_column='date')
    price = models.IntegerField(db_column='price')
    Action = models.TextField(db_column='Action')
    Operation_number = models.IntegerField(primary_key=True, db_column='Operation_number')
    unique_order_number = models.IntegerField(db_column='unique_order_number')
    amount = models.IntegerField(db_column='amount')
    class Meta:
        managed = False
        db_table = 'history'
class City(models.Model):
    City_id = models.AutoField(primary_key=True, db_column='City_id')
    Name_city = models.CharField(max_length=100, db_column='Name_city')
    class Meta:
        managed = False
        db_table = 'cities'

    @classmethod
    def get_city_id_by_name(cls, name):
        try:
            city_data = cls.objects.get(Name_city=name)
            return city_data.City_id
        except cls.DoesNotExist:
            return None

class flights_in_tours(models.Model):
    Flights_in_tours_id = models.IntegerField(primary_key=True, db_column='flights_in_tours_id')
    City_id = models.IntegerField(db_column='City_id')
    Day_number_in_city = models.IntegerField(db_column='day_number_in_city')
    Tour_number_id = models.IntegerField(db_column='tour_number_id')
    class Meta:
        managed = False
        db_table = 'flights_in_tours'
    #City_id = models.ForeignKey(City, on_delete=models.CASCADE)

    @classmethod
    def get_tours_id_by_city_id(cls, city_id):
        try:
            FlInTours_data = cls.objects.filter(City_id=city_id)
            return list(FlInTours_data.values_list('Tour_number_id', flat=True))
        except cls.DoesNotExist:
            return None

class TourDescription(models.Model):
    tour_number_id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image_url = models.TextField(max_length=100)
    class Meta:
        managed = False
        db_table = 'tour_description'

    @classmethod
    def get_tour_name_by_tour_id(cls, tour_id):
        try:
            Tour_info = cls.objects.filter(tour_number_id=tour_id)
            return Tour_info.values_list('name', flat=True)
        except cls.DoesNotExist:
            return None
    @classmethod
    def get_tour_price_by_tour_id(cls, tour_id):
        try:
            Tour_info = cls.objects.filter(tour_number_id=tour_id)
            return Tour_info.values_list('price', flat=True)
        except cls.DoesNotExist:
            return None
    @classmethod
    def get_tour_description_by_tour_id(cls, tour_id):
        try:
            Tour_info = cls.objects.filter(tour_number_id=tour_id)
            return Tour_info.values_list('description', flat=True)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_tour_image_number_by_tour_id(cls, tour_id):
        try:
            Tour_info = cls.objects.filter(tour_number_id=tour_id)
            return Tour_info.values_list('image_url', flat=True)[0]
        except cls.DoesNotExist:
            return None

class connect_tours_wfs(models.Model):
    tour_number_id = models.IntegerField(db_column='tour_number_id')
    WFS_id = models.IntegerField(db_column='WFS_id')
    number = models.IntegerField(primary_key=True, db_column='number')
    class Meta:
        managed = False
        db_table = 'connect_tours_wfs'