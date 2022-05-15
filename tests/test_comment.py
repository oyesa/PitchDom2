import unittest
from app.models import Comment


class TestComment(unittest.TestCase):
    def setUp(self):
        self.new_comment = Comment(comment_content = 'content')

    def tearDown(self):
        Comment.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))