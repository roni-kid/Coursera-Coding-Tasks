from datetime import datetime
import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Name of the JSON file used for data storage
DATA_FILE = "courses.json"

# Allowed values for the course status field
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]


# ==========================================
# HELPER FUNCTIONS FOR JSON DATA MANAGEMENT
# ==========================================


def load_courses():
  """Loads all courses from the courses.json file.

  If the file does not exist, it creates it automatically with an empty list.
  Handles file read errors and corrupted JSON data gracefully.
  """
  try:
    # Check if the file exists; if not, create it with an empty list
    if not os.path.exists(DATA_FILE):
      save_courses([])
      return []

    with open(DATA_FILE, "r") as file:
      return json.load(file)

  except json.JSONDecodeError:
    # Handle file corruption error
    print("Warning: courses.json was corrupted. Resetting file content.")
    save_courses([])
    return []
  except IOError as e:
    # Handle operating system / file permission errors
    print(f"File read error occurred: {e}")
    raise RuntimeError("Failed to read data from the storage file.")


def save_courses(courses):
  """Saves the provided list of courses to the courses.json file.

  Handles file write errors.
  """
  try:
    with open(DATA_FILE, "w") as file:
      # indent=4 makes the JSON file human-readable
      json.dump(courses, file, indent=4)
  except IOError as e:
    print(f"File write error occurred: {e}")
    raise RuntimeError("Failed to save data to the storage file.")


# ==========================================
# REST API ENDPOINTS
# ==========================================


@app.route("/api/courses", methods=["GET"])
def get_courses():
  """GET /api/courses

  Retrieves a list of all saved courses.
  """
  try:
    courses = load_courses()
    return jsonify(courses), 200
  except RuntimeError as e:
    return jsonify({"error": str(e)}), 500


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
  """GET /api/courses/<course_id>

  Retrieves a single specific course by its unique ID.
  """
  try:
    courses = load_courses()
    # Find the course matching the ID
    course = next((c for c in courses if c["id"] == course_id), None)

    # Error handling: Course not found
    if not course:
      return jsonify({"error": f"Course with ID {course_id} not found."}), 404

    return jsonify(course), 200
  except RuntimeError as e:
    return jsonify({"error": str(e)}), 500


@app.route("/api/courses", methods=["POST"])
def add_course():
  """POST /api/courses

  Adds a new course to the system with full validation checks.
  """
  try:
    data = request.get_json()

    # Ensure JSON body was provided
    if not data:
      return jsonify({"error": "Request body must be valid JSON."}), 400

    # 1. Error handling: Check for missing required fields
    required_fields = ["name", "description", "target_date", "status"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
      return (
          jsonify({
              "error": (
                  "Missing required fields:"
                  f" {', '.join(missing_fields)}"
              )
          }),
          400,
      )

    # 2. Error handling: Validate status values
    status = data.get("status")
    if status not in VALID_STATUSES:
      return (
          jsonify({
              "error": (
                  f"Invalid status '{status}'. Must be one of:"
                  f" {', '.join(VALID_STATUSES)}"
              )
          }),
          400,
      )

    courses = load_courses()

    # Auto-generate ID: starts at 1, increments automatically based on existing max ID
    new_id = max([c["id"] for c in courses], default=0) + 1

    # Create the new course dictionary
    new_course = {
        "id": new_id,
        "name": data.get("name").strip(),
        "description": data.get("description").strip(),
        "target_date": data.get("target_date").strip(),
        "status": status,
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # Auto-generated timestamp
    }

    courses.append(new_course)
    save_courses(courses)

    return jsonify(new_course), 201

  except RuntimeError as e:
    return jsonify({"error": str(e)}), 500


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
  """PUT /api/courses/<course_id>

  Updates an existing course by ID. Validates status if provided.
  """
  try:
    data = request.get_json()
    if not data:
      return jsonify({"error": "Request body must be valid JSON."}), 400

    courses = load_courses()
    course = next((c for c in courses if c["id"] == course_id), None)

    # Error handling: Course not found
    if not course:
      return jsonify({"error": f"Course with ID {course_id} not found."}), 404

    # Validate status if it's included in the update request
    if "status" in data:
      status = data.get("status")
      if status not in VALID_STATUSES:
        return (
            jsonify({
                "error": (
                    f"Invalid status '{status}'. Must be one of:"
                    f" {', '.join(VALID_STATUSES)}"
                )
            }),
            400,
        )
      course["status"] = status

    # Update other optional fields if present in request
    if "name" in data:
      course["name"] = data.get("name").strip()
    if "description" in data:
      course["description"] = data.get("description").strip()
    if "target_date" in data:
      course["target_date"] = data.get("target_date").strip()

    save_courses(courses)
    return jsonify(course), 200

  except RuntimeError as e:
    return jsonify({"error": str(e)}), 500


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
  """DELETE /api/courses/<course_id>

  Deletes a specific course by its unique ID.
  """
  try:
    courses = load_courses()
    updated_courses = [c for c in courses if c["id"] != course_id]

    # Error handling: Course not found (if length didn't change, ID didn't exist)
    if len(updated_courses) == len(courses):
      return jsonify({"error": f"Course with ID {course_id} not found."}), 404

    save_courses(updated_courses)
    return (
        jsonify({
            "message": f"Course with ID {course_id} deleted successfully."
        }),
        200,
    )

  except RuntimeError as e:
    return jsonify({"error": str(e)}), 500


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":
  # Run the Flask server in development/debug mode
  app.run(debug=True)