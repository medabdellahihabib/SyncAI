CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT now()
);

INSERT INTO products(name, description) VALUES
('MacBook Pro', 'Apple laptop 2021'),
('ThinkPad', 'Lenovo  laptop');
