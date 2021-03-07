import unittest

from Journal import db
from Journal.models import User


class TestCase(unittest.TestCase):
    #...
    def test_follow(self):
        u1 = User(email="addddd1c.com",username="ccccc",password="njnjnjn")
        u2 = User(email="abcsedddddb1c.com",username="ddddd",password="njnjertynjn")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().username == 'ccccc'
        assert u2.followers.count() == 1
        assert u2.followers.first().username == 'ddddd'
        u = u1.unfollow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0
        print("executed without error")

if __name__ == '__main__':
    unittest.main()