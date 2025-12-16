from django.test import TestCase
from django.contrib.auth import get_user_model
from planner.models import ContentTask
from datetime import date, timedelta
from ideas.models import Idea

User = get_user_model()
    
class PlannerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="tester@example.com", password="pass1234")

    def test_create_task_from_idea(self):
        idea = Idea.objects.create(user=self.user, content="Video idea: My dev flow")
        scheduled = date.today() + timedelta(days=2)
        task = ContentTask.objects.create(
            user=self.user,
            idea=idea,
            title="Dev Flow Clip",
            caption="Short caption",
            platform="tiktok",
            scheduled_date=scheduled
        )
        self.assertEqual(task.idea, idea)
        self.assertFalse(task.is_past_due)
        qs = ContentTask.objects.filter(user=self.user, scheduled_date=scheduled)
        self.assertEqual(qs.count(), 1)
