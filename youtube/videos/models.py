from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def display_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        # Return empty string if no thumbnail - template will handle fallback
        return ""

    @property
    def video_url(self):
        if self.video_file:
            return self.video_file.url
        return ""

    def delete(self, *args, **kwargs):
        # Delete files when model is deleted
        if self.video_file:
            self.video_file.delete()
        if self.thumbnail:
            self.thumbnail.delete()
        super().delete(*args, **kwargs)


class VideoLike(models.Model):
    LIKE = 1
    DISLIKE = -1
    LIKE_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="user_likes")
    value = models.SmallIntegerField(choices=LIKE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "video"]

    def __str__(self):
        action = "liked" if self.value == self.LIKE else "disliked"
        return f"{self.user.username} {action} {self.video.title}"