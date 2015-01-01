import unittest
from permission import Permission, WildcardPermission, PERMISSION_DELIMITER, PERMISSION_WILDCARD


class WildcardPermissionTests(unittest.TestCase):

    def setUp(self):
        self.p1 = WildcardPermission("test{0}1{0}{1}".format(PERMISSION_DELIMITER, PERMISSION_WILDCARD))
        self.p2 = Permission("test{0}2{0}hello".format(PERMISSION_DELIMITER))
        self.p3 = Permission("test")
        self.p4 = WildcardPermission("test{0}1{0}{1}".format(PERMISSION_DELIMITER, PERMISSION_WILDCARD))
        self.p5 = Permission("test{0}1{0}goodbye".format(PERMISSION_DELIMITER))
        self.p6 = Permission("test{0}1".format(PERMISSION_DELIMITER))
        self.p7 = WildcardPermission("*")
        self.p8 = WildcardPermission("test{0}{1}{0}hello".format(PERMISSION_DELIMITER, PERMISSION_WILDCARD))
        self.ps1 = {self.p1, self.p2}
        self.ps2 = {self.p1, self.p4}
        self.ps3 = {self.p1}

    def test_grants_permission(self):
        self.assertTrue(self.p1.grants_permission(self.p1))
        self.assertTrue(self.p1.grants_permission(self.p4))
        self.assertFalse(self.p1.grants_permission(self.p2))
        self.assertFalse(self.p1.grants_permission(self.p3))
        self.assertFalse(self.p3.grants_permission(self.p1))
        self.assertTrue(self.p1.grants_permission(self.p5))
        self.assertFalse(self.p1.grants_permission(self.p6))
        self.assertTrue(self.p7.grants_permission(self.p1))
        self.assertTrue(self.p7.grants_permission(self.p2))
        self.assertTrue(self.p7.grants_permission(self.p3))
        self.assertTrue(self.p7.grants_permission(self.p4))
        self.assertTrue(self.p7.grants_permission(self.p5))
        self.assertTrue(self.p7.grants_permission(self.p6))
        self.assertTrue(self.p8.grants_permission(self.p2))
        self.assertFalse(self.p8.grants_permission(self.p1))

    def test_is_end_wildcard(self):
        self.assertTrue(self.p1.is_end_wildcard)
        self.assertTrue(self.p4.is_end_wildcard)
        self.assertTrue(self.p7.is_end_wildcard)
        self.assertFalse(self.p8.is_end_wildcard)

if __name__ == "__main__":
    unittest.main()



