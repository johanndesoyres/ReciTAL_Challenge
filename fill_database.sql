DELETE FROM properties;
VACUUM;
DELETE FROM users;
VACUUM;

-- Fill Users table

INSERT INTO users
("id", "full_name", "age", "gender", "email", "phone", "salary", "job")
VALUES (1, 'Pierre Dumont', 35, 'M', 'pierre.dumont@gmail.com', '0687856575', 2000, 'serveur');

INSERT INTO users
("id", "full_name", "age", "gender", "email", "phone", "salary", "job")
VALUES (2, 'Lucas Parac', 22, 'M', 'lucas.parac@gmail.com', '0656789663', NULL, NULL);

INSERT INTO users
("id", "full_name", "age", "gender", "email", "phone", "salary", "job")
VALUES (3, 'Sophie Pressieux', 40, 'F', 'sophie.pressieux@hotmail.fr', '0789565472', 6000, 'chef de projet');


-- Fill Properties table

INSERT INTO properties
("id", "adress", "city", "surface", "rooms", "is_home", "is_flat", "age", "selling_price", "sale_date", "is_sold", "rental_price", "rental_start_date", "is_rented", "availability_date", "is_available", "owner_id")
VALUES (1, '39 boulevard Saint Martin', 'Paris', 60.0, 2, False, True, 60, 250000, NULL, False, 1500, '2019-10-16', True, NULL, False, 1);

INSERT INTO properties
("id", "adress", "city", "surface", "rooms", "is_home", "is_flat", "age", "selling_price", "sale_date", "is_sold", "rental_price", "rental_start_date", "is_rented", "availability_date", "is_available", "owner_id")
VALUES (2, '8 rue Marguerite', 'Paris', 40, 2, False, True, 60, 200000, '2020-01-13', True, 1000, NULL, False, NULL, False, 3);

INSERT INTO properties
("id", "adress", "city", "surface", "rooms", "is_home", "is_flat", "age", "selling_price", "sale_date", "is_sold", "rental_price", "rental_start_date", "is_rented", "availability_date", "is_available", "owner_id")
VALUES (3, '20 rue Charles Pathé', 'Vincennes', 70, 2, False, True, 80, 270000, '2020-06-22', True, 1000, NULL, False, NULL, False, 3);

INSERT INTO properties
("id", "adress", "city", "surface", "rooms", "is_home", "is_flat", "age", "selling_price", "sale_date", "is_sold", "rental_price", "rental_start_date", "is_rented", "availability_date", "is_available", "owner_id")
VALUES (4, '3 avenue de l''europe', 'Montreuil', 150, 3, True, False, 70, 400000, NULL, False, NULL, NULL, False, '2020-10-25', True, NULL);