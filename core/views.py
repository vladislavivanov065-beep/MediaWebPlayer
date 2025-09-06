from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, VideoRating, VideoVote, Comment
import requests
from django.http import JsonResponse

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
        title_input = request.POST.get("title")
        author_input = request.POST.get("author")

        if url:
            rutube_id = None
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
                        video_title = data.get("title", video_title)
                        author_data = data.get("author")
                        if isinstance(author_data, dict):
                            video_author = author_data.get("name", video_author)
                        elif isinstance(author_data, str):
                            video_author = author_data
                        thumbnail_url = data.get("thumbnail_url", "")
                except Exception as e:
                    print("Ошибка при получении данных Rutube:", e)

            if not thumbnail_url:
                thumbnail_url = f"https://via.placeholder.com/320x180?text={video_title}"

            video = Video.objects.create(
                url=url,
                title=video_title,
                author=video_author,
                thumbnail=thumbnail_url
            )

            # Создаем объект рейтинга для видео
            VideoRating.objects.create(video=video)

            return redirect("video_player")

    videos = Video.objects.all()
    return render(request, "core/video_player.html", {"videos": videos})

def video_rate_ajax(request, pk):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        video = get_object_or_404(Video, pk=pk)
        rating, _ = VideoRating.objects.get_or_create(video=video)

        action = request.POST.get("action")
        if action == "like":
            rating.likes += 1
        elif action == "dislike":
            rating.dislikes += 1
        rating.save()

        return JsonResponse({"likes": rating.likes, "dislikes": rating.dislikes})
    return JsonResponse({"error": "Invalid request"}, status=400)

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)

    # Получаем объект рейтинга для видео
    rating, _ = VideoRating.objects.get_or_create(video=video)

    if request.method == "POST":
        # Лайк
        if "like" in request.POST:
            rating.likes += 1
            rating.save()
            return redirect("video_detail", pk=pk)

        # Дизлайк
        if "dislike" in request.POST:
            rating.dislikes += 1
            rating.save()
            return redirect("video_detail", pk=pk)

        # Новый комментарий
        comment_text = request.POST.get("comment_text")
        comment_author = request.POST.get("comment_author") or "Аноним"
        if comment_text:
            Comment.objects.create(
                video=video,
                author=comment_author,
                text=comment_text
            )
            return redirect("video_detail", pk=pk)

    comments = video.comments.order_by("-created_at")
    context = {
        "video": video,
        "rating": rating,
        "comments": comments
    }
    return render(request, "core/video_detail.html", context)

def video_rate_ajax(request, pk):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Получаем видео по pk
        video = get_object_or_404(Video, pk=pk)

        # Получаем или создаём суммарный рейтинг
        rating, _ = VideoRating.objects.get_or_create(video=video)

        # Получаем действие из POST
        action = request.POST.get("action")
        if action == "like":
            rating.likes += 1
            VideoVote.objects.create(video=video, vote_type=VideoVote.LIKE)
        elif action == "dislike":
            rating.dislikes += 1
            VideoVote.objects.create(video=video, vote_type=VideoVote.DISLIKE)

        # Сохраняем суммарный рейтинг
        rating.save()

        # Возвращаем JSON с обновлёнными счётчиками
        return JsonResponse({"likes": rating.likes, "dislikes": rating.dislikes})

    return JsonResponse({"error": "Invalid request"}, status=400)

def add_comment(request, pk):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        video = get_object_or_404(Video, pk=pk)
        author = request.POST.get("comment_author") or "Аноним"
        text = request.POST.get("comment_text")

        if text.strip():
            comment = Comment.objects.create(video=video, author=author, text=text)
            return JsonResponse({
                "author": comment.author,
                "text": comment.text,
                "created_at": comment.created_at.strftime("%d.%m.%Y %H:%M")
            })

    return JsonResponse({"error": "Неверный запрос"}, status=400)

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    rating, _ = VideoRating.objects.get_or_create(video=video)
    comments = video.comments.all().order_by('-created_at')  # последние сверху

    # Обработка комментариев
    if request.method == "POST" and "comment_text" in request.POST:
        author = request.POST.get("comment_author") or "Аноним"
        text = request.POST.get("comment_text")
        if text:
            Comment.objects.create(video=video, author=author, text=text)
            return redirect('video_detail', pk=video.pk)

    return render(request, "core/video_detail.html", {
        "video": video,
        "rating": rating,
        "comments": comments
    })
