from flask import Flask, render_template, request, jsonify
from grading_logic import auto_grade_assignment
from feedback_generator import generate_feedback
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grade', methods=['POST'])
def grade_assignments():
    try:
        # Get uploaded files and rubric
        assignment_file = request.files['assignment']
        rubric_file = request.files['rubric']
        
        # Save files
        assignment_path = os.path.join(app.config['UPLOAD_FOLDER'], assignment_file.filename)
        rubric_path = os.path.join(app.config['UPLOAD_FOLDER'], rubric_file.filename)
        assignment_file.save(assignment_path)
        rubric_file.save(rubric_path)
        
        # Process grading
        grades = auto_grade_assignment(assignment_path, rubric_path)
        
        # Generate feedback
        feedback = generate_feedback(grades)
        
        return render_template('results.html', grades=grades, feedback=feedback)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)