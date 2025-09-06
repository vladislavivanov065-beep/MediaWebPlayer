from django.db import models

class Video(models.Model):
    url = models.URLField("Ссылка на видео")
    title = models.CharField("Название видео", max_length=255, blank=True)
    author = models.CharField("Автор", max_length=255)
    thumbnail = models.URLField("Миниатюра", blank=True, null=True)

    def __str__(self):
        return f"{self.title or self.url} — {self.author}"

    @property
    def rutube_id(self):
        if "rutube.ru/video/" in self.url:
            return self.url.split("rutube.ru/video/")[-1].split("/")[0]
        if "rutube.ru/play/embed/" in self.url:
            return self.url.split("rutube.ru/play/embed/")[-1].split("/")[0]
        return None

    @property
    def thumbnail_url(self):
        if self.rutube_id:
            return f"https://rutube.ru/api/video/{self.rutube_id}/thumbnail/"
        return "https://via.placeholder.com/320x180?text=No+Preview"

from django.db import models

class VideoRating(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='ratings')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.video.title} — {self.likes}👍 / {self.dislikes}👎"

# Новая модель для фиксации каждого лайка/дизлайка
class VideoVote(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    VOTE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    ]

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=7, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.video.title} — {self.vote_type}"

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=255, default="Аноним")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.text[:20]}"