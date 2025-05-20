from django.test import TestCase
from django.contrib.auth.models import User
from .models import SubscriptionPlan, UserSubscription, PlanFeature
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

# Create your tests here.
class SubscriptionPlanTests(TestCase):
    def setUp(self):
        self.plan = SubscriptionPlan.objects.create(
            plan_name="Test Plan",
            plan_price=10.00,
            plan_period="monthly",
            is_active=True
        )
        self.feature = PlanFeature.objects.create(
            plan=self.plan,
            feature_name="Test Feature",
            feature_limit=100
        )

    def test_plan_creation(self):
        self.assertEqual(self.plan.plan_name, "Test Plan")
        self.assertEqual(self.plan.plan_price, 10.00)
        self.assertEqual(self.plana.plan_period, "monthly")
        self.assertTrue(self.plan.is_active)

    def test_feature_creation(self):
        self.assertEqual(self.feature.feature_name, "Test Feature")
        self.assertEqual(self.feture.feature_limit, 100)
        self.assertTrue(self.feature.is_active)

    def test_plan_details(self):
        details = self.plan.get_plan_details()
        self.assertEqual(details['plan_name'], "Test Plan")
        self.assertEqual(details['plan_price'], 10.00)
        self.assertEqual(details['plan_period'], "monthly")
        self.assertTrue(details['is_active'])

    def test_feature_count(self):
        self.assertEqual(self.plan.feature_count(), 1)

    def test_feature_accessible(self):
        self.assertTrue(self.plan.feature_accessible("Test Feature"))

    def test_feature_limit(self):
        self.assertEqual(self.plan.feature_limit("Test Feature"), 100)

    def test_plan_duration_days(self):
        self.assertEqual(self.plan.get_plan_duration_days(), 30)

    def test_expiry_date(self):
        self.assertEqual(self.plan.get_expiry_date(), timezone.now() + timedelta(days=30))

    def test_feature_count(self):
        self.assertEqual(self.plan.feature_count(), 1)

    def test_feature_accessible(self):
        self.assertTrue(self.plan.feature_accessible("Test Feature"))

    def test_feature_limit(self):
        self.assertEqual(self.plan.feature_limit("Test Feature"), 100)

    def test_plan_price_display(self):
        self.assertEqual(self.plan.get_price_display(), "10.00 USD")

    def test_plan_to_dict(self):
        data = self.plan.to_dict()
        self.assertEqual(data['plan_name'], "Test Plan")
        self.assertEqual(data['plan_price'], 10.00)
        self.assertEqual(data['plan_period'], "monthly")
        self.assertTrue(data['is_active'])

    def test_user_subscription_creation(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )
        self.assertEqual(subscription.user, user)
        self.assertEqual(subscription.plan, self.plan)
        self.assertEqual(subscription.stripe_subscription_id, "sub_1234567890")

    def test_user_subscription_to_dict(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )   
        data = subscription.to_dict()
        self.assertEqual(data['user_id'], user.id)
        self.assertEqual(data['plan_id'], self.plan.plan_id)
        self.assertEqual(data['stripe_subscription_id'], "sub_1234567890")

    def test_user_subscription_status(self):    
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )   
        self.assertTrue(subscription.is_active)

    def test_user_subscription_usage(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,  
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )
        self.assertEqual(subscription.usage_start_date, timezone.now())

    def test_user_subscription_usage_limits(self):  
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )   
        self.assertEqual(subscription.usage_limits(), self.plan.feature_limit("Test Feature"))

    def test_user_subscription_usage_history(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )   
        self.assertEqual(subscription.usage_history(), [])

    def test_user_subscription_usage_limits(self):  
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )      
        self.assertEqual(subscription.usage_limits(), self.plan.feature_limit("Test Feature"))

    def test_user_subscription_usage_history(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )   
        self.assertEqual(subscription.usage_history(), [])

    def test_user_subscription_usage_limits(self):    
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )      
        self.assertEqual(subscription.usage_limits(), self.plan.feature_limit("Test Feature"))

    def test_user_subscription_usage_history(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )   
        self.assertEqual(subscription.usage_history(), [])

    def test_user_subscription_usage_limits(self):      
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )      
        self.assertEqual(subscription.usage_limits(), self.plan.feature_limit("Test Feature"))

    def test_user_subscription_usage_history(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        subscription = UserSubscription.objects.create(
            user=user,
            plan=self.plan,
            stripe_subscription_id="sub_1234567890"
        )   
        self.assertEqual(subscription.usage_history(), [])              

