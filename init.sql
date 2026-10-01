-- init.sql
CREATE TABLE IF NOT EXISTS productos (
    id VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);

-- Opcional: Insertar algunos datos de ejemplo para probar
INSERT INTO productos (id, nombre, descripcion, categoria, precio) VALUES
('P001', 'Laptop Gamer', 'Potente laptop para juegos', 'Laptops',1500.00),
('P002', 'Teclado Mecánico', 'Teclado RGB con switches azules', 'Periferico',80.50),
('P003', 'Mouse Inalámbrico', 'Mouse ergonómico para oficina', 'Periferico',35.00)
ON CONFLICT (id) DO NOTHING;