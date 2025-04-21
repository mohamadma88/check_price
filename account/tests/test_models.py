from rest_framework.test import APITestCase
from account.models import User, Otp, Profile
from django.utils.translation import gettext_lazy as _


class UserModelTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(phone='11223344556', password='1234')

    def test_user_creation(self):
        self.assertEqual(self.user.phone, '11223344556')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin)

    def test_str_method(self):
        self.assertEqual(str(self.user), '11223344556')

    def test_has_perm(self):
        self.assertTrue(self.user.has_perm('some_permission'))

    def test_is_staff_property(self):
        self.user.is_admin = True
        self.assertTrue(self.user.is_staff)

    def test_user_uniqueness(self):
        with self.assertRaises(Exception):
            User.objects.create_user(phone='11223344556', password='4321')


class OtpModelTest(APITestCase):

    def setUp(self):
        self.otp = Otp.objects.create(phone='11223344556', code=123456, token='sdfgsdgfdsfgsdg')

    def test_wallet_field_label(self):
        field_label = self.otp._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, _('شماره تلفن'))

    def test_code_field_label(self):
        field_label = self.otp._meta.get_field('code').verbose_name
        self.assertEqual(field_label, _('کد ارسال شده'))

    def test_token_field_label(self):
        field_label = self.otp._meta.get_field('token').verbose_name
        self.assertEqual(field_label, _('توکن'))

    def test_str_method(self):
        self.assertEqual(str(self.otp), self.otp.phone)


class ProfileModelTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(phone='11223344556', password='1234')
        cls.profile = Profile.objects.create(phone=cls.user, name='mohamad', last_name='mmm', birthday='2000-12-22',
                                             melicode='2233441155', bank='1122334455667788')

    def test_phone_field_label(self):
        field_label = self.profile._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, _('شماره تفن'))

    def test_phone_field_label(self):
        field_label = self.profile._meta.get_field('name').verbose_name
        self.assertEqual(field_label, _('نام'))

    def test_phone_field_label(self):
        field_label = self.profile._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, _('نام خانوادگی'))

    def test_phone_field_label(self):
        field_label = self.profile._meta.get_field('birthday').verbose_name
        self.assertEqual(field_label, _('تاریخ تولد'))

    def test_phone_field_label(self):
        field_label = self.profile._meta.get_field('melicode').verbose_name
        self.assertEqual(field_label, _('کد ملی'))

    def test_phone_field_label(self):
        field_label = self.profile._meta.get_field('bank').verbose_name
        self.assertEqual(field_label, _('شماره کارت'))
