import uuid
from typing import Optional, Tuple
from .models import UserProfile, ChatMessage

# Dictionary of career tips
career_tips = {
    "data science": "Data Science is a promising field. Focus on Python, statistics, and machine learning.",
    "web development": "Web development is in high demand. Learn HTML, CSS, JavaScript, and frameworks like React or Angular.",
    # ... (keep all other entries as is)
}

# Future scope explanations
future_scope_tips = {
    "data science": "Data science is revolutionizing industries like healthcare, finance, and e-commerce...",
    "web development": "Web development is essential for businesses establishing an online presence...",
    # ... (keep all other entries as is)
}

# Question patterns to identify user intent
question_patterns = {
    "skills": [
        "what skills do i need for {}",
        "which skills are important for {}",
        "what knowledge is required for {}",
        "what should i learn to work in {}"
    ],
    "start_learning": [
        "how can i start learning {}",
        "where should i begin if i want to learn {}",
        "what is the best way to learn {}",
        "how do i get started in {}"
    ],
    # ... (keep all other entries as is)
}


def get_or_create_profile(session_id: str) -> UserProfile:
    """Fetch or create a user profile based on session ID."""
    profile, _ = UserProfile.objects.get_or_create(
        session_id=session_id,
        defaults={
            'interests': [],
            'queries': [],
            'unknown_fields': []
        }
    )
    return profile


def extract_field(user_input: str) -> str:
    """Extract meaningful keywords from user input, ignoring common stop words."""
    stop_words = {"why", "should", "i", "choose", "what", "is", "the", "of", "for", "tell", "me", "about", "in", "career"}
    keywords = [word for word in user_input.split() if word.lower() not in stop_words]
    return " ".join(keywords) if keywords else "this field"


def match_question(user_input: str, profile: UserProfile) -> Tuple[Optional[str], Optional[str]]:
    """Identify question category and field from user input."""
    user_input_lower = user_input.lower()
    for field in career_tips.keys():
        if field in user_input_lower:
            for category, patterns in question_patterns.items():
                for pattern in patterns:
                    formatted = pattern.format(field)
                    if formatted in user_input_lower or field in user_input_lower:
                        return category, field
    return None, None


def answer_question(category: str, field: str) -> str:
    """Provide a response based on question category and field."""
    answers = {
        "skills": f"To work in {field}, you should focus on research, practical exercises, and certifications.",
        "start_learning": f"You can start learning {field} through online courses, tutorials, internships, and joining communities.",
        "good_career": f"{field.capitalize()} is a great career option because it offers growth, stability, and exciting challenges.",
        "job_opportunities": f"There are job opportunities in {field} across startups, multinational companies, and freelance platforms.",
        "salary_range": f"The average salary for {field} professionals depends on experience but ranges from $30,000 to $120,000 per year in many regions.",
        "career_switch": f"Switching to {field} from another field is possible with additional learning, certifications, and networking.",
        "time_to_learn": f"It typically takes between 6 months to 3 years to gain expertise in {field}, depending on your background and effort.",
        "certifications": f"Recommended certifications for {field} include specialized courses offered by recognized institutions and platforms.",
        "internships": f"You can find internships in {field} at reputed organizations, through career fairs, and online job portals.",
        "challenges": f"Common challenges in {field} include competition, keeping up with technology changes, and building experience."
    }
    return answers.get(category, "I'm still learning about this area. Can you tell me more?")


def get_response(user_input: str, profile: UserProfile) -> Tuple[str, str, str]:
    """Generate an appropriate response based on the user input."""
    user_input_lower = user_input.lower()
    category, field = match_question(user_input, profile)

    if category and field:
        if field not in profile.interests:
            profile.interests.append(field)
            profile.save()
        return answer_question(category, field), category, field

    # Check if field matches in career tips
    for field in career_tips.keys():
        if field in user_input_lower:
            if "why" in user_input_lower or "future" in user_input_lower or "scope" in user_input_lower:
                if field not in profile.interests:
                    profile.interests.append(field)
                    profile.save()
                return future_scope_tips.get(field, career_tips[field]), "future_scope", field
            else:
                if field not in profile.interests:
                    profile.interests.append(field)
                    profile.save()
                return career_tips[field], "general", field

    # Unknown field handling
    possible_field = extract_field(user_input)
    if possible_field not in profile.unknown_fields:
        profile.unknown_fields.append(possible_field)
        profile.save()

    response = ("{possible_field.capitalize()}")
    return response, "unknown", possible_field
def get_response(user_input: str, profile: UserProfile) -> Tuple[str, str, str]:
    """Generate an appropriate response based on the user input."""
    user_input_lower = user_input.lower()
    category, field = match_question(user_input, profile)

    if category and field:
        if field not in profile.interests:
            profile.interests.append(field)
            profile.save()
        return answer_question(category, field), category, field

    # Check if field matches in career tips
    for field in career_tips.keys():
        if field in user_input_lower:
            if "why" in user_input_lower or "future" in user_input_lower or "scope" in user_input_lower:
                if field not in profile.interests:
                    profile.interests.append(field)
                    profile.save()
                return future_scope_tips.get(field, career_tips[field]), "future_scope", field
            else:
                if field not in profile.interests:
                    profile.interests.append(field)
                    profile.save()
                return career_tips[field], "general", field

    # Unknown field handling
    possible_field = extract_field(user_input)
    if possible_field not in profile.unknown_fields:
        profile.unknown_fields.append(possible_field)
        profile.save()

    response = (f"{possible_field.capitalize()} is an interesting area. Generally, it offers various opportunities depending on your skills, "
                "certifications, and experience. Would you like suggestions on how to start or learn more?")
    return response, "unknown", possible_field



def save_chat_message(profile: UserProfile, message: str, response: str, category: Optional[str] = None, field: Optional[str] = None) -> None:
    """Save a chat message along with its metadata."""
    ChatMessage.objects.create(
        profile=profile,
        message=message,
        response=response,
        category=category,
        field=field
    )
