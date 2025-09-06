document.addEventListener('DOMContentLoaded', function() {
    const likeBtn = document.getElementById('like-btn');
    const dislikeBtn = document.getElementById('dislike-btn');
    const likeCount = document.getElementById('like-count');
    const dislikeCount = document.getElementById('dislike-count');

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function sendRating(action) {
        fetch(window.location.pathname + 'rate/', {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest"
            },
            body: new URLSearchParams({action})
        })
        .then(response => response.json())
        .then(data => {
            if(data.likes !== undefined) likeCount.textContent = data.likes;
            if(data.dislikes !== undefined) dislikeCount.textContent = data.dislikes;
        });
    }

    likeBtn.addEventListener('click', () => sendRating('like'));
    dislikeBtn.addEventListener('click', () => sendRating('dislike'));
});
