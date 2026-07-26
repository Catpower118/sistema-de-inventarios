# Sistema de Inventario

Aplicación de gestión de inventarios desarrollada con **Python**, **Flet** y **MySQL**. Implementa operaciones CRUD completas (Create, Read, Update, Delete) con una interfaz gráfica moderna e intuitiva.

## Características

- Interfaz gráfica moderna y responsiva con **Flet**
- Registro, edición y eliminación de productos
- Validación de entradas en tiempo real
- Tabla interactiva con colores personalizables
- Gestión de movimientos de entrada y salida de stock
- Triggers automáticos para actualización de inventario
- Arquitectura modular y escalable

## Requisitos

- Python 3.10+
- MySQL 8.0+
- [Flet](https://flet.dev/)
- mysql-connector-python

## Instalación

```bash
git clone https://github.com/Catpower118/sistema-de-inventarios.git
cd sistema-de-inventarios
pip install -r requirements.txt
```

## Configuración de MySQL

### 1. Crear la base de datos

```sql
CREATE DATABASE inventario;
USE inventario;
```

### 2. Crear las tablas

```sql
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    cantidad INT NOT NULL,
    stock INT NOT NULL CHECK (stock >= 0)
);

CREATE TABLE movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    tipo ENUM('entrada', 'salida') NOT NULL,
    cantidad INT UNSIGNED NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
```

### 3. Crear los triggers

```sql
DELIMITER $$

CREATE TRIGGER trg_salida
AFTER INSERT ON movimientos
FOR EACH ROW
BEGIN
    IF NEW.tipo = 'salida' THEN
        UPDATE productos
        SET stock = stock - NEW.cantidad
        WHERE id = NEW.producto_id;
    END IF;
END$$

DELIMITER ;

CREATE TRIGGER trg_entrada
AFTER INSERT ON movimientos
FOR EACH ROW
BEGIN
    IF NEW.tipo = 'entrada' THEN
        UPDATE productos
        SET stock = stock + NEW.cantidad
        WHERE id = NEW.producto_id;
    END IF;
END$$

DELIMITER ;
```

## Ejecución

```bash
python inventario_2.py
```

## Licencia

[MIT License](LICENSE)