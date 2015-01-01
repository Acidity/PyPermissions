import unittest
from permission import Permission, WildcardPermission, PermissionSet, PERMISSION_DELIMITER, PERMISSION_WILDCARD


class PermissionSetTests(unittest.TestCase):

    def setUp(self):
        self.p1 = Permission("test{0}1{0}hello".format(PERMISSION_DELIMITER))
        self.p2 = Permission("test{0}2{0}hello".format(PERMISSION_DELIMITER))
        self.p3 = Permission("test")
        self.p4 = Permission("test{0}1{0}hello".format(PERMISSION_DELIMITER))
        self.p5 = WildcardPermission("test{0}{1}".format(PERMISSION_DELIMITER, PERMISSION_WILDCARD))
        self.ps1 = PermissionSet({self.p1, self.p2})
        self.ps2 = PermissionSet({self.p1, self.p4})
        self.ps3 = PermissionSet({self.p1})
        self.ps4 = PermissionSet({self.p3})

    def test_equal(self):
        self.assertEqual(self.ps2, self.ps3)

    def test_grants_permission(self):
        self.assertTrue(self.ps1.grants_permission(self.p1))
        self.assertTrue(self.ps1.grants_permission(self.p4))
        self.assertTrue(self.ps1.grants_permission(self.p2))
        self.assertFalse(self.ps1.grants_permission(self.p3))
        self.assertTrue(self.ps3.grants_permission(self.p1))

    def test_grants_any_permission(self):
        self.assertTrue(self.ps1.grants_any_permission(self.ps1))
        self.assertTrue(self.ps2.grants_any_permission(self.ps1))
        self.assertTrue(self.ps3.grants_any_permission(self.ps1))
        self.assertFalse(self.ps4.grants_any_permission(self.ps1))
        self.assertFalse(self.ps1.grants_any_permission(self.ps4))

    def test_has_any_permission(self):
        self.assertTrue(self.ps1.has_any_permission(self.p5))
        self.assertFalse(self.ps4.has_any_permission(self.p5))


if __name__ == "__main__":
    unittest.main()



