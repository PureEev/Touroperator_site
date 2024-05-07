from datetime import timedelta
import datetime
import random

from django.contrib.gis.geoip2.resources import City
from django.db.models import Func, F
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TourDescription, flights_in_tours, WeeklyFlightSchedule, flight_shedule, aircraft, \
    tour_booking_history, connect_tours_wfs, History, airline
from Toursite.forms import ContactForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import TourDescription, City

def index(request):
    return render(request, 'index.html')

def get_tour_numbers_by_city(city_id):
    tour_numbers = flights_in_tours.objects.filter(City_id=city_id).values_list('Tour_number_id', flat=True).distinct()
    return list(tour_numbers)

def generate_unique_tour_number():
    while True:
        tour_number = random.randint(10000, 99999)
        if not tour_booking_history.objects.filter(tour_order_number_id = tour_number).exists():
            return tour_number

def generate_unique_ticket_number():
    while True:
        ticket_number = random.randint(10000, 99999)
        if not History.objects.filter(unique_order_number = ticket_number).exists():
            return ticket_number
def filing_history_by_flight_id(tour_id, Flight_id, price, unique_order_number):
    current_date = timezone.now()
    new_record = History(
        Tour_id=tour_id,
        Flight_id=Flight_id,
        date=current_date,
        price=price,
        Action='покупка',
        unique_order_number=unique_order_number,
        amount=1
    )
    new_record.save()
    flight_shedule.objects.filter(flight_id=Flight_id).update(tickets_number=F('tickets_number') - 1)


def buying_tickets_by_order_tour(date, tour_id, unique_number):
    sum = 0
    WFS_id = connect_tours_wfs.objects.filter(tour_number_id=tour_id).order_by('number').values_list('WFS_id')
    cur_date = flight_shedule.objects.filter(WFS_id=WFS_id[0][0]).annotate(date_difference=Func(F('date') - date, function='ABS')).order_by('date_difference').first().date
    flight_id = list(flight_shedule.objects.filter(date=cur_date).values_list('flight_id'))
    price = list(WeeklyFlightSchedule.objects.filter(WFS_id=WFS_id[0][0]).values_list('price'))
    filing_history_by_flight_id(tour_id, flight_id[0][0], price[0][0], unique_number)
    sum+=int(price[0][0])
    for id_val in WFS_id[1:]:
        city = list(WeeklyFlightSchedule.objects.filter(WFS_id = id_val[0]).values_list('departure_city_id'))
        NumbOfDays = list(flights_in_tours.objects.filter(City_id = city[0][0]).values_list('Day_number_in_city'))
        cur_date += timedelta(days = NumbOfDays[0][0])
        flight_id = list(flight_shedule.objects.filter(date = cur_date).values_list('flight_id'))
        price = list(WeeklyFlightSchedule.objects.filter(WFS_id = id_val[0]).values_list('price'))
        filing_history_by_flight_id(tour_id, flight_id[0][0], price[0][0], unique_number)
        sum += int(price[0][0])
    return sum

def filing_history_operations(tour_id, Flight_id, price, Action, unique_order_number, amount):
    current_date = timezone.now()
    new_record = History(
    Tour_id = tour_id,
    Flight_id = Flight_id,
    date = current_date,
    price = price,
    Action = Action,
    unique_order_number = unique_order_number,
    amount = amount
    )
    new_record.save()
    flight_shedule.objects.filter(flight_id=Flight_id).update(tickets_number=F('tickets_number') - 1*amount)


def buy_tour(request):
    if request.method == 'POST':
        message ={}
        tour_name = request.POST.get('tour_name')
        number_of_people = request.POST.get('quantity')
        tour_id = TourDescription.objects.filter(name=tour_name).values_list('tour_number_id', flat=True)[0]
        uniq_numb = generate_unique_tour_number()
        tour_price = 0
        for i in range(int(number_of_people)):
            tour_price+=buying_tickets_by_order_tour(datetime.date.today(), tour_id, uniq_numb)
        print(tour_price)
        new_record = tour_booking_history(
            tour_id=tour_id,
            number_people=number_of_people,
            action='покупка',
            amount=tour_price+10000,
            tour_order_number_id=uniq_numb
        )
        new_record.save()

        message = f"Тур {tour_name} куплен. Количество: {number_of_people}, уникальный номер: {uniq_numb}"
        return JsonResponse({'success': True, 'message': message})
    else:
        return JsonResponse({'success': False, 'error': 'Метод запроса должен быть POST'})

