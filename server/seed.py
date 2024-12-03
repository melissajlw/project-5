from config import app, db
from models.models import *

def seed_data():
    with app.app_context():

        print('Deleting existing products...')
        
        Product.query.delete()

        print('Creating products...')

        seller_id = 1  # Set the seller_id to 1 for all products

        phone1 = Product(name='iPhone 14 Prp', price=999, description='Apple iPhone 14 Pro, 128GB, Purple', image_url='https://i.pinimg.com/564x/46/4a/3c/464a3c2e8af440f769de8456976ffbc7.jpg', quantity_available=100, seller_id=seller_id)
        phone2 = Product(name='Samsung Galaxy S20', price=799, description='Samsung Galaxy S20, 128GB, Cosmic Gray', image_url='https://i.pinimg.com/564x/e8/b2/7d/e8b27df6b3f8f76c569c1715297672d2.jpg', quantity_available=80, seller_id=seller_id)
        phone3 = Product(name='Google Pixel 5', price=699, description='Google Pixel 7a, 128GB, Just Black', image_url='https://i.pinimg.com/564x/df/c7/24/dfc72427002660c11845df1c3e6cf43b.jpg', quantity_available=120, seller_id=seller_id)
        phone4 = Product(name='OnePlus 9 Pro', price=899, description='OnePlus 9 Pro, 256GB, Morning Mist', image_url='https://i.pinimg.com/564x/a2/c9/61/a2c9612d875b39b0d899598b67dc415d.jpg', quantity_available=90, seller_id=seller_id)

        laptop1 = Product(name='MacBook Pro', price=1799, description='Apple MacBook Pro, 13-inch, M1 chip, 256GB SSD', image_url='https://i.pinimg.com/736x/69/d5/44/69d544b42b46e696650e07ddef8bd28e.jpg', quantity_available=110, seller_id=seller_id)
        laptop2 = Product(name='Dell XPS 15', price=1499, description='Dell XPS 15 9500, Intel Core i7, 16GB RAM, 512GB SSD', image_url='https://i.pinimg.com/564x/e7/f8/01/e7f801cef4b945026ee53d3d8ebc3906.jpg', quantity_available=95, seller_id=seller_id)
        laptop3 = Product(name='HP Spectre x360', price=1299, description='HP Spectre x360, 13.3-inch 4K OLED, Intel Core i7, 512GB SSD', image_url='https://i.pinimg.com/564x/1a/c6/81/1ac681ab418ea8dfd00e37c3b2580fe1.jpg', quantity_available=125, seller_id=seller_id)
        laptop4 = Product(name='Lenovo ThinkPad X1 Carbon', price=1399, description='Lenovo ThinkPad X1 Carbon Gen 9, Intel Core i5, 256GB SSD', image_url='https://i.pinimg.com/564x/d7/10/f1/d710f17efbfcaa72651a2c6930c5e0ad.jpg', quantity_available=105, seller_id=seller_id)

        mouse1 = Product(name='Logitech MX Master 3', price=99, description='Logitech MX Master 3 Wireless Mouse, Advanced Ergonomic Design', image_url='https://i.pinimg.com/564x/b7/0d/e5/b70de54b530ad9fd214be295726a925e.jpg', quantity_available=45, seller_id=seller_id)
        mouse2 = Product(name='Razer DeathAdder V2', price=69, description='Razer DeathAdder V2 Gaming Mouse, 20K DPI Optical Sensor', image_url='https://i.pinimg.com/564x/ea/58/44/ea58445d3a95cec7c605b5f73fb2d624.jpg', quantity_available=30, seller_id=seller_id)
        mouse3 = Product(name='Microsoft Surface Precision Mouse', price=89, description='Microsoft Surface Precision Mouse, Bluetooth, Ergonomic Design', image_url='https://i.pinimg.com/736x/56/7d/bc/567dbc311ab4c56123acf7126827a0bf.jpg', quantity_available=50, seller_id=seller_id)
        mouse4 = Product(name='Corsair Dark Core RGB Pro SE', price=79, description='Corsair Dark Core RGB Pro SE Wireless Gaming Mouse, 18,000 DPI Optical Sensor', image_url='https://i.pinimg.com/564x/a9/57/8a/a9578a6b6685feffc61b197db46731f8.jpg', quantity_available=40, seller_id=seller_id)
  
        monitor1 = Product(name='Dell UltraSharp U2720Q', price=549, description='Dell UltraSharp U2720Q 27-inch 4K UHD LED Monitor, IPS', image_url='https://i.pinimg.com/564x/58/ec/d4/58ecd49ea2ab7a33cc7d3478f4430854.jpg', quantity_available=75, seller_id=seller_id)
        monitor2 = Product(name='LG 27UK850-W', price=449, description='LG 27UK850-W 27-inch 4K UHD IPS Monitor with HDR10', image_url='https://i.pinimg.com/564x/21/a4/aa/21a4aa92d916f0bc0d296f9c7138a29f.jpg', quantity_available=60, seller_id=seller_id)
        monitor3 = Product(name='ASUS ROG Swift PG279Q', price=699, description='ASUS ROG Swift PG279Q 27-inch 1440p IPS Gaming Monitor, 165Hz Refresh Rate', image_url='https://i.pinimg.com/564x/73/2a/cb/732acb1b666084a60561a0819c6f9b55.jpg', quantity_available=85, seller_id=seller_id)
        monitor4 = Product(name='BenQ EX2780Q', price=449, description='BenQ EX2780Q 27-inch 1440p IPS Entertainment Monitor, HDRi', image_url='https://i.pinimg.com/564x/73/2a/cb/732acb1b666084a60561a0819c6f9b55.jpg', quantity_available=65, seller_id=seller_id)


        LED_lights1 = Product(name='Philips Hue White and Color Ambiance Starter Kit', price=199, description='Philips Hue White and Color Ambiance Starter Kit, Hub Required, 3 A19 Smart Bulbs & 1 Hue Hub', image_url='https://i.pinimg.com/564x/e6/44/80/e644801e140f10085127c2a57015ff05.jpg', quantity_available=30, seller_id=seller_id)
        LED_lights2 = Product(name='LIFX Color 1000', price=59, description='LIFX Color 1000 Wi-Fi Smart LED Light Bulb, Multicolor, Dimmable', image_url='https://i.pinimg.com/564x/2f/83/9c/2f839cf3ded97ec4471a08e24ca45627.jpg', quantity_available=20, seller_id=seller_id)
        LED_lights3 = Product(name='Sengled Smart LED Multicolor Starter Kit', price=89, description='Sengled Smart LED Multicolor Starter Kit, Hub Required, 3 BR30 Bulbs & 1 Smart Hub', image_url='https://i.pinimg.com/236x/14/20/fe/1420fe04f758651ee2e65ff207826a40.jpg', quantity_available=35, seller_id=seller_id)
        LED_lights4 = Product(name='Revogi Smart Color LED Bulb LTB211 RGBW Dimmable', price=29, description='Yeelight Smart LED Bulb, Dimmable, RGB Color Changing, Wi-Fi Enabled', image_url='https://i.pinimg.com/564x/82/5a/ab/825aabfb9fd68673b5b0ca063b44ca17.jpg', quantity_available=25, seller_id=seller_id)

        products = [phone1, phone2, phone3, phone4, laptop1, laptop2, laptop3, laptop4, mouse1, mouse2, mouse3, mouse4, monitor1, monitor2, monitor3, monitor4, LED_lights1, LED_lights2, LED_lights3, LED_lights4]

        db.session.add_all(products)
        db.session.commit()

        print('Successfully created products')

if __name__ == '__main__':
    seed_data()