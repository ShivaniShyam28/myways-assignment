cde = ["""
Do $$ DECLARE
  r RECORD;
BEGIN
  FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
    raise notice 'droping table: %', r.tablename;
    EXECUTE 'DROP TABLE ' || quote_ident(r.tablename) || ' CASCADE';
  END LOOP;
END $$;
""",
"""
CREATE TABLE hospitals (
    hospital_id BIGSERIAL PRIMARY KEY,
    hospital_name character varying NOT NULL DEFAULT ''::character varying,
    hospital_details character varying NOT NULL DEFAULT ''::character varying,
    capacity bigint,
    is_covid_dedicated boolean NOT NULL DEFAULT true
);
""",
"""
CREATE TABLE severitites (
    severity_id BIGSERIAL PRIMARY KEY,
    severity_index character varying NOT NULL DEFAULT ''::character varying
);
""",
"""
CREATE TABLE health_index (
    health_id BIGSERIAL PRIMARY KEY,
    health_desc character varying NOT NULL DEFAULT ''::character varying
);
""",
"""
CREATE TABLE patients (
    patient_id BIGSERIAL PRIMARY KEY,
    patient_name character varying NOT NULL DEFAULT ''::character varying,
    age bigint NOT NULL DEFAULT 1,
    health_id bigint NOT NULL REFERENCES health_index(health_id),
    is_admitted_to_hospital boolean NOT NULL DEFAULT false,
    is_discharged_from_hospital boolean NOT NULL DEFAULT false,
    is_alive boolean DEFAULT true
);
""",
"""
CREATE TABLE hospital_items (
    hospital_equipment_id BIGSERIAL PRIMARY KEY,
    hospital_id bigint NOT NULL REFERENCES hospitals(hospital_id),
    equiment_name character varying NOT NULL DEFAULT ''::character varying,
    quality character varying NOT NULL DEFAULT ''::character varying,
    quantity numeric(5,2)
);
""",
"""
CREATE TABLE patient_hospitals (
    patient_hospital_id BIGSERIAL PRIMARY KEY,
    patient_id bigint NOT NULL REFERENCES patients(patient_id),
    hospital_id bigint NOT NULL REFERENCES hospitals(hospital_id),
    severity_id bigint NOT NULL REFERENCES severitites(severity_id),
    cost_to_patient numeric(10,3),
    admitted_health_id bigint NOT NULL REFERENCES health_index(health_id),
    discharged_health_id bigint REFERENCES health_index(health_id),
    admitted_date timestamp without time zone NOT NULL DEFAULT CURRENT_DATE,
    discharge_date timestamp without time zone
);
""",
"""
CREATE VIEW patient_hospital_details AS  SELECT a.patient_hospital_id,
    a.patient_id,
    b.patient_name,
    a.hospital_id,
    c.hospital_name,
    a.cost_to_patient,
    a.admitted_date,
    a.discharge_date
   FROM patient_hospitals a
     JOIN patients b ON a.patient_id = b.patient_id
     JOIN hospitals c ON a.hospital_id = c.hospital_id;
""",
"""
INSERT INTO "public"."health_index"("health_id","health_desc")
VALUES
(1,E'EXCELLENT'),
(2,E'GOOD'),
(3,E'HIGH MODERATE'),
(4,E'MODERATE'),
(5,E'LOW MODERATE'),
(6,E'LOW'),
(7,E'WORST'),
(8,E'DEAD');
""",
"""
INSERT INTO "public"."hospitals"("hospital_id","hospital_name","hospital_details","capacity","is_covid_dedicated")
VALUES
(1,E'JSS',E'ICU Dedicated',12000,TRUE),
(2,E'Adithya Hospital',E'For Mild Covid',2453,TRUE),
(3,E'Vidyaranya Hospital',E'Accessible to all',1543,TRUE),
(4,E'Narayana Hospital',E'For Sugar patients Only',433,TRUE),
(5,E'Appolo BGS',E'Accessible to all',5465,TRUE),
(6,E'Anarjana',E'Accessible to all',1023,TRUE),
(7,E'MVJAS Hospital',E'Accessible to all',435,TRUE),
(8,E'ACAS Hospital',E'For Sugar patients Only',566,TRUE);
""",
"""
INSERT INTO "public"."hospital_items"("hospital_equipment_id","hospital_id","equiment_name","quality","quantity")
VALUES
(1,1,E'Ventilators',E'Good',412),
(2,1,E'ICU Wards',E'Excellent',300),
(4,1,E'Oxygen Cylinders',E'Big',860),
(5,1,E'Remdesiver',E'Injection',222),
(6,2,E'Ventilators',E'Good',34),
(7,2,E'ICU Wards',E'Excellent',53),
(8,2,E'Oxygen Cylinders',E'Big',42),
(9,2,E'Remdesiver',E'Injection',34),
(10,3,E'Ventilators',E'Good',75),
(11,3,E'ICU Wards',E'Excellent',344),
(12,3,E'Oxygen Cylinders',E'Big',123),
(13,3,E'Remdesiver',E'Injection',123),
(14,4,E'Ventilators',E'Good',43),
(15,4,E'ICU Wards',E'Excellent',454),
(16,4,E'Oxygen Cylinders',E'Big',667),
(17,4,E'Remdesiver',E'Injection',98),
(18,5,E'Ventilators',E'Good',34),
(19,5,E'ICU Wards',E'Excellent',12),
(20,5,E'Oxygen Cylinders',E'Big',32),
(21,5,E'Remdesiver',E'Injection',54);
""",
"""
INSERT INTO "public"."patients"("patient_id","patient_name","age","health_id","is_admitted_to_hospital","is_discharged_from_hospital","is_alive")
VALUES
(1,E'Manthan',22,4,FALSE,FALSE,TRUE),
(2,E'Shivani',22,1,FALSE,FALSE,TRUE),
(3,E'Sumnath',34,1,FALSE,FALSE,TRUE),
(4,E'Sanna',54,1,FALSE,FALSE,TRUE),
(5,E'Supreeth',65,1,FALSE,FALSE,TRUE),
(6,E'Adithya',25,1,FALSE,FALSE,TRUE),
(7,E'Arun',29,1,FALSE,FALSE,TRUE),
(8,E'Prajwal',75,1,FALSE,FALSE,TRUE),
(9,E'Virat',46,1,FALSE,FALSE,TRUE),
(10,E'Kevin',38,1,FALSE,FALSE,TRUE),
(11,E'Maxwell',67,1,FALSE,FALSE,TRUE),
(12,E'Siraj',54,1,FALSE,FALSE,TRUE),
(13,E'Saini',33,1,FALSE,FALSE,TRUE),
(14,E'Zampa',23,1,FALSE,FALSE,TRUE),
(15,E'Dhoni',26,1,FALSE,FALSE,TRUE),
(16,E'King',28,1,FALSE,FALSE,TRUE),
(17,E'Gayle',40,1,FALSE,FALSE,TRUE),
(18,E'Lobo',80,1,FALSE,FALSE,TRUE),
(19,E'Mosadek',62,1,FALSE,FALSE,TRUE),
(20,E'Ali',74,1,FALSE,FALSE,TRUE),
(21,E'Sammy',21,4,FALSE,FALSE,TRUE),
(22,E'Pooran',19,1,FALSE,FALSE,TRUE),
(23,E'Pavan',17,4,FALSE,FALSE,TRUE),
(24,E'Mohammad',22,1,FALSE,FALSE,TRUE),
(25,E'Manthan',22,4,FALSE,FALSE,TRUE),
(26,E'Shivani',22,1,FALSE,FALSE,TRUE),
(27,E'Sumnath',34,1,FALSE,FALSE,TRUE),
(28,E'Sanna',54,1,FALSE,FALSE,TRUE),
(29,E'Supreeth',65,1,FALSE,FALSE,TRUE),
(30,E'Adithya',25,1,FALSE,FALSE,TRUE),
(31,E'Arun',29,1,FALSE,FALSE,TRUE),
(32,E'Prajwal',75,1,FALSE,FALSE,TRUE),
(33,E'Virat',46,1,FALSE,FALSE,TRUE),
(34,E'Kevin',38,1,FALSE,FALSE,TRUE),
(35,E'Maxwell',67,1,FALSE,FALSE,TRUE),
(36,E'Siraj',54,1,FALSE,FALSE,TRUE),
(37,E'Saini',33,1,FALSE,FALSE,TRUE),
(38,E'Zampa',23,1,FALSE,FALSE,TRUE),
(39,E'Dhoni',26,1,FALSE,FALSE,TRUE),
(40,E'King',28,1,FALSE,FALSE,TRUE),
(41,E'Gayle',40,1,FALSE,FALSE,TRUE),
(42,E'Lobo',80,1,FALSE,FALSE,TRUE),
(43,E'Mosadek',62,1,FALSE,FALSE,TRUE),
(44,E'Ali',74,1,FALSE,FALSE,TRUE),
(45,E'Sammy',21,4,FALSE,FALSE,TRUE),
(46,E'Pooran',19,1,FALSE,FALSE,TRUE),
(47,E'Pavan',17,4,FALSE,FALSE,TRUE),
(48,E'Manthan',22,4,FALSE,FALSE,TRUE),
(49,E'Shivani',22,1,FALSE,FALSE,TRUE),
(50,E'Sumnath',34,1,FALSE,FALSE,TRUE),
(51,E'Sanna',54,1,FALSE,FALSE,TRUE),
(52,E'Supreeth',65,1,FALSE,FALSE,TRUE),
(53,E'Adithya',25,1,FALSE,FALSE,TRUE),
(54,E'Arun',29,1,FALSE,FALSE,TRUE),
(55,E'Prajwal',75,1,FALSE,FALSE,TRUE),
(56,E'Virat',46,1,FALSE,FALSE,TRUE),
(57,E'Kevin',38,1,FALSE,FALSE,TRUE),
(58,E'Maxwell',67,1,FALSE,FALSE,TRUE),
(59,E'Siraj',54,1,FALSE,FALSE,TRUE),
(60,E'Saini',33,1,FALSE,FALSE,TRUE),
(61,E'Zampa',23,1,FALSE,FALSE,TRUE),
(62,E'Dhoni',26,1,FALSE,FALSE,TRUE),
(63,E'King',28,1,FALSE,FALSE,TRUE),
(64,E'Gayle',40,1,FALSE,FALSE,TRUE),
(65,E'Lobo',80,1,FALSE,FALSE,TRUE),
(66,E'Mosadek',62,1,FALSE,FALSE,TRUE),
(67,E'Ali',74,1,FALSE,FALSE,TRUE),
(68,E'Sammy',21,4,FALSE,FALSE,TRUE),
(69,E'Pooran',19,1,FALSE,FALSE,TRUE),
(70,E'Pavan',17,4,FALSE,FALSE,TRUE),
(71,E'Manthan',22,4,FALSE,FALSE,TRUE),
(72,E'Shivani',22,1,FALSE,FALSE,TRUE),
(73,E'Sumnath',34,1,FALSE,FALSE,TRUE),
(74,E'Sanna',54,1,FALSE,FALSE,TRUE),
(75,E'Supreeth',65,1,FALSE,FALSE,TRUE),
(76,E'Adithya',25,1,FALSE,FALSE,TRUE),
(77,E'Arun',29,1,FALSE,FALSE,TRUE),
(78,E'Prajwal',75,1,FALSE,FALSE,TRUE),
(79,E'Virat',46,1,FALSE,FALSE,TRUE),
(80,E'Kevin',38,1,FALSE,FALSE,TRUE),
(81,E'Maxwell',67,1,FALSE,FALSE,TRUE),
(82,E'Siraj',54,1,FALSE,FALSE,TRUE),
(83,E'Saini',33,1,FALSE,FALSE,TRUE),
(84,E'Zampa',23,1,FALSE,FALSE,TRUE),
(85,E'Dhoni',26,1,FALSE,FALSE,TRUE),
(86,E'King',28,1,FALSE,FALSE,TRUE),
(87,E'Gayle',40,1,FALSE,FALSE,TRUE),
(88,E'Lobo',80,1,FALSE,FALSE,TRUE),
(89,E'Mosadek',62,1,FALSE,FALSE,TRUE),
(90,E'Ali',74,1,FALSE,FALSE,TRUE),
(91,E'Sammy',21,4,FALSE,FALSE,TRUE),
(92,E'Pooran',19,1,FALSE,FALSE,TRUE),
(93,E'Pavan',17,4,FALSE,FALSE,TRUE);
""",
"""
INSERT INTO "public"."severitites"("severity_id","severity_index")
VALUES
(1,E'HIGH'),
(2,E'MODERATE'),
(3,E'LOW');
""",
"""
INSERT INTO "public"."patient_hospitals"("patient_hospital_id","patient_id","hospital_id","severity_id","cost_to_patient","admitted_health_id","discharged_health_id","admitted_date","discharge_date")
VALUES
(2,1,1,2,23532,4,NULL,E'2021-04-26 00:00:00',NULL),
(3,2,2,2,15343,4,2,E'2021-04-02 00:00:00',E'2021-04-04 00:00:00'),
(4,11,4,2,43564,4,2,E'2021-03-08 00:00:00',E'2021-03-12 00:00:00'),
(5,23,4,2,65000,4,3,E'2021-04-26 00:00:00',E'2021-04-28 00:00:00'),
(6,14,2,2,23400,4,1,E'2021-04-26 00:00:00',E'2021-04-30 00:00:00'),
(7,13,2,2,25000,4,NULL,E'2021-04-26 00:00:00',NULL),
(8,7,3,2,45680.34,4,3,E'2021-04-17 00:00:00',E'2021-04-20 00:00:00'),
(9,8,4,2,2454.65,4,NULL,E'2021-04-26 00:00:00',NULL),
(10,23,6,2,56324.4,4,NULL,E'2021-04-26 00:00:00',NULL),
(11,12,7,2,2345.68,4,NULL,E'2021-04-26 00:00:00',NULL),
(12,7,8,2,78999,4,NULL,E'2021-04-26 00:00:00',NULL),
(13,2,5,1,22234.34,7,NULL,E'2021-04-26 00:00:00',NULL),
(14,4,5,2,32123,4,NULL,E'2021-04-26 00:00:00',NULL),
(15,9,2,2,12000,4,NULL,E'2021-04-26 00:00:00',NULL),
(16,20,1,2,3000,4,NULL,E'2021-04-26 00:00:00',NULL),
(17,14,7,1,34333,6,NULL,E'2021-04-26 00:00:00',NULL),
(18,11,2,2,45666,4,NULL,E'2021-04-26 00:00:00',NULL),
(19,1,1,2,23532,4,NULL,E'2021-04-26 00:00:00',NULL),
(20,3,2,2,15343,4,2,E'2021-04-02 00:00:00',E'2021-04-04 00:00:00'),
(21,4,4,2,43564,4,2,E'2021-03-08 00:00:00',E'2021-03-12 00:00:00'),
(22,34,4,2,65000,4,3,E'2021-04-26 00:00:00',E'2021-04-28 00:00:00'),
(23,34,2,2,23400,4,1,E'2021-04-26 00:00:00',E'2021-04-30 00:00:00'),
(24,13,2,2,25000,4,NULL,E'2021-04-26 00:00:00',NULL),
(25,78,3,2,45680.34,4,3,E'2021-04-17 00:00:00',E'2021-04-20 00:00:00'),
(26,88,4,2,2454.65,4,NULL,E'2021-04-26 00:00:00',NULL),
(27,75,6,2,56324.4,4,NULL,E'2021-04-26 00:00:00',NULL),
(28,23,7,1,2345.68,7,NULL,E'2021-04-26 00:00:00',NULL),
(29,15,8,2,78999,4,NULL,E'2021-04-26 00:00:00',NULL),
(30,67,5,2,22234.34,4,NULL,E'2021-04-26 00:00:00',NULL),
(31,54,5,2,32123,4,NULL,E'2021-04-26 00:00:00',NULL),
(32,32,2,1,12000,5,NULL,E'2021-04-26 00:00:00',NULL),
(33,19,1,2,3000,4,NULL,E'2021-04-26 00:00:00',NULL),
(34,24,7,2,34333,4,NULL,E'2021-04-26 00:00:00',NULL),
(35,26,1,2,23532,4,NULL,E'2021-04-26 00:00:00',NULL),
(36,28,2,2,15343,5,2,E'2021-04-02 00:00:00',E'2021-04-04 00:00:00'),
(37,78,4,2,43564,4,2,E'2021-03-08 00:00:00',E'2021-03-12 00:00:00'),
(38,91,4,2,65000,4,3,E'2021-04-26 00:00:00',E'2021-04-28 00:00:00'),
(39,81,2,2,23400,4,1,E'2021-04-26 00:00:00',E'2021-04-30 00:00:00'),
(40,55,2,1,25000,6,NULL,E'2021-04-26 00:00:00',NULL),
(41,43,3,2,45680.34,4,3,E'2021-04-17 00:00:00',E'2021-04-20 00:00:00'),
(42,48,4,2,2454.65,4,NULL,E'2021-04-26 00:00:00',NULL),
(43,90,6,2,56324.4,4,NULL,E'2021-04-26 00:00:00',NULL),
(44,89,7,1,2345.68,7,NULL,E'2021-04-26 00:00:00',NULL),
(45,86,8,2,78999,4,NULL,E'2021-04-26 00:00:00',NULL);
"""]