def tour(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('city_name_textbox', '')
        date_pickerW = request.POST.get('datePickerWith', None)
        date_pickerB = request.POST.get('datePickerBefore', None)
        DayDifference = 0
        if date_pickerW:
            start_date = date_pickerW.split('-')
            date_start_value = datetime.date(*map(int, start_date))
        else:
            pass
        if date_pickerB:
            end_date = date_pickerB.split('-')
            date_end_value = datetime.date(*map(int, end_date))
            auto_populate_actual_schedule(date_end_value)
        else:
            pass
        if date_pickerB and date_pickerW:
            DayDifference = (date_end_value - date_start_value).days
        city_id = City.get_city_id_by_name(name)
        tours_id = flights_in_tours.get_tours_id_by_city_id(city_id)
        tours_days = {}
        for tour_id in tours_id:
            flights = flights_in_tours.objects.filter(Tour_number_id=tour_id)
            NumbOfDays = flights.values_list('Day_number_in_city', flat=True)
            sum_of_days = sum(map(int, NumbOfDays))
            if(sum_of_days<DayDifference):
                first_WFS_id = connect_tours_wfs.objects.filter(tour_number_id=tour_id).order_by('number').first().WFS_id
                first_date_flight = flight_shedule.objects.filter(WFS_id=first_WFS_id).annotate(date_difference=Func(F('date') - date_start_value, function='ABS')).order_by('date_difference').first().date
                if(abs((date_start_value - first_date_flight).days)+sum_of_days <= DayDifference):
                    tours_days[tour_id] = sum_of_days


        if len(tours_days) == 1:
            single_tour_id = list(tours_days.keys())[0]
            context['data'] = [{
                'tourname': TourDescription.objects.get(tour_number_id=single_tour_id).name,
                'tourprice': TourDescription.objects.get(tour_number_id=single_tour_id).price,
                'tourdescription': TourDescription.objects.get(tour_number_id=single_tour_id).description,
                'image_url': TourDescription.objects.get(tour_number_id=single_tour_id).image_url
            }]
        else:
            # Создание списка context['data'] и добавление информации о каждом туре
            context['data'] = []
            for key in tours_days:
                context['data'].append({
                    'tourname': TourDescription.get_tour_name_by_tour_id(key)[0],
                    'tourprice': TourDescription.get_tour_price_by_tour_id(key)[0],
                    'tourdescription': TourDescription.get_tour_description_by_tour_id(key)[0],
                    'image_url': TourDescription.get_tour_image_number_by_tour_id(key)
                })

    return render(request, 'tour.html', context)

def generate_unique_flight_number():
    while True:
        flight_number = random.randint(100000, 999999)
        if not flight_shedule.objects.filter(flight_number = flight_number).exists():
            return flight_number
def auto_populate_actual_schedule(end_date):
    weekdays_dict = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }
    weekly_schedule = WeeklyFlightSchedule.objects.all()
    latest_flight = flight_shedule.objects.order_by('date').last()
    CurrentLastDateInFlightShedule = latest_flight.date if latest_flight else datetime.date.today()
    while CurrentLastDateInFlightShedule <= end_date:
        if not flight_shedule.objects.filter(date=CurrentLastDateInFlightShedule).exists():
            CurrentRecordForWeekday = weekly_schedule.filter(
                week_day=weekdays_dict[CurrentLastDateInFlightShedule.weekday()])
            for record in CurrentRecordForWeekday:
                new_record = flight_shedule(
                    date=CurrentLastDateInFlightShedule,
                    tickets_number= aircraft.objects.filter(aircraft_id=record.aircraft_id).values_list('seats_number', flat=True).first(),
                    WFS_id=record.WFS_id,
                    flight_number=generate_unique_flight_number()
                )
                new_record.save()
        CurrentLastDateInFlightShedule += datetime.timedelta(days=1)
def search(request):
    context = {}
    if request.method == 'POST':
        city_from = request.POST.get('city_from', '')
        city_to = request.POST.get('city_to', '')
        date = request.POST.get('date_departure', '')
        F_city = City.objects.get(Name_city = city_to).City_id
        S_city = City.objects.get(Name_city = city_from).City_id
        Flight_info = WeeklyFlightSchedule.objects.filter(departure_city_id = F_city , arrival_city_id= S_city)
        flight_id = list(Flight_info.values_list('WFS_id', flat=True))
        flight = flight_shedule.objects.filter(date = date).filter(WFS_id = flight_id[0]).values_list('flight_id')
        tickets_number = flight_shedule.objects.filter(date = date).filter(WFS_id = flight_id[0]).values_list('tickets_number')
        price = Flight_info.values_list('price', flat=True)
        time = list(Flight_info.values_list('time', flat=True))
        flight_duration = list(Flight_info.values_list('flight_duration', flat = True))
        aircraft_id = list(Flight_info.values_list('aircraft_id', flat=True))
        aircraft_name = list(aircraft.objects.filter(aircraft_id=aircraft_id[0]).values_list('name', flat=True))
        airline_id = list(Flight_info.values_list('airline_id', flat=True))
        airline_name = list(airline.objects.filter(airlines_id=airline_id[0]).values_list('airlines', flat=True))
        print(list(flight)[0][0])
        print(airline_name[0])
        context['data'] = [{
            'city_from': city_from,
            'city_to': city_to,
            'date': date,
            'time': time[0],
            'flight_duration': flight_duration[0],
            'price': price[0],
            'tickets_number': tickets_number[0][0],
            'aircraft': aircraft_name[0],
            'airline': airline_name[0],
            'flight_number': list(flight)[0][0]
        }]
    return render(request, 'search.html', context)

