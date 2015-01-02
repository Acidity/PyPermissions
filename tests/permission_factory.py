import unittest
from permission import Permission, WildcardPermission
from factory import PermissionFactory


class PermissionFactoryTests(unittest.TestCase):

    def setUp(self):
        self.rpf = PermissionFactory()
        self.tpf = PermissionFactory(prefix="test")
        self.t2pf = self.rpf.create_child("test")
        self.ttpf = self.t2pf.create_child("2")
        self.thpf = self.tpf.create_child("hello")
        self.twpf = self.tpf.create_child("*")
        self.p1 = Permission("test.1.hello")
        self.p2 = Permission("test.2.hello")
        self.p3 = Permission("test")
        self.p4 = Permission("test.1.hello")
        self.p5 = WildcardPermission("test.*")

    def test_equal(self):
        self.assertEqual(self.p1, self.rpf.create_permission("test.1.hello"))
        self.assertNotEqual(self.p1, self.rpf.create_permission("test.2.hello"))
        self.assertEqual(self.p2, self.ttpf.create_permission("hello"))
        self.assertEqual(self.p2, self.tpf.create_permission("2.hello"))
        self.assertNotEqual(self.p5, self.twpf.create_permission(""))
        self.assertEqual(self.tpf, self.t2pf)
        self.assertNotEqual(self.tpf, self.ttpf)

if __name__ == "__main__":
    unittest.main()



