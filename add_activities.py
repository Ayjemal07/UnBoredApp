from app import create_app, db
from app.models import Activity

# Initialize the app and database
app = create_app()
app.app_context().push()

# 35 Cherry-picked activities to add
cherry_picked_activities = [
    {
        "name": "Pickleball",
        "description": "A fast-paced paddle sport combining tennis, badminton, and ping-pong, played on a smaller court with a perforated plastic ball.",
        "why_worth": "It's great for cardiovascular health and social interaction."
    },
    {
        "name": "Puzzle Swap",
        "description": "Exchange puzzles with friends and family to enjoy new challenges and foster community connections.",
        "why_worth": "This activity stimulates the brain and encourages bonding through shared interests."
    },
    {
        "name": "Tai Chi",
        "description": "A gentle martial art focused on slow, flowing movements that improve balance, flexibility, and mental tranquility.",
        "why_worth": "Practicing Tai Chi can reduce stress and enhance overall well-being."
    },
    {
        "name": "Murder Mystery Night",
        "description": "An interactive game where participants solve a fictional crime, providing entertainment and stimulating problem-solving skills.",
        "why_worth": "It encourages teamwork and creativity."
    },
    {
        "name": "Stargazing",
        "description": "Observing stars and celestial objects, offering relaxation and a sense of wonder about the universe.",
        "why_worth": "This activity can be both educational and calming, promoting a connection to nature."
    },
    {
        "name": "Potluck Dinner",
        "description": "A communal meal where everyone brings a dish, fostering social interaction and culinary creativity.",
        "why_worth": "Sharing food brings people together and introduces diverse cuisines."
    },
    {
        "name": "Board Game Night",
        "description": "Playing a variety of board games with friends or family, encouraging strategic thinking and fun.",
        "why_worth": "It strengthens relationships and improves cognitive functions."
    },
    {
        "name": "Hiking",
        "description": "Walking in nature, providing physical exercise, fresh air, and scenic beauty.",
        "why_worth": "Hiking boosts mental health and offers a break from the daily routine."
    },
    {
        "name": "Karaoke Night",
        "description": "Singing favorite songs, boosting confidence and providing entertainment.",
        "why_worth": "It's a fun way to relieve stress and connect with others through music."
    },
    {
        "name": "Dance Class",
        "description": "Learning new dance styles, offering physical exercise and improving coordination.",
        "why_worth": "Dancing is a joyful way to stay fit and meet new people."
    },
    {
        "name": "Book Club",
        "description": "Reading and discussing books, expanding knowledge, and fostering community.",
        "why_worth": "It encourages critical thinking and introduces diverse perspectives."
    },
    {
        "name": "Trivia Night",
        "description": "Competing in trivia games, challenging knowledge, and enjoying friendly competition.",
        "why_worth": "This activity sharpens the mind and is entertaining for all ages."
    },
    {
        "name": "Yoga Session",
        "description": "Practicing yoga, which enhances flexibility, strength, and mental clarity.",
        "why_worth": "Yoga reduces stress and improves overall physical and mental health."
    },
    {
        "name": "Beach Day",
        "description": "Spending a day at the beach, enjoying activities like swimming, sunbathing, and playing beach games.",
        "why_worth": "It's a great way to relax, have fun, and soak up some Vitamin D."
    },
    {
        "name": "Pottery Class",
        "description": "Learning to create pottery pieces, enhancing creativity, and providing a sense of accomplishment.",
        "why_worth": "Working with clay can be therapeutic and helps develop fine motor skills."
    },
    {
        "name": "Wine Tasting",
        "description": "Sampling a variety of wines, learning about different flavors and origins.",
        "why_worth": "It's an enjoyable way to refine your palate and socialize with others."
    },
    {
        "name": "Zip Lining",
        "description": "Soaring through the air on a zip line, offering an exhilarating adventure and stunning views.",
        "why_worth": "It's a thrilling way to overcome fears and enjoy nature from a different perspective."
    },
    {
        "name": "Camping",
        "description": "Spending a night or more in the wilderness, engaging in activities like hiking, fishing, and campfires.",
        "why_worth": "Camping reconnects you with nature and offers a break from technology and daily stress."
    },
    {
        "name": "Archery",
        "description": "Practicing shooting arrows at a target, improving focus and hand-eye coordination.",
        "why_worth": "Archery is both a mental and physical challenge, enhancing concentration and discipline."
    },
    {
        "name": "Salsa Dancing",
        "description": "Learning the energetic and rhythmic moves of salsa dancing.",
        "why_worth": "It's a fun way to exercise, improve coordination, and meet new people."
    },
    {
        "name": "Rock Climbing",
        "description": "Climbing indoor or outdoor rock walls, building strength and overcoming challenges.",
        "why_worth": "Rock climbing improves physical fitness and boosts confidence."
    },
    {
        "name": "Stand-Up Paddleboarding",
        "description": "Balancing on a paddleboard while navigating the water, providing a full-body workout.",
        "why_worth": "Paddleboarding enhances core strength and offers a peaceful water experience."
    },
    {
        "name": "Horseback Riding",
        "description": "Riding horses, improving balance, coordination, and a connection with animals.",
        "why_worth": "Horseback riding is both relaxing and invigorating, offering a unique way to enjoy the outdoors."
    },
    {
        "name": "Art Gallery Tour",
        "description": "Visiting local art galleries to appreciate different forms of art and culture.",
        "why_worth": "It's an enriching experience that fosters creativity and cultural appreciation."
    },
    {
        "name": "Meditation",
        "description": "Spending time meditating to practice mindfulness and relaxation.",
        "why_worth": "It helps reduce stress and enhances mental clarity and emotional well-being."
    },
    {
        "name": "Cooking a Themed Dinner",
        "description": "Preparing a dinner based on a specific theme or cuisine.",
        "why_worth": "It's a creative and educational way to explore new cultures and flavors."
    },
    {
        "name": "Biking Adventure",
        "description": "Going on a biking trail, enjoying the scenery, and getting a good workout.",
        "why_worth": "Biking is a fun and eco-friendly way to explore new areas and stay active."
    },
    {
        "name": "Film Festival Night",
        "description": "Watching a series of movies from a specific genre or director, often with themed snacks.",
        "why_worth": "It’s an entertaining way to appreciate cinema and discuss different films."
    },
    {
        "name": "Paddle Boating",
        "description": "Navigating a small boat on a calm lake or river, providing relaxation and a mild workout.",
        "why_worth": "Paddle boating is a serene way to enjoy nature and spend quality time with friends or family."
    },
    {
        "name": "Mini Golf",
        "description": "Playing a round of mini golf on a themed course, combining fun and mild physical activity.",
        "why_worth": "It’s a lighthearted way to enjoy outdoor recreation with others."
    },
    {
        "name": "Historical Site Visit",
        "description": "Touring historical sites or museums to learn about local history and culture.",
        "why_worth": "It’s an educational activity that enriches knowledge and perspective."
    },
    {
        "name": "Kayaking",
        "description": "Paddling through rivers, lakes, or coastal waters, offering adventure and a full-body workout.",
        "why_worth": "Kayaking connects you with nature and improves physical fitness."
    },
    {
        "name": "Ziplining",
        "description": "Gliding along cables through treetop canopies, offering adrenaline and stunning views.",
        "why_worth": "Ziplining is exhilarating and a great way to experience nature."
    },
    {
        "name": "Botanical Garden Tour",
        "description": "Visiting a botanical garden to appreciate diverse plant species and beautiful landscapes.",
        "why_worth": "This activity is relaxing, educational, and visually pleasing."
    },
    {
        "name": "Ice Skating",
        "description": "Gliding on ice at a rink or frozen pond, offering fun and exercise.",
        "why_worth": "Ice skating improves balance and coordination while providing a festive activity."
    }
]


# Adding cherry-picked activities to the database
for activity_data in cherry_picked_activities:
    new_activity = Activity(
        name=activity_data['name'],
        description=activity_data['description'],
        why_worth=activity_data['why_worth'],
        cherry_picked=True
    )
    db.session.add(new_activity)

db.session.commit()

print("Cherry-picked activities added successfully.")

