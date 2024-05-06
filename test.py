import unittest
import data_conn as dc


class TestCliFeature(unittest.TestCase):

    def setUp(self) -> None:
        dc.DB = "cli_test"
        dc.create_database()

    # def test_user_insertion(self):
    #     user1 = ("Dembe", "dembe@black.list", "ddddd", 1)
    #     user2 = ("Shelby", "shelby@peaky.com", "1a2b3c", 0)
    #     self.assertTrue(dc.insert_user(*user1))
    #     self.assertTrue(dc.insert_user(*user2))

    # def test_insert_task(self):
    #     tsk1 = ("test et integration",
    #             "terminer le projet de test et integration",
    #             0, 2)
    #     tsk2 = ("push up",
    #             "en faire 30 chaque jour", 0, 2)
    #     self.assertTrue(dc.insert_tasks(*tsk1))
    #     self.assertTrue(dc.insert_tasks(*tsk2))

    # def test_delete_task(self):
    #     self.assertTrue(dc.delete_task(2, 2))

    def test_set_task_done(self):
        self.assertTrue(dc.set_task_done(1, 2))


if __name__ == "__main__":
    unittest.main()
