import random

TOPICS = ["Sports", "Study", "Music", "Tech", "Fitness", "Communication"]
DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]
DURATIONS = [5, 10, 15]

TOPIC_CONTENT = {
    "Sports": {
        "titles": [
            "History of the Olympics", "Basketball Fundamentals", "Soccer Strategies",
            "Track and Field Basics", "Swimming Techniques", "Tennis Serve Mastery",
            "Cricket: A Beginner's Guide", "Volleyball Rules Explained",
            "The Science of Marathon Running", "Injury Prevention in Sports"
        ],
        "content_templates": [
            "Sports have been an integral part of human culture for thousands of years. {topic_detail} Understanding the fundamentals helps both players and fans appreciate the depth of athletic competition.",
            "Physical activity through sports offers numerous benefits including cardiovascular health, mental well-being, and social connections. {topic_detail} Regular practice and understanding of techniques can significantly improve performance.",
        ],
        "quiz_bank": [
            {"question": "Which country hosted the first modern Olympics?", "options": [{"text": "Greece", "is_correct": True}, {"text": "France", "is_correct": False}, {"text": "USA", "is_correct": False}, {"text": "UK", "is_correct": False}]},
            {"question": "How many players are on a basketball team on court?", "options": [{"text": "5", "is_correct": True}, {"text": "6", "is_correct": False}, {"text": "7", "is_correct": False}, {"text": "4", "is_correct": False}]},
            {"question": "What is the standard length of a marathon?", "options": [{"text": "42.195 km", "is_correct": True}, {"text": "40 km", "is_correct": False}, {"text": "45 km", "is_correct": False}, {"text": "38 km", "is_correct": False}]},
            {"question": "Which sport uses a shuttlecock?", "options": [{"text": "Badminton", "is_correct": True}, {"text": "Tennis", "is_correct": False}, {"text": "Squash", "is_correct": False}, {"text": "Table Tennis", "is_correct": False}]},
            {"question": "How many sets are played in a standard volleyball match?", "options": [{"text": "Best of 5", "is_correct": True}, {"text": "Best of 3", "is_correct": False}, {"text": "Best of 7", "is_correct": False}, {"text": "4 sets", "is_correct": False}]},
        ]
    },
    "Study": {
        "titles": [
            "Effective Note-Taking Methods", "Speed Reading Techniques", "Memory Palace Method",
            "Pomodoro Technique Deep Dive", "Active Recall Strategies", "Spaced Repetition Systems",
            "Mind Mapping for Learning", "Critical Thinking Skills",
            "How to Write Research Papers", "Exam Preparation Strategies"
        ],
        "content_templates": [
            "Effective studying requires more than just reading material. {topic_detail} Research shows that active engagement with content leads to better retention and understanding.",
            "Learning how to learn is perhaps the most valuable skill you can develop. {topic_detail} By applying evidence-based study techniques, you can dramatically improve your academic performance.",
        ],
        "quiz_bank": [
            {"question": "What is the Pomodoro Technique?", "options": [{"text": "25 min work + 5 min break cycles", "is_correct": True}, {"text": "1 hour continuous study", "is_correct": False}, {"text": "Reading before sleep", "is_correct": False}, {"text": "Group study method", "is_correct": False}]},
            {"question": "What is active recall?", "options": [{"text": "Testing yourself on material", "is_correct": True}, {"text": "Reading notes repeatedly", "is_correct": False}, {"text": "Highlighting text", "is_correct": False}, {"text": "Listening to lectures", "is_correct": False}]},
            {"question": "What is spaced repetition?", "options": [{"text": "Reviewing at increasing intervals", "is_correct": True}, {"text": "Studying all at once", "is_correct": False}, {"text": "Reading faster each time", "is_correct": False}, {"text": "Writing notes in different colors", "is_correct": False}]},
            {"question": "Who popularized the Memory Palace technique?", "options": [{"text": "Ancient Greeks", "is_correct": True}, {"text": "Albert Einstein", "is_correct": False}, {"text": "Isaac Newton", "is_correct": False}, {"text": "Leonardo da Vinci", "is_correct": False}]},
            {"question": "What does mind mapping help with?", "options": [{"text": "Visualizing connections between ideas", "is_correct": True}, {"text": "Memorizing exact text", "is_correct": False}, {"text": "Speed reading", "is_correct": False}, {"text": "Physical exercise", "is_correct": False}]},
        ]
    },
    "Music": {
        "titles": [
            "Music Theory Basics", "History of Jazz", "Learning Guitar Chords",
            "Piano Scales for Beginners", "The Art of Songwriting", "Electronic Music Production",
            "Classical Composers Overview", "Rhythm and Beat Patterns",
            "Vocal Training Fundamentals", "Music and the Brain"
        ],
        "content_templates": [
            "Music is a universal language that transcends cultural barriers. {topic_detail} Whether you're a performer or a listener, understanding music enriches the experience.",
            "The study of music involves both theoretical knowledge and practical skills. {topic_detail} Regular practice combined with understanding of musical concepts accelerates learning.",
        ],
        "quiz_bank": [
            {"question": "How many notes are in a standard musical octave?", "options": [{"text": "12", "is_correct": True}, {"text": "8", "is_correct": False}, {"text": "7", "is_correct": False}, {"text": "10", "is_correct": False}]},
            {"question": "What does 'tempo' refer to in music?", "options": [{"text": "Speed of the music", "is_correct": True}, {"text": "Volume", "is_correct": False}, {"text": "Pitch", "is_correct": False}, {"text": "Rhythm pattern", "is_correct": False}]},
            {"question": "Which instrument family does the piano belong to?", "options": [{"text": "Percussion/Keyboard", "is_correct": True}, {"text": "Strings only", "is_correct": False}, {"text": "Woodwind", "is_correct": False}, {"text": "Brass", "is_correct": False}]},
            {"question": "What is a chord?", "options": [{"text": "Three or more notes played together", "is_correct": True}, {"text": "A single note", "is_correct": False}, {"text": "A type of rhythm", "is_correct": False}, {"text": "A musical instrument", "is_correct": False}]},
            {"question": "Who composed the Moonlight Sonata?", "options": [{"text": "Beethoven", "is_correct": True}, {"text": "Mozart", "is_correct": False}, {"text": "Bach", "is_correct": False}, {"text": "Chopin", "is_correct": False}]},
        ]
    },
    "Tech": {
        "titles": [
            "Introduction to Python", "HTML & CSS Basics", "How the Internet Works",
            "Introduction to Databases", "Cybersecurity Fundamentals", "Cloud Computing 101",
            "Machine Learning Overview", "Git Version Control",
            "API Design Principles", "Mobile App Development Intro"
        ],
        "content_templates": [
            "Technology continues to reshape how we live and work. {topic_detail} Understanding core tech concepts is increasingly important in today's digital world.",
            "The tech industry evolves rapidly, but fundamental concepts remain consistent. {topic_detail} Building a strong foundation in these basics opens doors to countless specializations.",
        ],
        "quiz_bank": [
            {"question": "What does HTML stand for?", "options": [{"text": "HyperText Markup Language", "is_correct": True}, {"text": "High Tech Modern Language", "is_correct": False}, {"text": "Hyper Transfer Markup Language", "is_correct": False}, {"text": "Home Tool Markup Language", "is_correct": False}]},
            {"question": "What is an API?", "options": [{"text": "Application Programming Interface", "is_correct": True}, {"text": "Advanced Program Integration", "is_correct": False}, {"text": "Automated Process Interface", "is_correct": False}, {"text": "Application Process Integration", "is_correct": False}]},
            {"question": "What does CPU stand for?", "options": [{"text": "Central Processing Unit", "is_correct": True}, {"text": "Computer Personal Unit", "is_correct": False}, {"text": "Central Program Utility", "is_correct": False}, {"text": "Core Processing Unit", "is_correct": False}]},
            {"question": "Which language is primarily used for web styling?", "options": [{"text": "CSS", "is_correct": True}, {"text": "Python", "is_correct": False}, {"text": "Java", "is_correct": False}, {"text": "C++", "is_correct": False}]},
            {"question": "What is Git used for?", "options": [{"text": "Version control", "is_correct": True}, {"text": "Web hosting", "is_correct": False}, {"text": "Database management", "is_correct": False}, {"text": "Graphics design", "is_correct": False}]},
        ]
    },
    "Fitness": {
        "titles": [
            "Stretching Routines", "HIIT Workout Basics", "Nutrition for Fitness",
            "Yoga for Beginners", "Strength Training 101", "Cardio vs Weight Training",
            "Body Weight Exercises", "Recovery and Rest Days",
            "Building a Workout Plan", "Mental Health & Exercise"
        ],
        "content_templates": [
            "Physical fitness is essential for overall health and well-being. {topic_detail} A balanced approach to exercise includes both cardio and strength training components.",
            "Getting fit doesn't require expensive equipment or gym memberships. {topic_detail} Consistency and proper form are more important than intensity when starting out.",
        ],
        "quiz_bank": [
            {"question": "What does HIIT stand for?", "options": [{"text": "High Intensity Interval Training", "is_correct": True}, {"text": "Heavy Impact Intense Training", "is_correct": False}, {"text": "High Interval Impact Training", "is_correct": False}, {"text": "Healthy Intensity Interval Training", "is_correct": False}]},
            {"question": "How many hours of sleep are recommended for recovery?", "options": [{"text": "7-9 hours", "is_correct": True}, {"text": "4-5 hours", "is_correct": False}, {"text": "10-12 hours", "is_correct": False}, {"text": "3-4 hours", "is_correct": False}]},
            {"question": "What macronutrient helps build muscle?", "options": [{"text": "Protein", "is_correct": True}, {"text": "Fats only", "is_correct": False}, {"text": "Carbs only", "is_correct": False}, {"text": "Vitamins", "is_correct": False}]},
            {"question": "What is a compound exercise?", "options": [{"text": "Works multiple muscle groups", "is_correct": True}, {"text": "Uses only one muscle", "is_correct": False}, {"text": "Only cardio", "is_correct": False}, {"text": "Stretching only", "is_correct": False}]},
            {"question": "How long should you hold a static stretch?", "options": [{"text": "15-30 seconds", "is_correct": True}, {"text": "1-2 seconds", "is_correct": False}, {"text": "5 minutes", "is_correct": False}, {"text": "1 second", "is_correct": False}]},
        ]
    },
    "Communication": {
        "titles": [
            "Public Speaking Tips", "Active Listening Skills", "Non-Verbal Communication",
            "Writing Professional Emails", "Conflict Resolution", "Negotiation Techniques",
            "Storytelling in Business", "Cross-Cultural Communication",
            "Building Empathy", "Presentation Design Skills"
        ],
        "content_templates": [
            "Effective communication is the foundation of all human relationships. {topic_detail} Whether in personal or professional settings, strong communication skills lead to better outcomes.",
            "Communication involves both sending and receiving messages effectively. {topic_detail} Developing these skills requires practice, self-awareness, and a willingness to adapt to different situations.",
        ],
        "quiz_bank": [
            {"question": "What percentage of communication is non-verbal?", "options": [{"text": "Over 50%", "is_correct": True}, {"text": "10%", "is_correct": False}, {"text": "5%", "is_correct": False}, {"text": "90% is always verbal", "is_correct": False}]},
            {"question": "What is active listening?", "options": [{"text": "Fully concentrating on the speaker", "is_correct": True}, {"text": "Waiting for your turn to talk", "is_correct": False}, {"text": "Taking notes only", "is_correct": False}, {"text": "Interrupting with questions", "is_correct": False}]},
            {"question": "What is the best way to start a presentation?", "options": [{"text": "With a hook or story", "is_correct": True}, {"text": "Reading from slides", "is_correct": False}, {"text": "Apologizing for being nervous", "is_correct": False}, {"text": "Listing all agenda items", "is_correct": False}]},
            {"question": "What does empathy mean in communication?", "options": [{"text": "Understanding others' feelings", "is_correct": True}, {"text": "Agreeing with everyone", "is_correct": False}, {"text": "Speaking loudly", "is_correct": False}, {"text": "Avoiding conflict always", "is_correct": False}]},
            {"question": "Which email greeting is most professional?", "options": [{"text": "Dear [Name]", "is_correct": True}, {"text": "Hey!", "is_correct": False}, {"text": "Yo", "is_correct": False}, {"text": "Sup", "is_correct": False}]},
        ]
    },
}

