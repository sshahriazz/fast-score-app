categorized_skills = {
    "Soft Skills": [],
    "Technical/Professional Skills": [],
    "Other Skills": [],
}

def skills_category(skills_list):
    soft_skills_keywords = [
        "Problem Solving",
        "Agile",
        "Test-Driven",
        "Debugging",
        "Code Review",
        "Collaboration",
        "Communication",
        "Time Management",
        "Leadership",
        "Adaptability",
        "Creativity",
        "Critical Thinking",
        "Emotional Intelligence",
        "Flexibility",
        "Initiative",
        "Interpersonal Skills",
        "Resilience",
        "Teamwork",
        "Decision Making",
        "Conflict Resolution",
        "Empathy",
        "Organization",
        "Attention to Detail",
        "Positive Attitude",
        "Resourcefulness",
        "Self-Motivation",
        "Stress Management",
        "Active Listening",
        "Cultural Sensitivity",
        "Negotiation",
        "Persuasion",
        "Networking",
        "Innovation",
        "Diplomacy",
        "Feedback",
        "Mentoring",
        "Motivation",
        "Punctuality",
        "Strategic Thinking",
        "Customer Service",
        "Goal Setting",
        "Presentation Skills",
        "Analytical Skills",
        "Project Management",
        "Research Skills",
        "Sales Skills",
        "Technical Skills",
        "Listening Skills"
    ]

    technical_skills_keywords = [
        "Programming Languages",
        "Software Development",
        "Computer Science",
        "Coding",
        "Scripting",
        "Web Technologies",
        "Frontend Technologies",
        "Backend Technologies",
        "API Development",
        "Microservices",
        "RESTful APIs",
        "GraphQL",
        "Database",
        "SQL",
        "NoSQL",
        "Big Data",
        "Data Analytics",
        "Data Visualization",
        "Data Engineering",
        "Data Mining",
        "Data Warehousing",
        "ETL (Extract, Transform, Load)",
        "Machine Learning Models",
        "Deep Learning",
        "Neural Networks",
        "Computer Vision",
        "Natural Language Processing",
        "Reinforcement Learning",
        "Predictive Analytics",
        "Statistics",
        "Probability",
        "Cloud Platforms",
        "Amazon Web Services (AWS)",
        "Microsoft Azure",
        "Google Cloud Platform (GCP)",
        "Containerization",
        "Docker",
        "Kubernetes",
        "Infrastructure as Code (IaC)",
        "Configuration Management",
        "Continuous Integration/Continuous Deployment (CI/CD)",
        "Serverless Architecture",
        "Microservices Architecture",
        "Scalability",
        "Reliability",
        "Fault Tolerance",
        "Cybersecurity",
        "Encryption",
        "Penetration Testing",
        "Vulnerability Management",
        "Security Operations",
        "User Interface (UI) Design",
        "User Experience (UX) Design",
        "Responsive Design",
        "Wireframing",
        "Prototyping",
        "Graphic Design",
        "Interaction Design",
        "Accessibility"
    ]

    # Track categorized skills to avoid duplicates
    categorized = set()

    # Initialize categorized_skills dictionary
    categorized_skills = {
        "Soft Skills": [],
        "Technical/Professional Skills": [],
        "Other Skills": [],
    }

    # Categorize skills
    for skill in skills_list:
        found = False
        for category, keywords in {
            "Soft Skills": soft_skills_keywords,
            "Technical/Professional Skills": technical_skills_keywords,
        }.items():
            for keyword in keywords:
                if keyword.lower() in skill.lower():
                    if skill.lower() not in map(str.lower, categorized):
                        categorized_skills[category].append(skill)
                        categorized.add(skill)
                    found = True
                    break
            if found:
                break
        if not found:
            if skill.lower() not in map(str.lower, categorized):
                categorized_skills["Other Skills"].append(skill)
                categorized.add(skill)

    return categorized_skills