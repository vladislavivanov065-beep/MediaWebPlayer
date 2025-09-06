from django.shortcuts import render, get_object_or_404, redirect
from .models import Video
import requests

def home(request):
    return render(request, "core/home.html")

def video_player(request):
    if request.method == "POST":

        # Удаление видео по ID
        delete_id = request.POST.get("delete_id")
        if delete_id:
            try:
                video_to_delete = Video.objects.get(pk=int(delete_id))
                video_to_delete.delete()
            except Video.DoesNotExist:
                pass
            return redirect("video_player")

        # Добавление нового видео
        url = request.POST.get("rutube_url")
        title_input = request.POST.get("title")       # из формы
        author_input = request.POST.get("author")     # из формы

        if url:
            rutube_id = None

            # Извлечение rutube_id из ссылки
            if "rutube.ru/video/" in url:
                rutube_id = url.split("rutube.ru/video/")[-1].split("/")[0]
            elif "rutube.ru/play/embed/" in url:
                rutube_id = url.split("rutube.ru/play/embed/")[-1].split("/")[0]

            thumbnail_url = ""
            video_title = title_input or "Без названия"
            video_author = author_input or "Неизвестен"

            if rutube_id:
                api_url = f"https://rutube.ru/api/video/{rutube_id}/?format=json"
                try:
                    resp = requests.get(api_url, timeout=5)
                    if resp.status_code == 200:
                        data = resp.json()
                        # Название видео
                        video_title = data.get("title", video_title)
                        # Автор видео
                        author_data = data.get("author")
                        if isinstance(author_data, dict):
                            video_author = author_data.get("name", video_author)
                        elif isinstance(author_data, str):
                            video_author = author_data
                        else:
                            video_author = video_author
                        # Миниатюра
                        thumbnail_url = data.get("thumbnail_url", "")
                except Exception as e:
                    print("Ошибка при получении данных Rutube:", e)

            # Если миниатюра не доступна, ставим placeholder
            if not thumbnail_url:
                thumbnail_url = f"https://via.placeholder.com/320x180?text={video_title}"

            # Сохраняем видео
            Video.objects.create(
                url=url,
                title=video_title,
                author=video_author,
                thumbnail=thumbnail_url
            )

            return redirect("video_player")

    videos = Video.objects.all()
    return render(request, "core/video_player.html", {"videos": videos})

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, "core/video_detail.html", {"video": video})
