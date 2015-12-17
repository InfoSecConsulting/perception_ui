from os import getenv
from flask.ext.script import Manager
from app import create_app, db
from app.main.models import SnmpString
from app.auth.models import TimeZones, AppUser
from sqlalchemy.exc import IntegrityError

web_app = create_app(getenv('FLASK_CONFIG') or 'default')

manager = Manager(web_app)

@manager.command
def seed_db():

  # Add seed data to the database

  snmp_strings = ['public',
                  'private']

  time_zones = ['International Date Line West',
                'Midway Island',
                'American Samoa',
                'Hawaii',
                'Alaska',
                'Pacific Time (US & Canada)',
                'Tijuana',
                'Mountain Time (US & Canada)',
                'Arizona',
                'Chihuahua',
                'Mazatlan',
                'Central Time (US & Canada)',
                'Saskatchewan',
                'Guadalajara',
                'Mexico City',
                'Monterrey',
                'Central America',
                'Eastern Time (US & Canada)',
                'Indiana (East)',
                'Bogota',
                'Lima',
                'Quito',
                'Atlantic Time (Canada)',
                'Caracas',
                'La Paz',
                'Santiago',
                'Newfoundland',
                'Brasilia',
                'Buenos Aires',
                'Montevideo',
                'Georgetown',
                'Greenland',
                'Mid-Atlantic',
                'Azores',
                'Cape Verde Is.',
                'Dublin',
                'Edinburgh',
                'Lisbon',
                'London',
                'Casablanca',
                'Monrovia',
                'UTC',
                'Belgrade',
                'Bratislava',
                'Budapest',
                'Ljubljana',
                'Prague',
                'Sarajevo',
                'Skopje',
                'Warsaw',
                'Zagreb',
                'Brussels',
                'Copenhagen',
                'Madrid',
                'Paris',
                'Amsterdam',
                'Berlin',
                'Bern',
                'Rome',
                'Stockholm',
                'Vienna',
                'West Central Africa',
                'Bucharest',
                'Cairo',
                'Helsinki',
                'Kyiv',
                'Riga',
                'Sofia',
                'Tallinn',
                'Vilnius',
                'Athens',
                'Istanbul',
                'Minsk',
                'Jerusalem',
                'Harare',
                'Pretoria',
                'Kaliningrad',
                'Moscow',
                'St. Petersburg',
                'Vtzolgograd',
                'Samara',
                'Kuwait',
                'Riyadh',
                'Nairobi',
                'Baghdad',
                'Tehran',
                'Abu Dhabi',
                'Muscat',
                'Baku',
                'Tbilisi',
                'Yerevan',
                'Kabul',
                'Ekaterinburg',
                'Islamabad',
                'Karachi',
                'Tashkent',
                'Chennai',
                'Kolkata',
                'Mumbai',
                'New Delhi',
                'Kathmandu',
                'Astana',
                'Dhaka',
                'Sri Jayawardenepura',
                'Almaty',
                'Novosibirsk',
                'Rtzangoon',
                'Bangkok',
                'Hanoi',
                'Jakarta',
                'Krasnoyarsk',
                'Beijing',
                'Chongqing',
                'Hong Kong',
                'Urumqi',
                'Kuala Lumpur',
                'Singapore',
                'Taipei',
                'Perth',
                'Irkutsk',
                'Ulaanbaatar',
                'Seoul',
                'Osaka',
                'Sapporo',
                'Tokyo',
                'Yakutsk',
                'Darwin',
                'Adelaide',
                'Canberra',
                'Melbourne',
                'Sydney',
                'Brisbane',
                'Hobart',
                'Vladivostok',
                'Guam',
                'Port Moresby',
                'Magadan',
                'Srednekolymsk',
                'Solomon Is.',
                'New Caledonia',
                'Fiji',
                'Kamchatka',
                'Marshall Is.',
                'Auckland',
                'Wellington',
                "Nuku'alofa",
                'Tokelau Is.',
                'Chatham Is.',
                'Samoa']

  default_admin = AppUser(username='admin',
                          password='sup3rs3c73tp@ssw0rd',
                          email='admin@your.org',
                          firstname='Admin',
                          lastname='Istrator',
                          phone='5558765309',
                          company='ACME, Inc.')
  try:
    db.session.add(default_admin)
    db.session.commit()
  except IntegrityError:
    db.session.rollback()

  for element in snmp_strings:
    try:
      c = SnmpString(community_string=element)
      db.session.add(c)
      db.session.commit()
    except IntegrityError:
      db.session.rollback()

  for element in time_zones:
    try:
      tz = TimeZones(name=element)
      db.session.add(tz)
      db.session.commit()
    except IntegrityError:
      db.session.rollback()


if __name__ == '__main__':
  try:
    manager.run()
  except (IOError, SystemExit):
    raise
  except KeyboardInterrupt:
    print('Crtl+C Pressed. Shutting down.')