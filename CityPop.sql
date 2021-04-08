create database if not exists cities;

use cities;

create table `city_population` (
  `city` varchar(255) DEFAULT NULL,
  `population` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

insert into
	city_population(city, population)
values
('Москва', 12615279),
('Санкт-Петербург', 5383890),
('Новосибирск', 1618039),
('Екатеринбург', 1483119),
('Казань', 1251969),
('Нижний Новгород', 1253511),
('Челябинск', 1200719),
('Самара', 1156608),
('Омск', 1164815),
('Ростов-на-Дону', 1133307),
('Уфа', 1124226),
('Красноярск', 1095286),
('Воронеж', 1054111),
('Пермь', 1053934),
('Волгоград', 1013468);
    
select city from city_population where population = (select MIN(population) from city_population);