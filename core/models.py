from django.db import models

class Video(models.Model):
    url = models.URLField("Ссылка на видео")
    title = models.CharField("Название видео", max_length=255, blank=True)  # новое поле
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
        """Формируем ссылку на миниатюру Rutube по ID"""
        if self.rutube_id:
            return f"https://rutube.ru/api/video/{self.rutube_id}/thumbnail/"
        return "https://via.placeholder.com/320x180?text=No+Preview"
