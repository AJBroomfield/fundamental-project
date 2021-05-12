import unittest
from flask import url_for
from flask_testing import TestCase, LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen

from application import app, db
from application.models import Character, DiceRoll

class SeleniBase(LiveServerTestCase):
    TEST_PORT = 5050 
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///tester.db",
            LIVESERVER_PORT=self.TEST_PORT,
            DEBUG=True,
            TESTING=True
        )
        return app
    def setUp(self):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        db.create_all() 
        self.driver.get(f'http://localhost:{self.TEST_PORT}')
    def tearDown(self):
        self.driver.quit()
        db.drop_all()
    def test_server_is_up_and_running(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}')
        self.assertEqual(response.code, 200)

class SeleniAdd(SeleniBase):
    def test_create(self):
        
        self.driver.find_element_by_xpath('/html/body/h2[1]/a[2]').click()
        self.driver.find_element_by_xpath('//*[@id="name"]').send_keys('Chang Edlater')
        self.driver.find_element_by_xpath('//*[@id="level"]').send_keys('1')
        self.driver.find_element_by_xpath('//*[@id="race"]').send_keys('Human')
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        self.assertIn(url_for('home'), self.driver.current_url)
        player_details = self.driver.find_element_by_xpath('/html/body/p[1]').text
        self.assertIn('Chang Edlater',player_details)
        self.assertIn('Human',player_details)
        self.assertIn('1',player_details)

class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///tester.db",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False
                )
        return app

    def setUp(self):
        db.create_all()
        player_1 = Character(name="Chang Edlater",level=1,race='Tiefling')     
        roll_1 = DiceRoll(character_id=1,dice_num=20,dice_result=18)
        roll_2 = DiceRoll(character_id=1,dice_num=20,dice_result=3)
        db.session.add(player_1)
        db.session.add(roll_1)
        db.session.add(roll_2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    def test_read_task(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code,200)
    def test_create_get(self):
        response = self.client.get(url_for('adddice'))
        self.assertEqual(response.status_code, 200)
    def test_update_get(self):
        response = self.client.get(url_for('addchar'))
        self.assertEqual(response.status_code, 200)
    def test_complete_get(self):
        response = self.client.get(url_for('summary',id=1),follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    def test_incomplete_get(self):
        response = self.client.get(url_for('deleteroll',id=1),follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    def test_delete_get(self):
        response = self.client.get(url_for('update',id=1),follow_redirects=True)
        self.assertEqual(response.status_code, 200)

class TestRead(TestBase):
    def test_read_task(self):
        response = self.client.get(url_for('home'))
        self.assertIn(b'Chang Edlater',response.data)
        self.assertIn(b'1',response.data)
        self.assertIn(b'Tiefling',response.data)

class TestAdd(TestBase):
    def test_add_character(self):
        response = self.client.post(
            url_for('addchar'),
            data = dict(name='Luke Warm',level = 5,race = 'Mountain Dwarf'),
            follow_redirects=True
        )
        self.assertIn(b'Luke Warm',response.data)
        self.assertIn(b'5' ,response.data)
        self.assertIn(b'Mountain Dwarf',response.data)
    
    def test_add_roll(self):
        response = self.client.post(
            url_for('adddice'),
            data = dict(character_id=1, dice_roll=8, dice_result=7),
            follow_redirects=True
        )
        self.assertIn(b'd8',response.data)
        self.assertIn(b'7',response.data)

class TestUpdate(TestBase):
    def test_update_level(self):
        response = self.client.post(
            url_for('update',id=1),
            data = dict(level=2),
            follow_redirects=True
        )
        self.assertIn(b'Chang Edlater',response.data)
        self.assertIn(b'2',response.data)
        self.assertIn(b'Tiefling',response.data)

class TestDelete(TestBase):
    def test_delete_roll(self):
        response = self.client.get(
            url_for('deleteroll',id=1),
            follow_redirects=True
        )
        self.assertNotIn(b'18',response.data)