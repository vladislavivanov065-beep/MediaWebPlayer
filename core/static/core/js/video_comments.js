document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("comment-form");
    const commentList = document.getElementById("comment-list");
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch(window.location.pathname + "comment/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest"
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) return;

            // Создаём новый комментарий
            const newComment = document.createElement("div");
            newComment.classList.add("comment");
            newComment.innerHTML = `<strong>${data.author}:</strong> <span>${data.text}</span>`;

            // Добавляем в начало списка
            commentList.prepend(newComment);

            // Очищаем форму
            form.reset();
        });
    });
});
