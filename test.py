import unittest
import connection as dc


class TestCliFeature(unittest.TestCase):

    def setUp(self) -> None:
        dc.DB = "cli_test.db"
        dc.create_tables()

<<<<<<< HEAD
    def test_user_insertion(self):
=======
    def test_a_user_insertion(self):
>>>>>>> 25ce4bbda1e13006211d268f547428353c3bd959
        user1 = ("Dembe", "dembe@black.list", "ddddd", 1)
        user2 = ("Shelby", "shelby@peaky.com", "1a2b3c", 0)
        self.assertTrue(dc.insert_user(*user1))
        self.assertTrue(dc.insert_user(*user2))

<<<<<<< HEAD
    def test_insert_task(self):
        tsk1 = ("test et integration",
                "terminer le projet de test et integration",
                0, 2)
        tsk2 = ("push up",
                "en faire 30 chaque jour", 0, 2)
        self.assertTrue(dc.insert_tasks(*tsk1))
        self.assertTrue(dc.insert_tasks(*tsk2))

    def test_delete_task(self):
        self.assertTrue(dc.delete_task(2, 2))
=======
    def test_b_insert_task(self):
        tsk1 = ("test et integration",
                "terminer le projet de test et integration",
                0, 2)
        self.assertTrue(dc.insert_tasks(*tsk1))

    def test_c_delete_task(self):
        tsk2 = ("push up",
                "en faire 30 chaque jour", 0, 2)
        self.assertTrue(dc.insert_tasks(*tsk2))
        self.assertTrue(dc.delete_task(1, 2))
>>>>>>> 25ce4bbda1e13006211d268f547428353c3bd959

    def test_d_set_task_done(self):
        self.assertTrue(dc.set_task_done(2, 2))

    def test_e_get_stats(self):
        total, done = dc.get_stats(2)
        # print("->", dc.get_stats(1))
        self.assertEqual(total, 1)
        self.assertEqual(done, 1)


if __name__ == "__main__":
    unittest.main()
