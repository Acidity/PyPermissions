import unittest
from permission import Permission, PERMISSION_DELIMITER


class BasicPermissionTests(unittest.TestCase):

    def setUp(self):
        self.p1 = Permission("test{0}1{0}hello".format(PERMISSION_DELIMITER))
        self.p2 = Permission("test{0}2{0}hello".format(PERMISSION_DELIMITER))
        self.p3 = Permission("test")
        self.p4 = Permission("test{0}1{0}hello".format(PERMISSION_DELIMITER))
        self.ps1 = {self.p1, self.p2}
        self.ps2 = {self.p1, self.p4}
        self.ps3 = {self.p1}

    def test_equal(self):
        self.assertEqual(self.p1, self.p4)
        self.assertNotEqual(self.p1, self.p2)
        self.assertNotEqual(self.p1, self.p3)
        self.assertEqual(self.ps2, self.ps3)

    def test_grants_permission(self):
        self.assertTrue(self.p1.grants_permission(self.p1))
        self.assertTrue(self.p1.grants_permission(self.p4))
        self.assertFalse(self.p1.grants_permission(self.p2))
        self.assertFalse(self.p1.grants_permission(self.p3))
        self.assertFalse(self.p3.grants_permission(self.p1))

    def test_grants_any_permission(self):
        self.assertTrue(self.p1.grants_any_permission(self.ps1))
        self.assertTrue(self.p2.grants_any_permission(self.ps1))
        self.assertFalse(self.p3.grants_any_permission(self.ps1))
        self.assertTrue(self.p4.grants_any_permission(self.ps1))

    def test_segments(self):
        self.assertEqual(self.p1.segments, ["test", "1", "hello"])
        self.assertEqual(self.p2.segments, ["test", "2", "hello"])
        self.assertEqual(self.p3.segments, ["test"])
        self.assertEqual(self.p1.segments, self.p4.segments)

if __name__ == "__main__":
    unittest.main()



