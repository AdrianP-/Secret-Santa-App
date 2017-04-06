import json

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from usersenders.models import UserSender


class UserSenderRegistrationAPIViewTestCase(APITestCase):
    url = reverse("usersenders:register")

    def test_userSender_registration(self):
        """
        Test to verify that a post call with userSender valid data
        """
        userSender_data = {
            "name": "testuserSender",
            "age": 54,
            "group": "grupo1",
        }
        response = self.client.post(self.url, userSender_data)
        self.assertEqual(201, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

    def test_unique_userSendername_validation(self):
        """
        Test to verify that a post call with already exists name
        """
        userSender_data_1 = {
            "name": "testuserSender",
            "age": 54,
            "group": "grupo1",
        }
        response = self.client.post(self.url, userSender_data_1)
        self.assertEqual(201, response.status_code)

        userSender_data_2 = {
            "name": "testuserSender",
            "age": 22,
            "group": "grupo1",
        }
        response = self.client.post(self.url, userSender_data_2)
        self.assertEqual(400, response.status_code)

class UserSenderGetGiftess(APITestCase):

    def setUp(self):
        self.userSender = UserSender.objects._create_sender_user("Adrian", 23, "grupo1")
        self.userSender2 = UserSender.objects._create_sender_user("Juan", 34, "grupo1")
        self.userSender3 = UserSender.objects._create_sender_user("Dan", 12, "grupo1")
        self.userSender4 = UserSender.objects._create_sender_user("Smith", 63, "grupo3")
        self.userSender5 = UserSender.objects._create_sender_user("John", 74, "grupo1")
        self.userSender6 = UserSender.objects._create_sender_user("Smith_2", 63, "grupo3")

    def test_get_by_name(self):
        user = UserSender.objects.get_by_name("Adrian")
        self.assertEqual(self.userSender, user)

    def test_get_all_users(self):
        self.assertEqual(6, UserSender.objects.count())

    def test_get_all_users_same_group(self):
        self.assertEqual(4, UserSender.objects.get_by_group("grupo1").count())

    def test_make_giftees(self):
        """
        The function make_giftees makes a perfect cicle, so it can't happen
            A -> B
            B -> A
        """
        mixed = UserSender.objects.make_giftees("grupo1")
        for key in mixed:
            A = mixed[key]
            B = mixed[A]
            self.assertNotEqual(key, A)
            self.assertNotEqual(A, B)


    def test_save_giftees(self):
        """
        Once a pairing was generated, it's necessary persist them
        """
        giftees = UserSender.objects.make_giftees("grupo1")
        UserSender.objects.save_giftees(giftees)

        for user in UserSender.objects.get_by_group("grupo1"):
            self.assertFalse(user.isEmpty_send_to())

    def test_get_giftees_uninitialized(self):
        """
        The function get_giftee(user) make the pairing, persist and update the user object
        """
        user = self.userSender
        self.assertTrue(user.isEmpty_send_to())

        UserSender.objects.get_giftee(user)
        self.assertFalse(user.isEmpty_send_to())

    def test_get_giftees_initialized(self):
        giftees = UserSender.objects.make_giftees("grupo1")
        UserSender.objects.save_giftees(giftees)
        user = UserSender.objects.get_by_name("Adrian")

        self.assertEqual(user.send_to,UserSender.objects.get_giftee(user))


class UserSenderGetGifteeAPIViewTestCase(APITestCase):
    """
    This class test the functions of UserSenderGetGiftess through the View
    """
    url = reverse("usersenders:getGiftee")

    def setUp(self):
        self.userSender = UserSender.objects._create_sender_user("Adrian", 23, "grupo1")
        self.userSender2 = UserSender.objects._create_sender_user("Juan", 34, "grupo1")
        self.userSender3 = UserSender.objects._create_sender_user("Dan", 12, "grupo1")
        self.userSender4 = UserSender.objects._create_sender_user("Smith", 63, "grupo3")
        self.userSender5 = UserSender.objects._create_sender_user("John", 74, "grupo1")

    def test_post(self):
        response = self.client.post(self.url, {"name": "Juan"})
        self.assertEqual(200, response.status_code)

    def test_incorrect_post_name(self):
        response = self.client.post(self.url, {"name": "uuuuu"})
        self.assertEqual(400, response.status_code)

    def test_get_send_to(self):
        name = "Adrian"
        response = self.client.post(self.url, {"name": name})
        user = UserSender.objects.get_by_name(name)
        self.assertEqual({"send_to": user.send_to}, json.loads(response.content))
