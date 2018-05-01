from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    headline = models.CharField(max_length=50)
    text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    submit_date = models.DateTimeField(default=timezone.now)
    title = models.TextField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comment(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.key})

    def __str__(self):
        return self.headline


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.PROTECT)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text


class Review(models.Model):
    post = models.ForeignKey('blog.Post', related_name='reviews', on_delete=models.PROTECT)
    author = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("review_list", kwargs={'pk': self.key})
