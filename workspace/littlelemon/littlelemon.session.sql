CREATE DATABASE IF NOT EXISTS littlelemon;
USE littlelemon;

CREATE TABLE IF NOT EXISTS Menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slug VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    inventory INT NOT NULL
);

INSERT INTO restaurant_menu (slug, title, price, inventory, category_fk_id) VALUES
('greek-salad', 'Greek Salad', 8.99, 50, 1),
('hummus', 'Hummus', 5.99, 100, 2),
('falafel', 'Falafel', 7.99, 80, 1 ),
('shawarma', 'Shawarma', 9.99, 60, 1),
('baklava', 'Baklava', 4.99, 40, 3),
('tabbouleh', 'Tabbouleh', 6.99, 70, 2),
('baba-ganoush', 'Baba Ganoush', 5.49, 90, 1),
('tzatziki', 'Tzatziki', 4.49, 110, 2),
('dolma', 'Dolma', 6.49, 65, 2),
('spanakopita', 'Spanakopita', 7.49, 55, 2),
('moussaka', 'Moussaka', 10.99, 45, 1),
('kebab', 'Kebab', 11.99, 50, 2),
('souvlaki', 'Souvlaki', 12.99, 60, 2),
('gyro', 'Gyro', 9.49, 75, 1),
('baklava-ice-cream', 'Baklava Ice Cream', 5.99, 30, 3),
('pita-bread', 'Pita Bread', 2.99, 120, 2),
('feta-cheese', 'Feta Cheese', 3.99, 100, 2),
('olives', 'Olives', 4.99, 80, 2),
('stuffed-peppers', 'Stuffed Peppers', 8.49, 70, 1),
('grilled-vegetables', 'Grilled Vegetables', 7.99, 90, 1);


INSERT INTO restaurant_menu (slug, title, price, inventory, category_fk_id) VALUES
('lemonade', 'Lemonade', 3.99, 100, 4),
('iced-tea', 'Iced Tea', 2.99, 120, 4),
('sparkling-water', 'Sparkling Water', 1.99, 150, 4),
('orange-juice', 'Orange Juice', 4.49, 80, 4),
('mint-lemonade', 'Mint Lemonade', 3.49, 90, 4)
('soda', 'Soda', 1.99, 110, 4),
('iced-coffee', 'Iced Coffee', 3.99, 100, 4),
('hot-tea', 'Hot Tea', 2.49, 120, 4),
('espresso', 'Espresso', 2.99, 80, 4),
('cappuccino', 'Cappuccino', 3.49, 70, 4),
('latte', 'Latte', 3.99, 60, 4),
('mocha', 'Mocha', 4.49, 50, 4),
('macchiato', 'Macchiato', 4.99, 40, 4),
('americano', 'Americano', 3.99, 30, 4),
('cortado', 'Cortado', 4.49, 20, 4),
('flat-white', 'Flat White', 4.99, 10, 4),
('chai-latte', 'Chai Latte', 3.99, 5, 4),
('turkish-coffee', 'Turkish Coffee', 4.49, 3, 4),
('affogato', 'Affogato', 4.99, 2, 4);

INSERT INTO restaurant_menu (slug, title, price, inventory, category_fk_id) VALUES
('beer', 'Beer', 5.99, 100, 5),
('wine-red', 'Red Wine', 8.99, 50, 5),
('wine-white', 'White Wine', 8.99, 50, 5),
('whiskey', 'Whiskey', 12.99, 30, 5),
('vodka', 'Vodka', 11.99, 40, 5),
('rum', 'Rum', 10.99, 35, 5),
('gin', 'Gin', 9.99, 45, 5),
('tequila', 'Tequila', 13.99, 25, 5),
('cocktail-margarita', 'Margarita', 7.99, 60, 5),
('cocktail-mojito', 'Mojito', 7.99, 60, 5);