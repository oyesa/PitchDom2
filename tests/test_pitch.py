import unittest
from app.models import Pitch
from app import db

class PitchModelTest(unittest.TestCase):
    def setUp(self):

        self.new_pitch = Pitch(title = "title", pitch_content= "description", upvotes = 1, downvotes = 1)
        db.session.add(self.new_pitch)
        db.session.commit()

    def tearDown(self):
        Pitch.query.delete()
        db.session.commit()

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.title, 'title')
        self.assertEquals(self.new_pitch.pitch_content, 'description')
        self.assertEquals(self.new_pitch.upvotes, 1)
        self.assertEquals(self.new_pitch.downvotes, 1)