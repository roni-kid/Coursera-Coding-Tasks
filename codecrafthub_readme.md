# CodeCraftHub 🚀

Welcome to **CodeCraftHub**, a simple, beginner-friendly personalized learning platform backend built with **Python** and **Flask**. This project is designed for developers who want to master the fundamentals of **REST APIs** and HTTP methods without the complexity of setting up a heavy database or user authentication systems.

---

## 📌 Project Overview

CodeCraftHub acts as a digital logbook for developers to track the courses they want to learn, are currently taking, or have completed. It exposes a fully functional REST API that allows clients to perform **CRUD** operations (Create, Read, Update, Delete) while persisting all data locally in a plain JSON text file.

---

## ✨ Features

- **Full CRUD Support:** Create, read, update, and delete courses via clean REST endpoints.
- **JSON File Persistence:** No database required! Data is saved automatically to a `courses.json` file.
- **Auto-Initialization:** The application automatically creates the data file if it doesn't exist yet.
- **Smart Data Tracking:** Each course automatically tracks a unique ID, creation timestamp, and strict status validation.
- **Robust Error Handling:** Clear, user-friendly error messages for missing fields, invalid status values, or missing resources.

---

## 🛠️ Step-by-Step Installation Instructions

Follow these steps to get CodeCraftHub up and running on your local machine:

### Prerequisites
Make sure you have **Python 3.x** installed on your computer. You can check your Python version by running this command in your terminal:
```bash
python --version
```

### Step 1: Set Up Your Project Folder
1. Create a new folder on your computer named `CodeCraftHub`.
2. Open that folder in your code editor (like VS Code).

### Step 2: Install Flask
Flask is the micro-web framework we use to build our API. Install it using pip:
```bash
pip install Flask
```

### Step 3: Add the Project Files
Create two files inside your `CodeCraftHub` folder:
1. `app.py` — Paste your Flask backend code here.
2. `requirements.txt` — (Optional) Add `Flask` to this file to track dependencies.

---

## 🚀 How to Run the Application

1. Open your terminal or command prompt and navigate to your `CodeCraftHub` folder.
2. Start the Flask application by running:
   ```bash
   python app.py
   ```
3. You should see output in your terminal indicating that the development server is running, usually at:
   ```text
   http://127.0.0.1:5000
   ```
4. Keep this terminal window open while you test your API! (The `courses.json` file will automatically appear in your folder the first time you add a course).

---

## 🌐 API Endpoints Documentation

CodeCraftHub exposes the following REST endpoints:

| HTTP Method | Endpoint | Description | Request Body Required? |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/courses` | Retrieve all saved courses | No |
| **POST** | `/api/courses` | Add a brand new course | Yes (JSON) |
| **GET** | `/api/courses/<id>` | Retrieve a specific course by ID | No |
| **PUT** | `/api/courses/<id>` | Update an existing course | Yes (JSON) |
| **DELETE** | `/api/courses/<id>` | Delete a course by ID | No |

### Detailed Payload & Response Examples

#### 1. Add a Course (`POST /api/courses`)
* **Headers:** `Content-Type: application/json`
* **JSON Body:**
  ```json
  {
    "name": "Python REST APIs with Flask",
    "description": "Learn how to build lightweight backends and JSON endpoints.",
    "target_date": "2026-12-01",
    "status": "Not Started"
  }
  ```
* **Success Response (`201 Created`):**
  ```json
  {
    "id": 1,
    "name": "Python REST APIs with Flask",
    "description": "Learn how to build lightweight backends and JSON endpoints.",
    "target_date": "2026-12-01",
    "status": "Not Started",
    "created_at": "2026-10-14 22:45:00"
  }
  ```

#### 2. Get All Courses (`GET /api/courses`)
* **Success Response (`200 OK`):** Returns an array containing all course objects.

#### 3. Update a Course (`PUT /api/courses/1`)
* **JSON Body (Only include fields you want to change):**
  ```json
  {
    "status": "In Progress"
  }
  ```
* **Success Response (`200 OK`):** Returns the fully updated course object.

#### 4. Delete a Course (`DELETE /api/courses/1`)
* **Success Response (`200 OK`):**
  ```json
  {
    "message": "Course with ID 1 deleted successfully."
  }
  ```

---

## 🧪 Testing Instructions

You can test your API using tools like **Postman**, **Thunder Client** (VS Code extension), or directly from your terminal using **cURL**.

### Example cURL Commands (Linux/macOS/Git Bash):
- **Get all courses:**
  ```bash
  curl -X GET http://127.0.0.1:5000/api/courses
  ```
- **Add a course:**
  ```bash
  curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name": "Flask Basics", "description": "Intro to routing", "target_date": "2026-11-15", "status": "Not Started"}'
  ```

---

## 📂 Project Structure Explanation

Your file workspace should look like this:

```text
CodeCraftHub/
│
├── app.py          # Main application file containing all routes & logic
├── courses.json    # Local data store (created automatically on first run)
└── requirements.txt # Project dependencies list
```

- **`app.py`**: The heart of your application. It handles incoming HTTP requests, processes data, interacts with the JSON storage file, and sends back JSON responses.
- **`courses.json`**: Acts as your "database table". It stores all courses as an array of structured JSON objects.

---

## 🔍 Troubleshooting Common Issues

1. **`ModuleNotFoundError: No module named 'flask'`**
   * *Fix:* You haven't installed Flask in your current Python environment. Run `pip install Flask`.
2. **Port 5000 is already in use**
   * *Fix:* Another application is using port 5000. You can stop that process or modify the bottom of `app.py` to run on a different port (e.g., `app.run(debug=True, port=8000)`).
3. **JSONDecodeError / Corrupted File Error**
   * *Fix:* If you accidentally delete a bracket or quote in `courses.json`, it may become invalid JSON. The app is built to handle this by resetting the file, but you can also manually delete `courses.json` and let the app recreate a fresh one.