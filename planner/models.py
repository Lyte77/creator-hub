from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL

PLATFORM_CHOICES = [
    ("tiktok", "TikTok"),
    ("instagram", "Instagram"),
    ("youtube", "YouTube Shorts"),
]

STATUS_CHOICES = [
    ("draft",'Draft'),
    ("planned", "Planned"),
    ("posted", "Posted"),
]


class ContentTask(models.Model):
    """
    Core task representing a scheduled content item for a user.
    Lean, queryable, and ready for HTMX partial swaps.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="content_tasks")
    # optional link to an idea (set null when idea deleted)
    idea = models.ForeignKey(
        "ideas.Idea",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )

    title = models.CharField(max_length=255, blank=True)
    caption = models.TextField(blank=True)

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")

    scheduled_date = models.DateField(db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: store a simple ordering weight if you later add drag & drop ordering
    order = models.IntegerField(default=0, help_text="Sorting weight within the day")

    class Meta:
        ordering = ["scheduled_date", "order", "-created_at"]
        indexes = [
            models.Index(fields=["user", "scheduled_date"]),
            models.Index(fields=["user", "status"]),
        ]
        verbose_name = "Content Task"
        verbose_name_plural = "Content Tasks"

    def __str__(self):
        if self.title:
            return f"{self.title} — {self.platform} @ {self.scheduled_date}"
        return f"{self.platform} task @ {self.scheduled_date} (user {self.user_id})"

    @property
    def is_past_due(self):
        return self.scheduled_date < timezone.localdate()




