import unittest
from app.models import User
from app import db

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(username = "Oluchi", email ="oyesa.oluchina@gmail.com", bio = "Genie in a bottle", profile_pic_path = "image_url", password = 'sincera')
        db.session.add(self.new_user)
        db.session.commit()

    def tearDown(self):
        User.query.delete()
        db.session.commit()
 
    def test_password_setter(self):
        self.assertTrue(self.new_user.pass_secure is not None)

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('sincera'))

    def test_save_user(self):
        self.new_user.save_user()
        self.assertTrue(len(User.query.all())>0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_user.username, 'Oluchi')
        self.assertEquals(self.new_user.email, 'oyesa.oluchina@gmail.com')
        self.assertEquals(self.new_user.bio, 'Genie in a bottle')
        self.assertEquals(self.new_user.profile_pic_path, 'image_url')
        self.assertTrue(self.new_user.verify_password('sincera'))


    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password 