def buy_ticket(request):
    if request.method == 'POST':
        flight_number = request.POST.get('Ticket_number')
        number_of_people = request.POST.get('quantity')
        price = request.POST.get('price')
        unique_number = generate_unique_ticket_number()
        filing_history_operations(0, flight_number[14:], price[6:], 'покупка', unique_number, number_of_people)

        message = f"Билет {flight_number} куплен. Количество: {number_of_people}, уникальный номер: {unique_number}"

        return JsonResponse({'success': True, 'message': message})
    else:
        return JsonResponse({'success': False, 'error': 'Метод запроса должен быть POST'})

def refund(request):
    return render(request, 'refund.html')

def refund_action(request):
    if request.method == 'POST':
        message={}
        unique_number = request.POST.get('unique_number')
        Note = History.objects.filter(unique_order_number = unique_number).values_list()
        if Note.exists():
            Note = list(Note)
            if (Note[0][0]>=1):
                    tour_refaund_id = generate_unique_ticket_number()
                    flight_date = Note[0][1]
                    current_date = datetime.date.today()
                    date_string = current_date.strftime("%Y-%m-%d")
                    if (flight_date == date_string):
                        for Not in Note[1:]:
                            new_record = History(
                                Tour_id=Not[0],
                                Flight_id=Not[1],
                                date=datetime.datetime.now(),
                                price=int(Not[3])/2,
                                Action='возврат со скидкой',
                                unique_order_number=tour_refaund_id,
                                amount=Not[5]
                            )
                            new_record.save()
                            new_record2 = tour_booking_history(
                                tour_id=Not[0],
                                number_people=1,
                                action='возврат со скидкой',
                                amount=int(Not[3])/4,
                                tour_order_number_id=tour_refaund_id
                            )
                            new_record2.save()

                    else:
                        for Not in Note[1:]:
                            new_record = History(
                                Tour_id=Not[0],
                                Flight_id=Not[1],
                                date=datetime.datetime.now(),
                                price=Not[3],
                                Action='возврат',
                                unique_order_number=tour_refaund_id,
                                amount=Not[5]
                            )
                            new_record.save()
                            new_record2 = tour_booking_history(
                                tour_id=Not[0],
                                number_people=1,
                                action='возврат',
                                amount=int(Not[3]),
                                tour_order_number_id=tour_refaund_id
                            )
                            new_record2.save()


            else:
                new_record = History(
                    Tour_id=Note[0][0],
                    Flight_id=Note[0][1],
                    date=datetime.datetime.now(),
                    price=Note[0][3],
                    Action='возврат',
                    unique_order_number=generate_unique_ticket_number(),
                    amount=Note[0][7]
                )
                new_record.save()




        return render(request, 'refund.html')

def statistic(request):
    context = {}
    if request.method == 'POST':
        airline_name = request.POST.get('airline_name_textbox', '')
        if(len(airline_name)!= 0):
            turnover = 0
            income = 0
            number_of_flights = 0
            airline_id = airline.objects.filter(airlines = airline_name).first().airlines_id
            wfs_ides = WeeklyFlightSchedule.objects.filter(airline_id = airline_id).values_list('WFS_id')
            for id in wfs_ides:
                flights_id = list(flight_shedule.objects.filter(WFS_id = id[0]).values_list('flight_number'))
                for ides in flights_id:
                    for i in ides:
                        amount = list(History.objects.filter(Flight_id=i).values_list('amount'))
                        price = list(History.objects.filter(Flight_id=i).values_list('price'))
                        action = list(History.objects.filter(Flight_id = i).values_list('Action'))
                        if(len(price)!=0):
                            for act in range(len(action)):
                                if(action[act][0] == 'покупка'):
                                    income+= int(price[act][0])*int(amount[act][0])
                                    turnover+=int(price[act][0])*int(amount[act][0])
                                else:
                                    income-= int(price[act][0])*int(amount[act][0])
                                number_of_flights += 1
            context['data'] = [{
                'income': income,
                'order': number_of_flights,
                'turnover' : turnover
            }]
        else:
            income = 0
            order = 0
            turnover = 0
            objects = tour_booking_history.objects.all()

            for obj in objects:
                order+=1
                #cur = int(obj.amount) * int(obj.number_people)
                cur = 10000 * int(obj.number_people)

                if obj.action == 'покупка':
                    turnover+=cur
                    income += cur
                elif obj.action == 'возврат со скидкой':
                    income -= (int(obj.amount) * int(obj.number_people))/4
                else:
                    income -= cur
            context['data'] = [{
                'income': income,
                'order': order,
                'turnover': turnover
            }]

    return render(request, 'statistic.html', context)