import unittest
from flask import url_for
from flask_testing import TestCase, LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen

from application import app, db
from application.models import Character, DiceRoll

#
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

class SeleniAddChar(SeleniBase):
    players = [('Luke Warm','2', 'Human'),('Chang Edlater', 3, 'Elf')]
    def add_player(self, player):
    
        self.driver.find_element_by_xpath('/html/body/h2[1]/a[2]').click()
        self.driver.find_element_by_xpath('//*[@id="name"]').send_keys(player[0])
        self.driver.find_element_by_xpath('//*[@id="level"]').send_keys(player[1])
        self.driver.find_element_by_xpath('//*[@id="race"]').send_keys(player[2])
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
    
    def test_create_success(self):
        for player in self.players:
            self.add_player(player)
            self.assertIn(url_for('home'), self.driver.current_url)
            
            player_details = self.driver.find_element_by_xpath('/html/body/p[1]').text
            self.assertIn(player[0],player_details)
            self.assertIn(str(player[1]),player_details)
            self.assertIn(str(player[2]),player_details)

            self.driver.find_element_by_xpath('/html/body/form[1]/input').click() # goes to summary page
            self.driver.find_element_by_xpath('/html/body/form[1]/input').click() # deletes character
    
    fail_players_1 = [('L',1,'Human'),('A'*41,1,'Human')]
    def test_create_fail_name(self):
        for player in self.fail_players_1:
            self.add_player(player)
            self.assertIn(url_for('addchar'),self.driver.current_url) #checks the page hasn't changed
            error = self.driver.find_element_by_xpath('/html/body/form/div/span/i').text
            self.assertEqual(error,'Enter a name between 2 and 40 characters long')

    fail_players_2 = [('Luke Warm',2,'H'),('Brian Butterfield',3,'H'*41)]
    def test_create_fail_race(self):
        for player in self.fail_players_2:
            self.add_player(player)
            self.assertIn(url_for('addchar'),self.driver.current_url) #checks the page hasn't changed
            error = self.driver.find_element_by_xpath('/html/body/form/div/span/i').text
            self.assertEqual(error,'Enter a race between 2 and 40 characters long')

    fail_players_3 = [('Luke Warm', 'Level 1', 'Human')]
    def test_create_fail_level(self):
        for player in self.fail_players_3:
            self.add_player(player)
            self.assertIn(url_for('addchar'),self.driver.current_url) #checks the page hasn't changed
            error = self.driver.find_element_by_xpath('/html/body/form/div/span/i').text
            self.assertEqual(error,'Not a valid integer value')

class SeleniAddDice(SeleniBase):
    
    def test_create_success_dice(self):
        player_1 = Character(name="Chang Edlater",level=4,race='Tiefling')     
        db.session.add(player_1)
        db.session.commit()

        self.driver.find_element_by_xpath('/html/body/h2[1]/a[3]').click()
        self.driver.find_element_by_xpath('//*[@id="character"]/option[1]').click()
        self.driver.find_element_by_xpath('//*//*[@id="dice_roll"]/option[5]').click()
        self.driver.find_element_by_xpath('//*[@id="dice_result"]').send_keys(17)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        
        self.assertIn(url_for('adddice'),self.driver.current_url)

        self.driver.find_element_by_xpath('/html/body/h2[1]/a[1]').click()

        self.assertIn(url_for('home'),self.driver.current_url)
        dice_rolls = self.driver.find_element_by_xpath('/html/body/p[1]').text
        self.assertIn('d20=17',dice_rolls)
    
    def test_create_fail_dice(self):
        player_1 = Character(name="Chang Edlater",level=4,race='Tiefling')     
        db.session.add(player_1)
        db.session.commit()

        self.driver.find_element_by_xpath('/html/body/h2[1]/a[3]').click()
        self.driver.find_element_by_xpath('//*[@id="character"]/option[1]').click()
        self.driver.find_element_by_xpath('//*//*[@id="dice_roll"]/option[5]').click()
        self.driver.find_element_by_xpath('//*[@id="dice_result"]').send_keys(23)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        
        self.assertIn(url_for('adddice'),self.driver.current_url)
        error = self.driver.find_element_by_xpath('/html/body/form/div/span/i').text
        self.assertEqual(error,'Result is too large')

        self.driver.find_element_by_xpath('/html/body/h2[1]/a[1]').click()

        self.assertIn(url_for('home'),self.driver.current_url)
        dice_rolls = self.driver.find_element_by_xpath('/html/body/p[1]').text
        self.assertNotIn('d20=23',dice_rolls)

    def test_create_fail_dice_2(self):
        player_1 = Character(name="Chang Edlater",level=4,race='Tiefling')     
        db.session.add(player_1)
        db.session.commit()

        self.driver.find_element_by_xpath('/html/body/h2[1]/a[3]').click()
        self.driver.find_element_by_xpath('//*[@id="character"]/option[1]').click()
        self.driver.find_element_by_xpath('//*//*[@id="dice_roll"]/option[5]').click()
        self.driver.find_element_by_xpath('//*[@id="dice_result"]').send_keys(-1)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        
        self.assertIn(url_for('adddice'),self.driver.current_url)
        error = self.driver.find_element_by_xpath('/html/body/form/div/span/i').text
        self.assertEqual(error,'Enter a number greater than zero')

        self.driver.find_element_by_xpath('/html/body/h2[1]/a[1]').click()

        self.assertIn(url_for('home'),self.driver.current_url)
        dice_rolls = self.driver.find_element_by_xpath('/html/body/p[1]').text
        self.assertNotIn('d20=-1',dice_rolls)