DETAIL_SNIPPETS = {
    "Beginner": "This introductory lesson covers the essential basics you need to get started. No prior knowledge is required — we'll walk through everything step by step.",
    "Intermediate": "Building on foundational knowledge, this lesson explores more nuanced concepts and practical applications. You should have some familiarity with the basics.",
    "Advanced": "This advanced lesson dives deep into expert-level concepts and strategies. Prior experience and solid foundational understanding are recommended.",
}


def generate_lessons():
    lessons = []
    lesson_id = 0
    for topic in TOPICS:
        data = TOPIC_CONTENT[topic]
        for diff_idx, difficulty in enumerate(DIFFICULTIES):
            # ~3-4 lessons per topic per difficulty = ~60-72 total
            num_lessons = random.randint(3, 4)
            for i in range(num_lessons):
                title_idx = (diff_idx * num_lessons + i) % len(data["titles"])
                title = data["titles"][title_idx]
                if difficulty != "Beginner":
                    title = f"{difficulty} {title}"

                duration = random.choice(DURATIONS)
                content_template = random.choice(data["content_templates"])
                content = content_template.format(topic_detail=DETAIL_SNIPPETS[difficulty])

                # Extend content to be more realistic
                content += f"\n\n## Key Concepts\n\nIn this {duration}-minute session, we'll cover the most important aspects of {title.lower()}. "
                content += f"This is a {difficulty.lower()}-level lesson designed for learners who want to deepen their understanding of {topic.lower()}.\n\n"
                content += f"### Learning Objectives\n\n"
                content += f"1. Understand the fundamental principles of this topic\n"
                content += f"2. Apply key concepts through practical examples\n"
                content += f"3. Build confidence in your knowledge of {topic.lower()}\n\n"
                content += f"### Summary\n\nBy completing this lesson, you'll have a solid grasp of the concepts covered. "
                content += f"Remember to take the quiz to test your understanding and track your progress!"

                # Pick 2-3 quiz questions
                num_quiz = random.randint(2, 3)
                quiz = random.sample(data["quiz_bank"], min(num_quiz, len(data["quiz_bank"])))

                lessons.append({
                    "title": title,
                    "topic": topic,
                    "duration": duration,
                    "difficulty": difficulty,
                    "content": content,
                    "quiz": quiz,
                })
                lesson_id += 1
    return lessons
