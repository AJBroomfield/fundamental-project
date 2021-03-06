import unittest
from flask import url_for
from flask_testing import TestCase

from application import app, db
from application.models import Character, DiceRoll

class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///tester.db",
                SECRET_KEY='TEST_SECRET_KEY',
                SQLALCEHMY_TRACK_MODIFICATIONS=False,
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
    def test_adddice_get(self):
        response = self.client.get(url_for('adddice'))
        self.assertEqual(response.status_code, 200)
    def test_addchar_get(self):
        response = self.client.get(url_for('addchar'))
        self.assertEqual(response.status_code, 200)
    def test_summary_get(self):
        response = self.client.get(url_for('summary',id=1),follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    def test_deleteroll_get(self):
        response = self.client.get(url_for('deleteroll',id=1),follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    def test_update_get(self):
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
            data = dict(character=1, dice_roll=8, dice_result=7),
            follow_redirects=True
        )
        character = Character.query.get(1)
        self.assertEqual(8,character.rolls[-1].dice_num)
        self.assertEqual(7,character.rolls[-1].dice_result)

    def test_add_roll_fail(self):
        response = self.client.post(
            url_for('adddice'),
            data = dict(character=1, dice_roll=8, dice_result=9),
            follow_redirects=True
        )
        self.assertIn(b'Result is too large',response.data)
    
    def test_add_roll_failneg(self):
        response = self.client.post(
            url_for('adddice'),
            data = dict(character=1, dice_roll=8, dice_result=-1),
            follow_redirects=True
        )
        self.assertIn(b'Enter a number greater than zero',response.data)
    

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
    
    def test_delete_roll(self):
        response = self.client.get(
            url_for('deletechar',id=1),
            follow_redirects=True
        )
        self.assertNotIn(b'Luke Warm',response.data)