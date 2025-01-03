#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app
from models.models import db, User, Seller, Customer, Category, Item, CartItem, OrderItem, Order, Review

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

        Review.query.delete()
        OrderItem.query.delete()
        Order.query.delete()
        CartItem.query.delete()
        Seller.query.delete()
        Customer.query.delete()
        User.query.delete()
        Item.query.delete()
        Category.query.delete()
        db.session.commit()

        # Users
        users = []
        for i in range(25):

            users.append(User(
                username=f'buyer{i}' if i < 20 else f'seller{i-20}',
                password_hash=f'buyer{i}' if i < 20 else f'seller{i-20}',
                phone=f'{i%10}00){i%10}00-{i%10}000',
                email=f'buyer{i}@gmail.com' if i < 20 else f'seller{i-20}@gmail.com',
                street_1=f'{i%10}0000 Broadway',
                street_2='',
                city='New York',
                state='NY',
                zip_code=f'{i%10}1111'
            ))

        customers = []
        for i in range(20):
                customers.append(Customer(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                mobile=fake.numerify('###-###-####'),
                nickname=users[i].username,
                user = users[i]
            ))

        sellers = []
        for i in range(5):
            sellers.append(Seller(
                name=fake.company(),
                user = users[i+20]
            ))
        
        db.session.add_all(users)
        db.session.add_all(customers)
        db.session.add_all(sellers)
        db.session.commit()

        # Categories
        cats = []
        cat_list = [
            'Books',
            'Movies, Music & Games',
            'Electronics',
            'Computers',
            'Smart Home',
            'Home, Garden & Tools',
            'Food & Grocery',
            'Beauty & Health',
            'Toys, Kids, & Baby',
        ]
        for cat in cat_list:
            cats.append(Category(
                name=cat
            ))
        db.session.add_all(cats)

        # Items : 'Books',
        items = []
        items.append(Item(
            active = 1,
            name = "The Silk Roads: A New History of the World",
            brand = 'Peter Frankopan (Author)',
            default_item_idx = 2,
            prices = [14.99, 20.48, 37.36, 23],
            discount_prices = [14.99, 20.48, 37.36, 12.49],
            amounts = [1, 1, 1, 1],
            units = ['kindle', 'audiobook', 'hardcover', 'paperback'],
            packs = [1, 1, 1, 1],
            about_item = [
                 "INTERNATIONAL BESTSELLER • Far more than a history of the Silk Roads, this book is truly a revelatory new history of the world, promising to destabilize notions of where we come from and where we are headed next.",
                 "A rare book that makes you question your assumptions about the world.” —The Wall Street Journal",
                 "From the Middle East and its political instability to China and its economic rise, the vast region stretching eastward from the Balkans across the steppe and South Asia has been thrust into the global spotlight in recent years. Frankopan teaches us that to understand what is at stake for the cities and nations built on these intricate trade routes, we must first understand their astounding pasts.",
                 "Frankopan realigns our understanding of the world, pointing us eastward. It was on the Silk Roads that East and West first encountered each other through trade and conquest, leading to the spread of ideas, cultures and religions. From the rise and fall of empires to the spread of Buddhism and the advent of Christianity and Islam, right up to the great wars of the twentieth century—this book shows how the fate of the West has always been inextricably linked to the East.",
                 "Also available: The New Silk Roads, a timely exploration of the dramatic and profound changes our world is undergoing right now—as seen from the perspective of the rising powers of the East.",
            ],
            details_1 = [
                 'Publisher;-;Vintage, Reprint edition (March 7, 2017)',
                 'Language;-;English',
                 'Paperback;-;672 pages',
                 'ISBN-10;-;1101912375',
                 'ISBN-13;-;978-1101912379',
                 'Reading age;-;10-13 years',
                 'Item Weight;-;1.8 pounds',
                 'Dimensions;-;6 x 1.45 x 9.18 inches'
            ],
            details_2 = [
                 'Is Discontinued By Manufacturer;-;No',
            ],
            images = [
                 'https://m.media-amazon.com/images/I/91A1-6ny+pL._SY522_.jpg',
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[0],
            seller = sellers[0],
        ))
    
        items.append(Item(
            active = 1,
            name = 'From Values to Action: The Four Principles of Values-Based Leadership',
            brand = 'Harry M. Jansen Kraemer Jr. (Author)',
            default_item_idx = 0,
            prices = [18.00, 30,],
            discount_prices = [16.00, 18.44, ],
            amounts = [1, 1],
            units = ['kindle', 'hardcover',],
            packs = [1, 1,],
            about_item = [
                "Respected former CEO, professor, and speaker examines what it takes to become a values-based leader. In this highly-anticipated book, Harry Kraemer argues that today's business environment demands values-based leaders who, in doing the right thing, deliver outstanding and lasting results. The journey to becoming a values-based leader starts with self-reflection. He asks, If you are not self-reflective, how can you know yourself? If you do not know yourself, how can you lead yourself? If you cannot lead yourself, how can you lead others? Kraemer identifies self-reflection as the first of four principles that guide leaders to make choices that honor their values and candidly recounts how these principles helped him navigate some of the toughest challenges he faced in his career.", 
                "Offers a framework for adopting the principles of values-based leadership, self-reflection, balance, true self-confidence, and genuine humility to lead organizations effectively.", 
                "Based on Kraemer's popular Kellogg MBA course on values-based leadership.", 
                "A recognized expert in values-based leadership, Kraemer is a sought after speaker on the subject. Lively and engaging, Kraemer's book comes at a critical time when true leadership in every facet of society is desperately needed.", 
            ],
            details_1 = [
                'Publisher;-;Jossey-Bass; 1st edition (April 19, 2011)',
                'Language;-;English',
                'Hardcover;-;224 pages',
                'ISBN-10;-;0470881259',
                'ISBN-13;-;978-0470881255',
                'Item Weight;-;2.31 pounds',
                'Dimension;-;6.2 x 1.2 x 9.1 inches',
            ],
            details_2 = [
                'Is Discontinued By Manufacturer;-;No',
            ],
            images = [
                'https://m.media-amazon.com/images/I/71dlwCoPsCL._SY522_.jpg',
                'https://m.media-amazon.com/images/I/81gNcSC-2AL._SY522_.jpg',
                'https://m.media-amazon.com/images/I/71CNLBgpGfL._SL1500_.jpg',
                'https://m.media-amazon.com/images/I/81mWlViW6xL._SL1500_.jpg', 
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[0],
            seller = sellers[0],
        ))

        # Items : 'Movies, Music & Games',

        items.append(Item(
            active = 1,
            name = "PowerA Enhanced Nintendo Switch Controller Wireless - Black, Rechargeable Pro Controller for Switch, Immersive Motion Control and Advanced Gaming Buttons",
            brand = 'PowerA',
            default_item_idx = 0,
            prices = [59.99, ],
            discount_prices = [35.49, ],
            amounts = [1, ],
            units = ['unit', ],
            packs = [1, ],
            about_item = [
                "Wireless controller with Bluetooth 5.0 technology.",
                "Rechargeable lithium-ion battery: Up to 30 hours per charge.",
                "Two mappable Advanced Gaming Buttons.",
                "Embedded anti-friction rings for smooth thumbstick control.", 
                "Superior ergonomics for hours of comfortable gaming.",
                "Intuitive Nintendo button layout.",
                "Low battery warning LED indicator."
            ],
            details_1 = [
                'ASIN;-;B08DRRJBC6',
                'Release date;-;September 5, 2020',
                'Product Dimension;-;5.91 x 4.17 x 2.4 inches',
                'Weight;-;8 ounces',
                'Type of item;-;Videogame',
            ],
            details_2 = [
                'Manufacturer;-;PowerA',
                'Country of Origin;-;China',
                'Batteries;-;1 Lithium Polymer batteries required (included)',
                'Date First Available;-;August 11, 2020',
            ],
            images = [
                'https://m.media-amazon.com/images/I/71MlKoonK-L._SX522_.jpg',
                'https://m.media-amazon.com/images/I/71iu1JeScPL._SX522_.jpg',
                'https://m.media-amazon.com/images/I/710rA7lBqlL._SX522_.jpg',
                'https://m.media-amazon.com/images/I/7112chsO+NL._SX522_.jpg',
                'https://m.media-amazon.com/images/I/71IPR4js2wL._SX522_.jpg',
                'https://m.media-amazon.com/images/I/61o15cgHM8L._SX522_.jpg',
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[0],
            seller = sellers[0],
        ))

        items.append(Item(
            active = 1,
            name = 'Sony WH-1000XM5 The Best Wireless Noise Canceling Headphones with Auto Noise Canceling Optimizer, and Crystal Clear Hands-Free Calling, Smoky Pink',
            brand = 'the Sony Store',
            default_item_idx = 0,
            prices = [399.99, ],
            discount_prices = [298.00, ],
            amounts = [1, ],
            units = ['unit', ],
            packs = [1, ],
            about_item = [
                'THE BEST NOISE CANCELLATION: Two processors control 8 microphones for unprecedented noise cancellation. With Auto NC Optimizer, noise canceling is automatically optimized based on your wearing conditions and environment.', 
                'MAGNIFICENT SOUND: Engineered to perfection with the new Integrated Processor V1', 
                'CRYSTAL CLEAR HANDS-FREE CALLING: 4 beamforming microphones, precise voice pickup, and advanced audio signal processing.', 
                'LONG BATTERY LIFE: Up to 30-hour battery life with quick charging (3 min charge for 3 hours of playback).(USB Type-C Cable included)', 
                'ULTRA-COMFORTABLE: Lightweight design with soft fit leather.',
                'MULTIPOINT CONNECTION: Quickly switch between devices.',
                'CARRY CASE INCLUDED: Carry your headphones effortlessly in the redesigned case.', 
            ],
            details_1 = [
                'Brand;-;Sony',
                'Color;-;Smoky Pink',
                'Ear Placement;-;Over Ear',
                'Form Factor;-;Over Ear',
                'Impedance;-;48 Ohm',
            ],
            details_2 = [
                'Connectivity Tech;-;Bluetooth 5.2, Wireless',
                'Connector Type;-;USB Type C',
                'Noise Control;-;active noise cancellation',
                'Headphones Jack;-;3.5 mm Jack',
                'Cable Feature;-;Without Cable',
                'Control Type;-;Voice Control',
                'Material;-;Leather, Carbon Fiber',
                'Model Name;-;WH1000XM5/P',
            ],
            images = [
                'https://m.media-amazon.com/images/I/51FvhumQETL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/81m6Pyx8ypL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/816XENAlWCL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/81+4fB1ehJL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71KIL0csAfL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71Q4Kk3zyeL._AC_SY879_.jpg', 
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[0],
            seller = sellers[0],
        ))

        items.append(Item(
            active = 1,
            name = 'JBL Vibe Beam - True Wireless JBL Deep Bass Sound Earbuds, Bluetooth 5.2, Water & Dust Resistant, Hands-free call with VoiceAware, Up to 32 hours of battery life (Black)',
            brand = 'the JBL Store',
            default_item_idx = 0,
            prices = [49.95, ],
            discount_prices = [24.95, ],
            amounts = [1, ],
            units = ['unit', ],
            packs = [1, ],
            about_item = [
                "JBL Deep Bass Sound: Get the most from your mixes with high-quality audio from secure, reliable earbuds with 8mm drivers featuring JBL Deep Bass Sound", 
                "Comfortable fit: The ergonomic, stick-closed design of the JBL Vibe Beam fits so comfortably you may forget you're wearing them. The closed design excludes external sounds, enhancing the bass performance", 
                "Up to 32 (8h + 24h) hours of battery life and speed charging: With 8 hours of battery life in the earbuds and 24 in the case, the JBL Vibe Beam provide all-day audio. When you need more power, you can speed charge an extra two hours in just 10 minutes.", 
                "Hands-free calls with VoiceAware: When you're making hands-free stereo calls on the go, VoiceAware lets you balance how much of your own voice you hear while talking with others",
                "Water and dust resistant: From the beach to the bike trail, the IP54-certified earbuds and IPX2 charging case are water and dust resistant for all-day experiences", 
            ],
            details_1 = [
                'Brand;-;JBL',
                'Color;-;Black',
                'Ear Placement;-;In Ear',
                'Form Factor;-;In Ear',
                'Impedance;-;16 Ohm',
            ],
            details_2 = [
                'Bluetooth Version;-;5.2',
                'Battery Life;-;32 Hours',
                'Battery Size;-;530mAh',
                'Water Resistants;-;IP54 earbuds and IPX2 case',
                'Noise Cancellation;-;No',
                'Ambient Aware;-;Smart Ambient with TalkThru',
                'Number of Mics;-;2 Mics',
                'JBL Sound;-;JBL Deep Bass Sound',
            ],
            images = [
                'https://m.media-amazon.com/images/I/41+1Csr1pSL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/51hrTx-nCdL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/51+hzCQ97WL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61V52s8z8eL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71QBbCa6mHL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/618QCoicmSL._AC_SX679_.jpg', 
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[0],
            seller = sellers[0],
        ))

        # Items : 'Electronics',

        items.append(Item(
            active = 1,
            name = 'SanDisk 256GB Extreme microSDXC UHS-I Memory Card with Adapter - Up to 190MB/s, C10, U3, V30, 4K, 5K, A2, Micro SD Card - SDSQXAV-256G-GN6MA',
            brand = 'SanDisk Store',
            default_item_idx = 0,
            prices = [27.99, 42.46, 91.99,],
            discount_prices = [24.64, 42.46, 91.99,],
            amounts = [256, 512, 1],
            units = ['GB', 'GB', 'TB'],
            packs = [1, 1, 1,],
            about_item = [
                "Save time with card offload speeds of up to 190MB/s powered by SanDisk QuickFlow Technology (Up to 190MB/s read speeds, engineered with proprietary technology to reach speeds beyond UHS-I 104MB/s, requires compatible devices capable of reaching such speeds. Based on internal testing; performance may be lower depending upon host device interface, usage conditions and other factors. 1MB=1,000,000 bytes. SanDisk QuickFlow Technology is only available for 64GB, 128GB, 256GB, 400GB, 512GB, and 1TB capacities. 1GB=1,000,000,000 bytes and 1TB=1,000,000,000,000 bytes. Actual user storage less.)",
                "Pair with the SanDisk Professional PRO-READER SD and microSD to achieve maximum speeds (sold separately), Compatible with microSDHC, microSDXC, microSDHC UHS-I, and microSDXC UHS-I supporting host devices",
                "Up to 130MB/s write speeds for fast shooting (Based on internal testing; performance may be lower depending upon host device interface, usage conditions and other factors. 1MB=1,000,000 bytes.)",
                "4K and 5K UHD-ready with UHS Speed Class 3 (U3) and Video Speed Class 30 (V30) (Compatible device required. Full HD (1920x1080), 4K UHD (3840 x 2160), and 5K UHD (5120 X 2880) support may vary based upon host device, file attributes and other factors. See HD page on SanDisk site. UHS Speed Class 3 (U3) designates a performance option designed to support real-time video recording with UHS-enabled host devices. Video Speed Class 30 (V30), sustained video capture rate of 30MB/s, designates a performance option designed to support real-time video recording with UHS-enabled host devices. See the SD Association's official website.)",
                "Rated A2 for faster loading and in-app performance (A2 performance is 4000 read IOPS, 2000 write IOPS. Results may vary based on host device, app type and other factors)",
            ],
            details_1 = [
                'Brand;-;SanDisk',
                'Model Name;-;SanDisk Extreme microSD UHS-I Card with Adapter',
                'Flash Memory Type;-;Micro SDXC',
                'Scent;-;Unscented',
                'Compatible Devices;-;Action Cameras, Digital Cameras, Tablet, Smartphone, Drones',
            ],
            details_2 = [
                'Transfer Speeds;-;Up to 190MB/s(1)[128GB-1TB](2)',
                'Shot Speeds;-;Up to 130MB/s[256GB-1TB]',
                'Video Quality;-;4K & 5K UHD(3)',
                'Speed Class;-;C10, V30, and U3(4)',
                'App Performance;-;A2 Specification(5)[64GB-1TB]',
            ],
            images = [
                'https://m.media-amazon.com/images/I/719ZXZP+5LL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71sXK8lfQwL._AC_SX679_.jpg',
                'https://m.media-amazon.com/images/I/81JdU5CVySL._AC_SX679_.jpg',
                'https://m.media-amazon.com/images/I/81UDwWaka2L._AC_SX679_.jpg',
                'https://m.media-amazon.com/images/I/7125Gn7LbWL._AC_SX679_.jpg',
                'https://m.media-amazon.com/images/I/81dOA8U3ROL._AC_SX679_.jpg',
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[0],
            seller = sellers[0],
        ))

        items.append(Item(
            active = 1,
            name = 'Liene 4x6'' Photo Printer, Phone Printer 100 Sheets & 3 Cartridges, Full-Color Photo, Portable Instant Photo Printer for iPhone Android, Thermal Dye Sublimation, Wi-Fi Picture Printer 100 Papers',
            brand = 'Liene Store',
            default_item_idx = 0,
            prices = [229.99, ],
            discount_prices = [135.99, ],
            amounts = [1, ],
            units = ['unit', ],
            packs = [1, ],
            about_item = [
                "User-Friendly Portable Photo Printer for iPhone, Android & PC - Get beautiful and colourful memories with Liene 4x6 photo printer! Full package includes smartphone photo printer, Liene 4x6 photo printer papers (100 sheets), 3 colour cartridges, and fully sealed cassette to prevent dust. Minimalist and magnetic design for compact storage.", 
                "Superior Quality 4x6 Photo Printer - Print photos like no other thanks to the thermal-dye sublimation tech adopted by the picture printer for iphone. The dyes deeply penetrate the paper for vibrant photo printing, and the laminated surface is resistant to water, scratches, fingerprints and fading. Get Liene photo printers now for yourself and your loved ones, print your happy moments together and keep your love forever!", 
                "Wi-Fi Photo Printer for Smartphone - The built-in hotspot of the photo printer makes it easy to print pictures from your phone, avoiding outside interference with a fast and stable connection. No other networks required! Simply connect your device to the independent instant photo printer 4x6 hotspot.", 
                "Multiple Device Compatibility - Liene phone printer provides instant photo printing for up to 5 simultaneous connections. Share with family and friends or print from your different devices. No additional cables or Bluetooth required when printing photos with this picture printer.", 
                "Customize your Printing with the Liene App - Customize your photos with our specialized App! You can add a Square border, insert filters, enhance the contrast and brightness, check printing status, and more. You can even print your ID and Visa photos from home with this photo printer for iphone 4x6 prints.", 
            ],
            details_1 = [
                'Brand;-;Liene',
                'Connectivity Technology;-;Wi-Fi, USB',
                'Special Feature;-;Borderless Printing',
                'Color;-;White',
                'Model Name;-;DHP513',
                'Printer Output;-;Color',
                'Maximum Print Speed (Color);-;1 ppm',
                'Product Dimensions;-;7.48"D x 9.84"W x 7.48"H',
                'Controller Type;-;Windows, iOS, Mac, Android',
            ],
            details_2 = [
                'Paper Size;-;4x6',
                'Number of Paper Included;-;20',
                'Number of Ink Cartridge;-;1',
                'Connection;-;Wi-Fi, USB',
                'Weight;-;2.16lbs',
            ],
            images = [
                'https://m.media-amazon.com/images/I/81VcMk0B3LL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/81VE02ekKML._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/81607irxOoL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71WdZTNCWTL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71Wv2GNDOuL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/718pGOeW+EL._AC_SX679_.jpg', 
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[0],
            seller = sellers[0],
        ))

        # Items : 'Computers',

        items.append(Item(
            active = 1,
            name = "Sceptre Curved 24-inch Gaming Monitor 1080p R1500 98% sRGB HDMI x2 VGA Build-in Speakers, VESA Wall Mount Machine Black (C248W-1920RN Series)",
            brand = 'Sceptre',
            default_item_idx = 0,
            prices = [99.97,],
            discount_prices = [93.79,],
            amounts = [1,],
            units = ['unit',],
            packs = [1,],
            about_item = [
                "1800R curve monitor the curved display delivers a revolutionary visual experience with a leading 1800R screen curvature as the images appear to wrap around you for an in depth, immersive experience", 
                "Hdmi, VGA & PC audio in ports", 
                "High refresh rate 75Hz.Brightness (cd/m²):250 cd/m2", 
                "Vesa wall mount ready; Lamp Life: 30,000+ Hours", 
                "Windows 10 Sceptre Monitors are fully compatible with Windows 10, the most recent operating System available on PCs.Brightness: 220 cd/M2",
                "Pixel Pitch: 0.27156mm (H) x 0.27156 mm (V)",
                "75 hertz",
            ],
            details_1 = [
                'Brand;-;Sceptre',
                'Screen Size;-;24 Inches',
                'Resolution;-;FDH 1080p',
                'Aspect Ratio;-;16:9',
                'Screen Surface Description;-;Glossy',
            ],
            details_2 = [
                'Standing Screen Display Size;-;24 Inches',
                'Screen Resolution;-;1920x1080',
                'Max Screen Resolution;-;1920x1080',
                'Brand;-;Sceptre',
                'Item Model Number;-;C248W-1920RN',
                'Item Weight;-;7 pounds',
                'Product Dimension;-;16.04 x 21.61 x 9.06 inches',
                'Item Dimensions LxWxH;-;16.04  21.61 x 9.06 inches',
                'Color;-;Metal Black',
                'Voltage;-;110240 Volts',
                'Manufacturer;-;Sceptre',
                'ASIN;-;B07KXSR99Y',
                'Country of Origin;-;China',
                'Date First Available;-;December 1, 2018',
            ],
            images = [
                'https://m.media-amazon.com/images/I/71P0M7tKjYL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/81tqfkSX2sL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71PB0Cg1y3L._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71YsgB8ywOL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61EfXRGhuXL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/51f3lg5yumL._AC_SX679_.jpg', 
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[0],
            seller = sellers[0],
        ))

        items.append(Item(
            active = 1,
            name = 'Apple 2024 Mac Mini Desktop Computer with M4 chip with 10core CPU and 10core GPU: Built for Apple Intelligence, 16GB Unified Memory, 256GB SSD Storage, Gigabit Ethernet. Works with iPhone/iPad',
            brand = 'Apple Store',
            default_item_idx = 0,
            prices = [599.00,],
            discount_prices = [499.99,],
            amounts = [1,],
            units = ['unit',],
            packs = [1,],
            about_item = [
                "SIZE DOWN. POWER UP — The far mightier, way tinier Mac mini desktop computer is five by five inches of pure power. Built for Apple Intelligence.* Redesigned around Apple silicon to unleash the full speed and capabilities of the spectacular M4 chip. With ports at your convenience, on the front and back.", 
                "LOOKS SMALL. LIVES LARGE — At just five by five inches, Mac mini is designed to fit perfectly next to a monitor and is easy to place just about anywhere.", 
                "CONVENIENT CONNECTIONS — Get connected with Thunderbolt, HDMI, and Gigabit Ethernet ports on the back and, for the first time, front-facing USB-C ports and a headphone jack.", 
                "SUPERCHARGED BY M4 — The powerful M4 chip delivers spectacular performance so everything feels snappy and fluid.", 
                "BUILT FOR APPLE INTELLIGENCE — Apple Intelligence is the personal intelligence system that helps you write, express yourself, and get things done effortlessly. With groundbreaking privacy protections, it gives you peace of mind that no one else can access your data — not even Apple.*",
                "APPS FLY WITH APPLE SILICON — All your favorites, including Microsoft 365 and Adobe Creative Cloud, run lightning fast in macOS.*",
                "IF YOU LOVE IPHONE, YOU'LL LOVE MAC — Mac works like magic with your other Apple devices. View and control what's on your iPhone from your Mac with iPhone Mirroring.* Copy something on iPhone and paste it on Mac. Send texts with Messages or use your Mac to answer FaceTime calls.*",
            ],
            details_1 = [
                'Brand;-;Apple',
                'Operating System;-;Mac OS',
                'CPU Model;-;Apple M4',
                'CPU Speed;-;1',
                'Graphics Card Description;-;Integrated',
                'Graphics Coprocessor;-;Apple Integrated Graphics',
                'Memory Storage Capacity;-;16 GB',
                'Specific Uses For Product;-;Everyday Use, Education, Business',
                'Personal Computer Design Type;-;Mini PC',
                'Ram Memory Installed Size;-;16 GB',
            ],
            details_2 = [
                'Display;-;24-inch 4.5K Retina display',
                'Processor;-;Apple M4 chip',
                'CPU;-;10-core CPU',
                'GPU;-;10-core GPU',
                'Apple Intelligence;-;Yes',
                'Memory;-;Up to 32GB unified memory',
                'Storage;-;Up to 2TB',
                'Keyboard and Mouse;-;Magic Keyboard with Touch ID, Magic Mouse',
            ],
            images = [
                'https://m.media-amazon.com/images/I/615y53Ws-NL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71z1d0Sg0hL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61D65d5SvdL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61ckwOsZG4L._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/81RptZyEZZL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61AvLgnYlQL._AC_SX679_.jpg', 
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[0], 
            seller = sellers[0],
        ))

        # Items : 'SmartHome',

        items.append(Item(
            active = 1,
            name = 'August Home, Silver Wi-Fi Connected Smart Keyless Entry Door Lock, Electronic Door Lock Fits Your Existing Deadbolt in Minutes, AUG-SL05-M01-S01',
            brand = 'August Home Store',
            default_item_idx = 0,
            prices = [229.99, 249.99,],
            discount_prices = [127.98, 149.99,],
            amounts = [1, 1],
            units = ['WiFi Smart Lock', 'Lock + Keypad',],
            packs = [1, 1],
            about_item = [
                "UPGRADE YOUR EXISTING DEADBOLT: August smart locks fit on the inside of your door, making your regular deadbolt smarter, more secure and way more convenient. Keep your keys just in case (but you won't need them).Connectivity Protocol:wi-fi.Note: Measure your door's backset, cross bore and thickness to ensure you find the right fit.", 
                "GRANT ACCESS WITH THE AUGUST APP: Forget key copying. Quickly and easily share permanent, scheduled or temporary access to your home with friends, family and other people you trust, and never put a key under the doormat again.", 
                "EASY TO INSTALL ON ANY DOOR: Even if you're not so handy, installation only takes about 10 minutes. August locks fit perfectly over most single cylinder deadbolts and aren't much bigger than your original thumbturn.", 
                "AUTO-LOCKS AND UNLOCKS: August Wi-Fi Smart Lock is able to Auto-Unlock as you get home for totally hands-free unlocking (optional). With Auto-Lock and DoorSense, your home automatically secures once your door is closed, or after a set amount of time.", 
                "WORKS SEAMLESSLY WITH YOUR SMART HOME: Built-in Wi-Fi allows your lock to work with your favorite voice assistant, including Amazon Alexa, Google Assistant, Apple HomeKit, Samsung SmartThings and more",
                "AWARD-WINNING SMART LOCK YEAR AFTER YEAR: Voted CNET Editor's Choice two years in a row (2020/2021), Best Smart Lock by Good Housekeeping (2021), Best Smart Lock by Tom's Guide (2021).",
                "KEEP YOUR HOME'S CURB APPEAL: Get smart lock functionality without changing the look of the outside of your front door. August smart locks are installed only on the inside of the door, so your design for your front door doesn't have to adapt.",
            ],
            details_1 = [
                'Brand;-;August Home',
                'Special Feature;-;Biometric verification, Retrofits to your existing deadbolt, No hub needed',
                'Lock Type;-;Biometric, Deadbolt, Wi-Fi, Smart Lock',
                'Item Dimensions L x W x H;-;2.8 x 2.8 x 2.75 inches',
                'Material;-;Metal',
            ],
            details_2 = [
                'Style;-;WiFi Smart Lock',
                'Recommended Uses for Product;-;Door',
                'Color;-;Silver',
                'Finish Type;-;Brushed',
                'Included Components;-;August Wi-Fi Smart Lock, Mounting Hardware, Batteries',
                'Controller Type;-;Vera, Google Assistant, Amazon Alexa',
                'Shape;-;Round',
                'Item Weight;-; 181 Grams',
                'Control Method;-;Voice',
                'Connectivity Protocol;-;Wi-Fi',
                'UPC;-;850004426265',
                'Model Name;-;August Wi-Fi Smart Lock, (4th Generation)',
                'Global Trade Identification Number;-;00850004426265',
                'Manufacturer;-;August Home Inc',
                'ASIN;-;B082VXK9CK',
                'Country of Origin;-;China',
                'Item Model Number;-;AUG-SL05-M01-S01',
                'Batteries;-;2 CR123A batteries required. (included)',
            ],
            images = [
                'https://m.media-amazon.com/images/I/61e592E6PqL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61uBJoqdY4L._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71F0U12YwfL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71YiVGRRn1L._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61ZLFrT8LYL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61MgfyKFg+L._AC_SX679_.jpg', 
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[0], 
            seller = sellers[0],
        ))

        # Items : 'Home, Garden & Tools',

        items.append(Item(
            active = 1,
            name = 'LYKOCLEAN Hydroponics Growing System 12 Pods, Indoor Herb Garden with Grow Light Water Pump Automatic Timer, Smart Indoor Gardening System for Salad Lettuce, Fruit, Vegetable Plant, Grey',
            brand = 'LYKOCLEAN',
            default_item_idx = 0,
            prices = [159.99,],
            discount_prices = [59.99,],
            amounts = [1, ],
            units = ['unit',],
            packs = [1,],
            about_item = [
                "Intelligent Water Recycling System: LYKOCLEAN indoor hydroponics growing system, every 30 minutes silent circulation, to provide sufficient oxygen for the plants. 4L large capacity, can be used for 20 days, vacation travel do not have to worry about lack of water", 
                "Professional Simulated Light: The aero gardening system restores daily light, simulates sunlight for 16h of work, then goes dormant for 8h, then turns on again on a 24-hour cycle. Several types of light for indoor herb gardens allow plants to grow up to 6 times faster than outdoor gardens. The most realistic ecological environment for your plant garden, fast harvest", 
                "Harvest in Just 2 Modes: Just press the power button to activate vegetable mode by default. The light in this mode promotes plant germination and growth, which is 6 times faster than in soil. Switch to fruit mode during fruiting to enhance harvest. Both modes provide essential growth factors: sunlight, moisture, and oxygen", 
                "Flexible Height Adjustment: Choose your favorite seeds and grow up to 12 plants at a time. Don't worry about the height of the fruit and flower plants. At the beginning of germination, you can turn the height down to the lowest level so that the planting gets enough sunlight, and the height of the device can be adjusted according to the plants at the growth stage", 
                "Ideal Gift Choice: Our hydroponic herb garden comes with everything you need to grow. Includes 12 planting baskets, 12 planting domes, 12 planting sponges, and 12 plant labels. The hydroponic growing system is ideal for holiday gifts, share the green and organic growing experience with your family and friends.", 
            ],
            details_1 = [
                'Brand;-;LYKOCLEAN',
                'Item Weight;-;4.44 Pounds',
                'Manufacturer;-;LYKOCLEAN',
            ],
            details_2 = [
                'Package Dimensions;-;6 x 3 x 1 inches',
                'Item model number;-;LYKOCLEAN-LK-LSC-12pods-Grey',
                'Date First Available;-;October 4, 2023',
                'Manufacturer;-;LYKOCLEAN',
                'ASIN;-;B0CX4SGMGL',
                'Country of Origin;-;China',
            ],
            images = [
                'https://m.media-amazon.com/images/I/81nV07g46eL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/811CpMGHnRL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/81Ne3H9kcaL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71gUJ7x88pL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71CSdWDdOyL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/81IF7Td4PiL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/81QscTQqftL._AC_SX679_.jpg',
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[1], 
            seller = sellers[0],
        ))

        items.append(Item(
            active = 1,
            name = 'White Ceramic Vase Set of 2 for Modern Home Decor, Round Matte Donut Vases for Pampas Grass, Neutral Boho Nordic Minimalism Style Flower Vases for Living Room Wedding Table Party Office Bedroom',
            brand = 'COTYNI',
            default_item_idx = 0,
            prices = [32.99, ],
            discount_prices = [25.99, ],
            amounts = [1, ],
            units = ['unit', ],
            packs = [2, ],
            about_item = [
                "【Unique White Ceramic Vase--Original Creation by COTYNI】 The hollow and irregular design of the white ceramic vases add a modern, minimalist style to your home decor. The unique donut shape makes the vases romantic and stylish. Let our beautiful ceramic vases become part of your home decor collection.", 
                "【Perfect Details & Extreme Crafsmanship】 Our pampas grass vases are expertly designed to achieve perfect line proportions, 100% ceramic craftsmanship. Each vase is handcrafted by experienced masters using high quality clay. The exquisite craftsmanship, frosted feel and smooth lines make it a perfect work of art. These vases are resistant to corrosion, wear and tear and are built to last. Such high quality decorative pieces keep your decorations fresh year after year.", 
                "【Multi-purpose Decorative Vases】 Our modern vases have been crafted with a new upgrade and are not only suitable for holding dried flowers, but can also be used to hold flowers in water without any worries about leaks. This bohemian vase is suitable for fireplace decoration, bedroom decoration, table decoration, dining table decoration, living room decoration, etc. Add a beautiful landscape of art to your space decoration. It can also be used as a beautiful gift choice for weddings, housewarming.", 
                "【Perfect Match for Bohe Decoration】 White ceramic vases are clean and elegant, it can be well matched with dried flowers, pampas grass, succulents, flowers, it will be the centerpiece of your living room, bedroom, study, office, desk and other places. This exquisite and simple floral porcelain vase will enhance your home's taste.", 
                "【Sturdy Packaging】 The whole set is carefully wrapped in molded foam and thick box after high standard quality inspection to avoid damage during transportation. Since each ceramic vase is handmade, there may be a little deviation. If you have any questions or problems after receiving the product, please feel free to email us and we will solve your problem perfectly within 12 hours.", 
            ],
            details_1 = [
                'Material;-;Ceramic',
                'Color;-;White Vase',
                'Brand;-;COTYNI',
                'Product Dimensions;-;7.5"L x 1.4"W x 7.5"H',
                'Shape;-;Irregular',
            ],
            details_2 = [
                'Style;-;Garden',
                'Special Feature;-;Corrosion Resistant, Durable, Handmade',
                'Theme;-;Flowers',
                'Recommended Uses For Product;-;Decor',
                'Finish Type;-;Matte',
                'Number of Pieces;-;2',
                'Installation Type;-;Freestanding',
                'Mounting Type;-;Table',
                'UPC;-;774034303238',
                'Item Weight;-;2.32 pounds',
                'ASIN;-;B0BB2LB224'
            ],
            images = [
                'https://m.media-amazon.com/images/I/71Ms+27gxoL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61pPwGrnLhL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61mKxxbLm8L._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71viH6yoxCL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71i6bnWiEvL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/711Y+5gjhyL._AC_SX679_.jpg', 
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[1], 
            seller = sellers[0],
        ))

        items.append(Item(
            active = 1,
            name = 'Govee RGBIC Floor Lamp, LED Corner Lamp Works with Alexa, 1000 Lumen Smart Modern Floor Lamp with Music Sync and 16 Million DIY Colors, Color Changing Standing Floor Lamp for Bedroom Living Room Black',
            brand = 'Govee',
            default_item_idx = 0,
            prices = [99.99, ],
            discount_prices = [99.99, ],
            amounts = [1, ],
            units = ['unit', ],
            packs = [1, ],
            about_item = [
                "Dynamic RGBIC Color: Unleash your creativity with Govee RGBIC technology, you can customize each segment color base and the floor lamp will display multicolor effects simultaneously, suitable for Christmas decorations and family gifts.", 
                "Smart Control: Manage your LED floor lamp with simple voice commands via Alexa, Google Assistant. And Govee Home APP also make it more convenient to enjoy multiple dynamic scenes like Cheerful, Romantic and design your living room or bedroom decorations.", 
                "Sync with Music: Elevate your movie, party, gaming time or listening session with our modern floor lamps for living room, the color and brightness of it will change simultaneously as music or gaming audio changes.", 
                "16 Million DIY Colors: The floor lamp owns millions of color and 58 Dynamic scene modes, you can explore your favored one or pick one for Christmas decorations, to bring yourself to a real fantastic lighting experience(only support 2.4Ghz WiFi).",
                "Wide Application: Add exciting, expressive, and personalized lighting to your gaming room, living room and summer decorations indoor. With unique shape and weight design, you can move this standing floor lamp in your house freely.",
                "Note: With the height of 136cm and seperate warm white LEDs, this floor lamp provides up to 1000 lumen lighting for daily illumination. Components: 4 aluminum light pole section, aluminum base, silicone light strip, power adapter.",
            ],
            details_1 = [
                'Finish Type;-;Painted',
                'Base Material;-;Aluminum',
                'Product Dimensions;-;7.9"D x 7.9W x 53.8"H',
                'Item Weight;-;3.52 Pounds',
                'Lamp Type;-;Floor Lamp',
            ],
            details_2 = [
                'Alexa Compatible;-;Yes',
                'Matter Compatible;-;No',
                'Color;-;RGBIC + Warm White',
                'Color Temperature;-;3300-4300K',
                'Lumens;-;1000',
                'Scene Mode;-;61',
                'Height;-;1360mm / 53in',
            ],
            images = [
                'https://m.media-amazon.com/images/I/615Yog6t9nL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71fGbR-anfL._AC_SY879_.jpg', 
                'https://m.media-amazon.com/images/I/719as+6e-mL._AC_SY879_.jpg', 
                'https://m.media-amazon.com/images/I/61nP38UdsjL._AC_SY879_.jpg', 
                'https://m.media-amazon.com/images/I/61eTnCvuRDL._AC_SY879_.jpg', 
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[1], 
            seller = sellers[0],
        ))

        # Items : 'Food & Grocery',

        items.append(Item(
            active = 1,
            name = 'Nespresso Capsules Vertuo, Variety Pack, Medium and Dark Roast Coffee, 30 Count Coffee Pods, Brews 7.8 oz.',
            brand = 'Nespresso',
            default_item_idx = 1,
            prices = [37.50, 46.98, ],
            discount_prices = [37.50, 46.98, ],
            amounts = [10, 10, ],
            units = ['count', 'count', ],
            packs = [3, 4, ],
            about_item = [
                "DEEP ; DENSE:;;Brown sugar and roasted notes are the signature aromatics of the Intenso coffee pod. It’s an intense long black with a distinctly lingering aftertaste and a thick coffee crema.", 
                "DARK ROAST: The Arabicas get a darker roast to lower the acidity and bring out that brown sugar aroma. The Guatemalan Robusta gets a longer roast to develop bold and bitter notes.; Intensity9.", 
                "INTENSO COFFEE BREWS 7.77 FL. OZ.: These Nespresso Vertuo pods provide you with a 7.77 fl. oz. serving of coffee which is perfect for a longer drinking experience", 
                "SAVOR WITH MILK: Every Nespresso coffee is created to taste great both as a black coffee and as part of a milk with coffee recipe.", 
                "SUSTAINABILITY FIRST:;As a certified B Corporation,;Nespresso;meets the highest standards of verified social and environmental performance, joining a global movement using business as a force for good.;;Nespresso aluminum capsules are fully recyclable and guarantee coffee freshness - we provide different options for recycling your used aluminum coffee pods to fulfill our collective commitment to protecting the environment",
                "MACHINE COMPATIBILITY:;Nespresso;Vertuo pods are not compatible with;Original;Line machines.",
            ],
            details_1 = [
                'Brand;-;Nespresso',
                'Item Form;-;Capsule',
                'Flavor;-;Intenso',
                'Caffeine Content Description;-;Caffeinated',
                'Roast Level;-;Dark Roast',
            ],
            details_2 = [
                'Manufacturer;-;Nespresso Pods',
                'Part Number;-;SG_B0768N9N6K_US',
                'Item Weight;-;13.2 ounces',
                'Product Dimensions;-;11.42 x 7.64 x 3.91 inches',
                'Item model number;-;Ad-bm11-94455',
                'Is Discontinued By Manufacturer;-;No',
                'Country of Origin;-;Switzerland',
                'Style;-;Vertuo Medium/Dark Roast',
                'Size;-;10 Count',
            ],
            images = [
                'https://m.media-amazon.com/images/I/51oRUDe8wxL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61WewPIS4vL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/81G9mFCgTqL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71pMOpsIMfL._AC_SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71q8qBZEYIL._AC_SX679_.jpg',
                'https://m.media-amazon.com/images/I/71Vjyw2E2vL._AC_SX679_.jpg',
                'https://m.media-amazon.com/images/I/515OIJcgU4L._AC_SX679_.jpg',
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[1], 
            seller = sellers[0],
        ))

        ############################################################################
        # Items : 'Beauty & Health',
        ############################################################################

        items.append(Item(
            active = 1,
            name = 'BIODANCE Bio-Collagen Real Deep Mask, Hydrating Overnight Hydrogel Mask, Pore Minimizing, Elasticity Improvement, 34g x4ea',
            brand = 'BIODANCE',
            default_item_idx = 0,
            prices = [19.00, 62.00],
            discount_prices = [19.00, 62.00],
            amounts = [4, 16, ],
            units = ['Count', 'Count',],
            packs = [1, 1, ],
            about_item = [
                "DEEP HYDRATION: The oligo-hyaluronic acid in the Biodance Bio-Collagen Real Deep Mask provides superior moisturizing effects compared to regular hyaluronic acid. It quickly hydrates the skin's surface and penetrates deeper layers, leaving the complexion healthy and well-moisturized.", 
                "PORE TIGHTENING & FIRMING: Ultra-low molecular collagen maximizes absorption and skin penetration. It helps refine enlarged pores, enhances skin elasticity immediately after application, and visibly reduces the appearance of fine lines and wrinkles.", 
                "BRIGHTENS THE SKIN: Formulated with Galactomyces Ferment Filtrate and Niacinamide, it improves uneven skin tone and texture while offering antioxidant effects, resulting in healthier, more radiant skin.", 
                "AMPOULE SOLIDIFIED: Each 1.19 oz bottle of ampoule is solidified into a sheet mask.", 
                "BECOMES TRANSPARENT: The mask turns transparent after 3 hours or overnight, delivering active ingredients deep into the skin.", 
                "SAFE FOR SENSITIVE SKIN: All Biodance products are formulated with non-toxic, non-irritant ingredients. They are free from common allergens and 19 other harmful or controversial substances, making them completely safe for sensitive skin.",
            ],
            details_1 = [
                'Brand;-;BIODANCE',
                'Item Form;-;Sheet',
                'Product Benefits;-;Hydrating, Pore Treatment, Moisturizing, Anti Aging, Firming',
                'Scent;-;Collagen',
                'Material Type;-;Non-toxic',
            ],
            details_2 = [
                'Sold By;-;Biodance',
                'Skin Type;-;All, Sensitive, Combination, Dry, Oily',
                'Form;-;Sheet',
                'Specialty ;-;Hypoallergenic',
            ],
            images = [
                'https://m.media-amazon.com/images/I/51299uVd3YL._SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71KorRTgLlL._SX679_.jpg', 
                'https://m.media-amazon.com/images/I/610s3PQnk-L._SX679_.jpg', 
                'https://m.media-amazon.com/images/I/71oGe24lN-L._SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61FuTZRjOoL._SX679_.jpg', 
                'https://m.media-amazon.com/images/I/61lMkfbvCoL._SX679_.jpg', 
            ],
            accum_sales_cnt = 0,
            avg_review_rating = 0,
            accum_review_cnt = 0,
            category = cats[1], 
            seller = sellers[0],
        ))

        # Items : 'Toys, Kids & Baby',

        # Reviews

        stars = [1, 2, 3, 4, 5]

        reviews = []
        for i in range(1, 20):
            for item in items: 
                review = Review(
                    rating = rc(stars), 
                    headline = fake.sentence(),
                    content = fake.paragraph(),
                    images = '',
                    review_done = 1,
                    item = item, 
                    customer = customers[i]
                )

                reviews.append(review)
                item.accum_review_cnt += 1
                item.avg_review_rating += (review.rating - item.avg_review_rating) / item.accum_review_cnt
        
        db.session.add_all(items)
        db.session.add_all(reviews)
        db.session.commit() 