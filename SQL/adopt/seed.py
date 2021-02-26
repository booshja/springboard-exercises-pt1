"""Seed file to make sample data for adopt_db"""

from models import Pet, db
from app import app

db.drop_all()
db.create_all()

p1 = Pet(name='Woofly', species='dog',
         photo_url='https://dogtime.com/assets/uploads/2011/03/puppy-development-1280x720.jpg', age=2, notes="Oh my he's got so much energy!")
p2 = Pet(name='Porchetta', species='porcupine',
         photo_url='https://cdn.mos.cms.futurecdn.net/jFpJp5sJzEeeKtjAnHRM8K-1200-80.jpg', age=9)
p3 = Pet(name='Snargle', species='cat',
         photo_url='https://upload.wikimedia.org/wikipedia/commons/6/68/Lynx_lynx_poing.jpg', age=8, notes="Sneaky girl")
p4 = Pet(name='Rebecca', species='dog',
         photo_url='https://res.cloudinary.com/dk-find-out/image/upload/q_80,w_1920,f_auto/Velociraptor_u4hjbq.jpg', age=2, notes="Super super cuddly!")
p5 = Pet(name='Polly', species='porcupine',
         photo_url='https://image.freepik.com/free-vector/cartoon-pterodactyl-with-her-baby_29190-4302.jpg', age=29, notes="Comes with babies!")
p6 = Pet(name='George', species='cat',
         photo_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTe-6XLJvAfc_Sk56rqBb5LyK1XvVfFBHoaYg&usqp=CAU', age=14, notes="Sometimes buries his head for some reason...")

db.session.add_all([p1, p2, p3, p4, p5, p6])
db.session.commit()
