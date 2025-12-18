CREATE DATABASE IF NOT EXISTS prision_db;
USE prision_db;

CREATE TABLE BLOQUE (
    id_bloque INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE PABELLON (
    id_pabellon INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_bloque INT NOT NULL,
    FOREIGN KEY (id_bloque) REFERENCES BLOQUE(id_bloque)
);

CREATE TABLE DELITO (
    id_delito INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE PRESO (
    id_preso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni VARCHAR(15) NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_salida_prev DATE,
    id_pabellon INT NOT NULL,
    id_delito INT NOT NULL,
    observaciones TEXT,

    FOREIGN KEY (id_pabellon) REFERENCES PABELLON(id_pabellon),
    FOREIGN KEY (id_delito) REFERENCES DELITO(id_delito)
);

INSERT INTO BLOQUE (nombre) VALUES
('Bloque A'),
('Bloque B');

INSERT INTO PABELLON (nombre, id_bloque) VALUES
('Pabellón 1', 1),
('Pabellón 2', 1),
('Pabellón 3', 2),
('Pabellón 4', 2),
('Pabellón 5', 2);

INSERT INTO DELITO (nombre) VALUES
('Robo'),
('Fraude'),
('Homicidio'),
('Estafa'),
('Lesiones');


CREATE ROLE IF NOT EXISTS 'admin_role';
CREATE ROLE IF NOT EXISTS 'editor_role';
CREATE ROLE IF NOT EXISTS 'viewer_role';
GRANT ALL PRIVILEGES ON prision_db.* TO 'admin_role';
GRANT SELECT, INSERT, UPDATE ON prision_db.* TO 'editor_role';
GRANT SELECT ON prision_db.* TO 'viewer_role';
CREATE USER IF NOT EXISTS 'admin_prision'@'localhost' IDENTIFIED BY 'admin123';
CREATE USER IF NOT EXISTS 'editor_prision'@'localhost' IDENTIFIED BY 'editor123';
CREATE USER IF NOT EXISTS 'viewer_prision'@'localhost' IDENTIFIED BY 'viewer123';
GRANT 'admin_role' TO 'admin_prision'@'localhost';
GRANT 'editor_role' TO 'editor_prision'@'localhost';
GRANT 'viewer_role' TO 'viewer_prision'@'localhost';
SET DEFAULT ROLE 'admin_role' TO 'admin_prision'@'localhost';
SET DEFAULT ROLE 'editor_role' TO 'editor_prision'@'localhost';
SET DEFAULT ROLE 'viewer_role' TO 'viewer_prision'@'localhost';
CREATE USER IF NOT EXISTS 'prision_user'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON prision_db.* TO 'prision_user'@'localhost';
FLUSH PRIVILEGES;

