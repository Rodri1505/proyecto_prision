DROP TABLE IF EXISTS EMPLEADO;
DROP TABLE IF EXISTS PRESO;
DROP TABLE IF EXISTS DELITO;
DROP TABLE IF EXISTS PABELLON;
DROP TABLE IF EXISTS BLOQUE;

CREATE TABLE BLOQUE (
    id_bloque INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(10) NOT NULL,
    descripcion VARCHAR(100)
);

INSERT INTO BLOQUE (nombre, descripcion) VALUES
('A', 'Bloque principal de alta seguridad'),
('B', 'Bloque de presos comunes'),
('C', 'Bloque de aislamiento');

CREATE TABLE PABELLON (
    id_pabellon INT AUTO_INCREMENT PRIMARY KEY,
    id_bloque INT NOT NULL,
    nombre VARCHAR(20) NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    capacidad INT NOT NULL,
    FOREIGN KEY (id_bloque) REFERENCES BLOQUE(id_bloque)
);

INSERT INTO PABELLON (id_bloque, nombre, tipo, capacidad) VALUES
(1, 'A1', 'alta seguridad', 30),
(1, 'A2', 'alta seguridad', 25),
(2, 'B1', 'comunes', 40),
(2, 'B2', 'comunes', 35),
(3, 'C1', 'aislamiento', 10);

CREATE TABLE DELITO (
    id_delito INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    gravedad ENUM('leve','grave','muy grave') NOT NULL
);

INSERT INTO DELITO (nombre, descripcion, gravedad) VALUES
('Robo con violencia', 'Uso de fuerza física durante el robo', 'grave'),
('Tráfico de drogas', 'Distribución de sustancias ilegales', 'grave'),
('Homicidio', 'Quitar la vida a otra persona', 'muy grave'),
('Fraude financiero', 'Manipulación económica', 'leve'),
('Agresión', 'Ataque físico a otra persona', 'grave');

CREATE TABLE PRESO (
    id_preso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_salida_prev DATE,
    id_pabellon INT NOT NULL,
    id_delito INT NOT NULL,
    observaciones TEXT,
    FOREIGN KEY (id_pabellon) REFERENCES PABELLON(id_pabellon),
    FOREIGN KEY (id_delito) REFERENCES DELITO(id_delito)
);

INSERT INTO PRESO 
(nombre, apellidos, dni, fecha_nacimiento, fecha_ingreso, fecha_salida_prev, id_pabellon, id_delito, observaciones)
VALUES
('Juan', 'García López', '12345678A', '1985-04-10', '2023-01-15', '2030-01-15', 1, 3, 'En observación psicológica'),
('Carlos', 'Martínez Ruiz', '23456789B', '1990-07-20', '2022-06-12', NULL, 3, 1, 'Buen comportamiento'),
('Luis', 'Fernández Soto', '34567890C', '1982-11-30', '2021-09-25', '2027-09-25', 2, 2, NULL),
('Miguel', 'Pérez Gómez', '45678901D', '1995-01-17', '2024-02-10', NULL, 5, 5, 'Aislamiento temporal'),
('Roberto', 'Lozano Díaz', '56789012E', '1978-05-05', '2018-03-01', '2035-03-01', 4, 4, 'Participa en talleres educativos');

CREATE TABLE EMPLEADO (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    puesto VARCHAR(50) NOT NULL,
    fecha_contratacion DATE NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    id_bloque INT,
    FOREIGN KEY (id_bloque) REFERENCES BLOQUE(id_bloque)
);

INSERT INTO EMPLEADO 
(nombre, apellidos, dni, puesto, fecha_contratacion, salario, id_bloque)
VALUES
('Ana', 'López Romero', '77889900X', 'directora', '2015-05-10', 3200.00, 1),
('Pedro', 'Sánchez Ruiz', '88990011Y', 'funcionario', '2018-09-12', 2100.00, 1),
('María', 'Gómez Torres', '99001122Z', 'médico', '2020-01-20', 2800.00, 2),
('Jorge', 'Díaz Moreno', '11223344W', 'seguridad', '2017-04-05', 1900.00, 3),
('Lucía', 'Ramírez Cruz', '22334455V', 'psicóloga', '2021-11-15', 2600.00, 1);


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

