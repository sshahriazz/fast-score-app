categorized_skills = {
    "Soft Skills": [],
    "Technical/Professional Skills": [],
    "Other Skills": [],
}

def skills_category(skills_list):
    soft_skills_keywords = ["Problem Solving", "Agile", "Test-Driven", "Debugging", "Code Review", "Collaboration", "Communication", "Time Management", "Leadership"]

    technical_skills_keywords = ["Programming", "Algorithm", "Data Structures", "Object-Oriented", "Version Control", "Database", "Web Development", "Backend Development", "Frontend Development", "Full Stack Development", "Mobile App Development", "Software Architecture", "DevOps", "Cloud Computing", "Machine Learning", "Artificial Intelligence", "Natural Language Processing", "Security", "UI/UX Design"]

    # Categorize skills
    for skill in skills_list:
        found = False
        for category, keywords in {
            "Soft Skills": soft_skills_keywords,
            "Technical/Professional Skills": technical_skills_keywords,
            }.items():
            for keyword in keywords:
                if keyword.lower() in skill.lower():
                    categorized_skills[category].append(skill)
                    found = True
                    break
            if found:
                break
        if not found:
            categorized_skills["Other Skills"].append(skill)

    return categorized_skills
