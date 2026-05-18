# Game Collection Manager 🎮

A professional, multi-user Flask web application designed for gamers to track, rate, and manage their personal game libraries.

## 🚀 Features

* **User Registration & Login:** Secure authentication implemented using Flask sessions.
* **Multi-user Isolation:** Data privacy is guaranteed; each user can only access their own collection.
* **Game Management (CRUD):** Full Add, View, Update status, and Delete functionality.
* **Rating & Reviews:** Integrated system for personal evaluations using ⭐ stars.
* **Status Tracking:** Effortlessly toggle between "Playing" and "Completed" states.
* **Dark Mode UI:** Professional minimalist design for an optimal user experience.

## 🛠️ Technologies Used

* **Backend:** Flask (Python)
* **Database:** SQLite with **Raw SQL** (No ORM used as per requirements).
* **Frontend:** HTML5, CSS3 (External stylesheet)
* **Testing:** Unit Testing for core business logic functions.

## 📁 Project Structure

```text
Game-Collection-Manager/
├── app.py              # Main application & routes
├── logic.py            # Business logic functions
├── static/             # CSS & Assets
├── templates/          # HTML files
└── tests/              # Unit tests