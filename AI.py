def generate_roadmap(quiz_score, time_taken):
    score_feedback = ""
    time_feedback = ""
    GNW_AVG_TIME = 90
    if time_taken > GNW_AVG_TIME * 1.2:
        roadmap_message = f"नमस्ते{score_feedback}..."
        return roadmap_message
