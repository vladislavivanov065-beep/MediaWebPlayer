# MediaWebPlayer

A Django-based web application for managing and viewing Rutube videos with a clean and responsive interface.

---

## Features

- **Add videos by URL:** Add Rutube videos by pasting their link. The app automatically fetches the **title**, **author**, and **thumbnail** from Rutube.
- **Delete videos:** Remove videos from the database by entering their ID.
- **Responsive video grid:**
  - The top **8 videos** are displayed in a **4x2 grid** on wide screens.
  - Remaining videos appear in a **vertical list** below the grid.
- **Automatic thumbnail handling:** If a Rutube thumbnail is unavailable, a placeholder image is shown.
- **Compact video cards:** Minimized spacing between thumbnails and text for a clean layout.
- **Fallbacks:** If the Rutube API fails, the app uses values entered manually in the form.

---

## Project Structure

mediawebplayer/
├── core/
│ ├── migrations/
│ ├── models.py
│ ├── views.py
│ ├── static/
│ │ └── core/
│ │ └── css/
│ │ └── style.css
│ ├── templates/
│ │ └── core/
│ │ └── video_player.html
├── mediawebplayer/
│ └── settings.py
├── manage.py


- **core/models.py:** Defines the `Video` model with fields for URL, title, author, and thumbnail.  
- **core/views.py:** Handles video addition, deletion, and fetching data from Rutube API.  
- **core/templates/core/video_player.html:** Main interface for viewing, adding, and deleting videos.  
- **core/static/core/css/style.css:** Styling for responsive grids and video cards.

---

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd mediawebplayer

2. Create and activate a virtual environment:
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Apply migrations:
python manage.py migrate

5. Run the development server:
python manage.py runserver

6. Open your browser and go to:
http://127.0.0.1:8000/player/

Usage

Add video: Enter the Rutube video URL, optional title, and author (fallback) in the top form. Click Add.
Delete video: Enter the video ID in the delete form and click Delete.
View videos: Top 8 videos are shown in a 4x2 grid; remaining videos are listed below. Click on any video to open it for playback.

Notes

Video thumbnails are fetched from Rutube API. If the API fails or the video is private, a placeholder is displayed.
The app automatically extracts the video ID from Rutube links to fetch metadata.
Supports responsive layout for desktop, tablet, and mobile.

Screenshots
(Optional: You can add screenshots of your grid and list view here.)

License
This project is open-source and free to use.