# core_app_ai.py
# Core, subject-agnostic AI mentor brain for ARchieve

from collections import defaultdict
from AI import db, QuizResult, Question, Topic


# -------------------------------------------------
# 1. Fetch joined quiz + question + topic data
# -------------------------------------------------

def fetch_quiz_data(user_id):
    results = (
        db.session.query(QuizResult, Question, Topic)
        .join(Question, QuizResult.question_id == Question.id)
        .join(Topic, Question.topic_id == Topic.id)
        .filter(QuizResult.user_id == user_id)
        .all()
    )
    return results


# -------------------------------------------------
# 2. Pattern analysis engine (THE BRAIN)
# -------------------------------------------------

def analyze_patterns(results):
    topic_errors = defaultdict(int)
    topic_attempts = defaultdict(int)
    topic_subject = {}

    slow_questions = 0
    correct = 0
    times = []

    for result, question, topic in results:
        topic_attempts[topic.name] += 1
        topic_subject[topic.name] = topic.subject
        times.append(result.time_taken_seconds)

        if result.was_correct:
            correct += 1
        else:
            topic_errors[topic.name] += 1

        if result.time_taken_seconds > 90:
            slow_questions += 1

    accuracy = round((correct / len(results)) * 100, 1)
    avg_time = round(sum(times) / len(times), 1)

    return {
        "accuracy": accuracy,
        "avg_time": avg_time,
        "topic_errors": topic_errors,
        "topic_attempts": topic_attempts,
        "topic_subject": topic_subject,
        "slow_questions": slow_questions,
        "total_questions": len(results)
    }


# -------------------------------------------------
# 3. Weakness explanation (student friendly)
# -------------------------------------------------

def explain_weaknesses(analysis):
    explanations = []

    for topic, errors in analysis["topic_errors"].items():
        if errors >= 2:
            explanations.append(
                f"You are losing marks repeatedly in **{topic}**, which means the core concept is not fully clear yet."
            )

    if analysis["avg_time"] > 90:
        explanations.append(
            "You are taking extra time on questions, which suggests hesitation or partial understanding."
        )

    if not explanations:
        explanations.append(
            "Your mistakes are not repeating much, which means your basics are mostly stable."
        )

    return explanations


# -------------------------------------------------
# 4. Subject-AI hook (for future Maths/Science AI)
# -------------------------------------------------

def subject_specific_hook(subject, analysis):
    """
    Placeholder for future subject-specific AIs.
    maths_ai.py or science_ai.py can override this later.
    """
    return []


# -------------------------------------------------
# 5. Personalized mini-roadmap generator
# -------------------------------------------------

def generate_mini_roadmap(analysis):
    roadmap = []

    for topic, errors in analysis["topic_errors"].items():
        if errors >= 2:
            roadmap.append(
                f"Revise the core concepts of **{topic}** from your notes, then attempt 5 basic questions."
            )

    if analysis["avg_time"] > 90:
        roadmap.append(
            "Do a 10-minute speed drill with only easy questions to build confidence."
        )

    subjects = set(analysis["topic_subject"].values())
    for subject in subjects:
        roadmap.extend(subject_specific_hook(subject, analysis))

    if not roadmap:
        roadmap.append(
            "Move to mixed questions of the same difficulty to strengthen consistency."
        )

    return roadmap


# -------------------------------------------------
# 6. Final ARchieve mentor feedback generator
# -------------------------------------------------

def generate_archieve_feedback(user_id):
    results = fetch_quiz_data(user_id)

    if not results:
        return {
            "performance_overview": "No quiz data found yet.",
            "key_weaknesses": [],
            "concept_explanations": ["Attempt at least one quiz to unlock your learning analysis."],
            "mini_roadmap": ["Start with a short quiz from any chapter."],
            "motivation": "Every strong result begins with a first attempt."
        }

    analysis = analyze_patterns(results)

    weak_topics = [
        topic for topic, errors in analysis["topic_errors"].items() if errors >= 2
    ]

    return {
        # 1. Short performance overview
        "performance_overview": (
            f"You scored {analysis['accuracy']}% with an average time of "
            f"{analysis['avg_time']} seconds per question."
        ),

        # 2. Key weaknesses detected
        "key_weaknesses": weak_topics if weak_topics else ["No strong repeating weakness detected"],

        # 3. Concept-level explanation of mistakes
        "concept_explanations": explain_weaknesses(analysis),

        # 4. Personalized mini-roadmap
        "mini_roadmap": generate_mini_roadmap(analysis),

        # 5. Human motivational line
        "motivation": "You’re closer than you think — fixing just one weak area can lift your score quickly."
    }
   
from core_app_ai import generate_archieve_feedback

feedback = generate_archieve_feedback(user_id=1)
print(feedback)
