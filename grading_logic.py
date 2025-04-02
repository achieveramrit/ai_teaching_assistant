import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def auto_grade_assignment(assignment_path, rubric_path):
    """
    Automatically grades assignments based on a rubric
    Supports multiple formats (CSV for now)
    """
    try:
        # Load rubric and student submissions
        rubric = pd.read_csv(rubric_path)
        submissions = pd.read_csv(assignment_path)
        
        # Initialize results dictionary
        results = {
            'students': [],
            'scores': [],
            'correct_answers': []
        }
        
        # Vectorize rubric answers
        vectorizer = TfidfVectorizer()
        rubric_vectors = vectorizer.fit_transform(rubric['answer'])
        
        # Grade each submission
        for _, row in submissions.iterrows():
            student_answer = row['answer']
            student_vector = vectorizer.transform([student_answer])
            
            # Calculate similarity with rubric answers
            similarities = cosine_similarity(student_vector, rubric_vectors)
            max_sim_idx = np.argmax(similarities)
            score = rubric.iloc[max_sim_idx]['points']
            
            results['students'].append(row['name'])
            results['scores'].append(score)
            results['correct_answers'].append(rubric.iloc[max_sim_idx]['answer'])
        
        return results
    
    except Exception as e:
        raise Exception(f"Grading error: {str(e)}")