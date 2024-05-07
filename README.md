Первоначальное задание

Имеется сеть городов (1 город – 1 аэропорт). Имеется набор авиакомпаний. Для каждой авиакомпании: список самолетов и список рейсов (рейс - «город-город»).
Рейс: тип самолета, дни недели и время вылета, время в пути, стоимость билета (включая наценку туроператора; наценка для туроператора – постоянная величина.), период актуальности рейса. Известно количество посадочных мест в самолете.

Требуется:

•	Поддержка возможности заказать тур (множество связанных рейсов). Заказанный тур считается сразу оплаченным. Туры могут быть для одного человека, а также для групп.

•	Поддержка справочника пассажира: по дате и направлению получить список рейсов с указанием количества свободных мест; по названию города и указанию периода времени определить, какие туры туда попадают;

•	Фин. отчет (годовой) для любой авиакомпании и для туроператора. 

•	Поддержка возможности возврата тура (при возврате в день вылета производится удержание 50% стоимости билета; удержанная сумма делится пополам между туроператором и авиакомпанией).


Составим схему нашей будущей базы данных

![Схема таблиц](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/schema.jpg)

Переносим таблицы в MySQL Workbench и запускаем локальный сервер, через который будем работать, подключаем его через настройки.

![aircraft](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/aircraft.jpg)
![airlines](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/airlines.jpg)
![cities](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/cities.jpg)
![connect_airlines_aircraft](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/connect_airlines_aircraft.jpg)
![connect_tours_wfs](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/connect_tours_wfs.jpg)
![flight_in_tours](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/flight_in_tours.jpg)
![flight_schedule](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/flight_schedule.jpg)
![history](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/history.jpg)
![tour_booking_history](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/tour_booking_history.jpg)
![weekly_flight_schedule](https://raw.githubusercontent.com/PureEev/Touroperator_site/main/weekly_flight_schedule.jpg)

