from app import create_app, db
from app.models import Activity

# Initialize the app and database
app = create_app()
app.app_context().push()

# 35 Cherry-picked activities to add
cherry_picked_activities = [
    
	{
		"description": "A fast-paced paddle sport combining tennis, badminton, and ping-pong, played on a smaller court with a perforated plastic ball.",
		"google_link": "https://www.google.com/search?q=Pickleball+near+me",
		"id": 73,
		"meetup_link": "https://www.meetup.com/find/?keywords=Pickleball%20near%20me",
		"name": "Pickleball",
		"why_worth": "It's great for cardiovascular health and social interaction.",
		"youtube_link": "https://www.youtube.com/watch?v=kqLRRNOpe8U",
        "tags": ["social", "high-physical", "group", "outdoor"]

	},
	{
		"description": "Exchange puzzles with friends and family to enjoy new challenges and foster community connections.",
		"google_link": "https://www.google.com/search?q=Puzzle+Swap+near+me",
		"id": 74,
		"meetup_link": "https://www.meetup.com/find/?keywords=Puzzle%20Swap%20near%20me",
		"name": "Puzzle Swap",
		"why_worth": "This activity stimulates the brain and encourages bonding through shared interests.",
		"youtube_link": "https://www.youtube.com/watch?v=Lz-JOvp0Des",
        "tags": ["social", "mental challenge", "group", "indoor"]

	},
	{
		"description": "An interactive game where participants solve a fictional crime, providing entertainment and stimulating problem-solving skills.",
		"google_link": "https://www.google.com/search?q=Murder+Mystery+Night+near+me",
		"id": 76,
		"meetup_link": "https://www.meetup.com/find/?keywords=Murder%20Mystery%20Night%20near%20me",
		"name": "Murder Mystery Night",
		"why_worth": "It encourages teamwork and creativity.",
		"youtube_link": "https://www.youtube.com/watch?v=eG3botJCppk",
 		"tags": ["social", "mental challenge", "group", "indoor"]
	},
	{
		"description": "Observing stars and celestial objects, offering relaxation and a sense of wonder about the universe.",
		"google_link": "https://www.google.com/search?q=Stargazing+near+me",
		"id": 77,
		"meetup_link": "https://www.meetup.com/find/?keywords=Stargazing%20near%20me",
		"name": "Stargazing",
		"why_worth": "This activity can be both educational and calming, promoting a connection to nature.",
		"youtube_link": "https://www.youtube.com/watch?v=ibL91sASgKQ",
        "tags": ["relaxing", "educational", "solo", "outdoor"]
	},
	{
		"description": "Walking in nature, providing physical exercise, fresh air, and scenic beauty.",
		"google_link": "https://www.google.com/search?q=Hiking+near+me",
		"id": 80,
		"meetup_link": "https://www.meetup.com/find/?keywords=Hiking%20near%20me",
		"name": "Hiking",
		"why_worth": "Hiking boosts mental health and offers a break from the daily routine.",
		"youtube_link": "https://www.youtube.com/watch?v=edElLWvSVLk&t=805s",
        "tags": ["nature", "medium-physical", "solo", "outdoor"]
 
	},
	{
		"description": "Singing favorite songs, boosting confidence and providing entertainment.",
		"google_link": "https://www.google.com/search?q=Karaoke+Night+near+me",
		"id": 81,
		"meetup_link": "https://www.meetup.com/find/?keywords=Karaoke%20Night%20near%20me",
		"name": "Karaoke Night",
		"why_worth": "It's a fun way to relieve stress and connect with others through music.",
		"youtube_link": "https://www.youtube.com/watch?v=tBksosv42Ic",
         "tags": ["social", "entertainment", "group", "indoor"]
        
	},
	{
		"description": "Learning new dance styles, offering physical exercise and improving coordination.",
		"google_link": "https://www.google.com/search?q=Dance+Class+near+me",
		"id": 82,
		"meetup_link": "https://www.meetup.com/find/?keywords=Dance%20Class%20near%20me",
		"name": "Dance Class",
		"why_worth": "Dancing is a joyful way to stay fit and meet new people.",
		"youtube_link": "https://www.youtube.com/watch?v=Kd-Va1m4s1E",
        "tags": ["fitness", "medium-physical", "group", "indoor"]
	},
	{
		"description": "Competing in trivia games, challenging knowledge, and enjoying friendly competition.",
		"google_link": "https://www.google.com/search?q=Trivia+Night+near+me",
		"id": 84,
		"meetup_link": "https://www.meetup.com/find/?keywords=Trivia%20Night%20near%20me",
		"name": "Trivia Night",
		"why_worth": "This activity sharpens the mind and is entertaining for all ages.",
		"youtube_link": "https://www.youtube.com/watch?v=TtS-2K8_qm8",
        "tags": ["mental challenge", "entertainment", "group", "indoor"]

	},
	{
		"description": "Practicing yoga, which enhances flexibility, strength, and mental clarity.",
		"google_link": "https://www.google.com/search?q=Yoga+Session+near+me",
		"id": 85,
		"meetup_link": "https://www.meetup.com/find/?keywords=Yoga%20Session%20near%20me",
		"name": "Yoga Session",
		"why_worth": "Yoga reduces stress and improves overall physical and mental health.",
		"youtube_link": "https://www.youtube.com/watch?v=j7rKKpwdXNE",
        "tags": ["relaxing", "medium-physical", "solo", "indoor"]
	},
	{
		"description": "Spending a day at the beach, enjoying activities like swimming, sunbathing, and playing beach games.",
		"google_link": "https://www.google.com/search?q=Beach+Day+near+me",
		"id": 86,
		"meetup_link": "https://www.meetup.com/find/?keywords=Beach%20Day%20near%20me",
		"name": "Beach Day",
		"why_worth": "It's a great way to relax, have fun, and soak up some Vitamin D.",
		"youtube_link": "https://www.youtube.com/watch?v=Pw-pWL912nM",
        "tags": ["relaxing", "low-physical", "group", "outdoor"]
	},
	{
		"description": "Sampling a variety of wines, learning about different flavors and origins.",
		"google_link": "https://www.google.com/search?q=Wine+Tasting+near+me",
		"id": 88,
		"meetup_link": "https://www.meetup.com/find/?keywords=Wine%20Tasting%20near%20me",
		"name": "Wine Tasting",
		"why_worth": "It's an enjoyable way to refine your palate and socialize with others.",
		"youtube_link": "https://www.youtube.com/watch?v=QF6xzSyet4U&t=10s",
        "tags": ["social", "relaxing", "group", "indoor"]
	},
	{
		"description": "Spending a night or more in the wilderness, engaging in activities like hiking, fishing, and campfires.",
		"google_link": "https://www.google.com/search?q=Camping+near+me",
		"id": 90,
		"meetup_link": "https://www.meetup.com/find/?keywords=Camping%20near%20me",
		"name": "Camping",
		"why_worth": "Camping reconnects you with nature and offers a break from technology and daily stress.",
		"youtube_link": "https://www.youtube.com/watch?v=q5qwrjRajPQ",
        "tags": ["nature", "medium-physical", "group", "outdoor"]
	},
	{
		"description": "Practicing shooting arrows at a target, improving focus and hand-eye coordination.",
		"google_link": "https://www.google.com/search?q=Archery+near+me",
		"id": 91,
		"meetup_link": "https://www.meetup.com/find/?keywords=Archery%20near%20me",
		"name": "Archery",
		"why_worth": "Archery is both a mental and physical challenge, enhancing concentration and discipline.",
		"youtube_link": "https://www.youtube.com/watch?v=NYz4p7YRmv0",
        "tags": ["mental challenge", "high-physical", "solo", "outdoor"]
	},
	{
		"description": "Learning the energetic and rhythmic moves of salsa dancing.",
		"google_link": "https://www.google.com/search?q=Salsa+Dancing+near+me",
		"id": 92,
		"meetup_link": "https://www.meetup.com/find/?keywords=Salsa%20Dancing%20near%20me",
		"name": "Salsa Dancing",
		"why_worth": "It's a fun way to exercise, improve coordination, and meet new people.",
		"youtube_link": "https://www.youtube.com/watch?v=vwGp16NXgQU",
        "tags": ["fitness", "medium-physical", "group", "indoor"]
	},
	{
		"description": "Climbing indoor or outdoor rock walls, building strength and overcoming challenges.",
		"google_link": "https://www.google.com/search?q=Rock+Climbing+near+me",
		"id": 93,
		"meetup_link": "https://www.meetup.com/find/?keywords=Rock%20Climbing%20near%20me",
		"name": "Rock Climbing",
		"why_worth": "Rock climbing improves physical fitness and boosts confidence.",
		"youtube_link": "https://www.youtube.com/watch?v=s-ArwEzr-2M",
        "tags": ["sports", "high-physical", "outdoor"]
	},
	{
		"description": "Balancing on a paddleboard while navigating the water, providing a full-body workout.",
		"google_link": "https://www.google.com/search?q=Stand-Up+Paddleboarding+near+me",
		"id": 94,
		"meetup_link": "https://www.meetup.com/find/?keywords=Stand-Up%20Paddleboarding%20near%20me",
		"name": "Stand-Up Paddleboarding",
		"why_worth": "Paddleboarding enhances core strength and offers a peaceful water experience.",
		"youtube_link": "https://www.youtube.com/watch?v=ES2mShoQ3_Q",
        "tags": ["sports", "high-physical", "outdoor"]
        
	},
	{
		"description": "A gentle martial art focused on slow, flowing movements that improve balance, flexibility, and mental tranquility.",
		"google_link": "https://www.google.com/search?q=Tai+Chi+near+me",
		"id": 75,
		"meetup_link": "https://www.meetup.com/find/?keywords=Tai%20Chi%20near%20me",
		"name": "Tai Chi",
		"why_worth": "Practicing Tai Chi can reduce stress and enhance overall well-being.",
		"youtube_link": "https://www.youtube.com/watch?v=hIOHGrYCEJ4",
        "tags": ["relaxing", "medium-physical", "outdoor"]
	},
	{
		"description": "Playing a variety of board games with friends or family, encouraging strategic thinking and fun.",
		"google_link": "https://www.google.com/search?q=Board+Game+Night+near+me",
		"id": 79,
		"meetup_link": "https://www.meetup.com/find/?keywords=Board%20Game%20Night%20near%20me",
		"name": "Board Game Night",
		"why_worth": "It strengthens relationships and improves cognitive functions.",
		"youtube_link": "https://www.youtube.com/watch?v=oJ7JHQ4l5TE",
        "tags": ["mental challenge", "social", "indoor"]
	},
	{
		"description": "A communal meal where everyone brings a dish, fostering social interaction and culinary creativity.",
		"google_link": "https://www.google.com/search?q=Potluck+Dinner+near+me",
		"id": 78,
		"meetup_link": "https://www.meetup.com/find/?keywords=Potluck%20Dinner%20near%20me",
		"name": "Potluck Dinner",
		"why_worth": "Sharing food brings people together and introduces diverse cuisines.",
		"youtube_link": "https://www.youtube.com/watch?v=ObL0w7OKOzY",
        "tags": ["social", "relaxing", "indoor"]
	},
	{
		"description": "Learning to create pottery pieces, enhancing creativity, and providing a sense of accomplishment.",
		"google_link": "https://www.google.com/search?q=Pottery+Class+near+me",
		"id": 87,
		"meetup_link": "https://www.meetup.com/find/?keywords=Pottery%20Class%20near%20me",
		"name": "Pottery Class",
		"why_worth": "Working with clay can be therapeutic and helps develop fine motor skills.",
		"youtube_link": "https://www.youtube.com/watch?v=FtES7Gd5gHE",
        "tags": ["art", "relaxing", "indoor"]
        
	},
	{
		"description": "Riding horses, improving balance, coordination, and a connection with animals.",
		"google_link": "https://www.google.com/search?q=Horseback+Riding+near+me",
		"id": 95,
		"meetup_link": "https://www.meetup.com/find/?keywords=Horseback%20Riding%20near%20me",
		"name": "Horseback Riding",
		"why_worth": "Horseback riding is both relaxing and invigorating, offering a unique way to enjoy the outdoors.",
		"youtube_link": "https://www.youtube.com/watch?v=fV7kuUrjutY",
        "tags": ["nature", "medium-physical", "outdoor"]
	},
	{
		"description": "Visiting local art galleries to appreciate different forms of art and culture.",
		"google_link": "https://www.google.com/search?q=Art+Gallery+Tour+near+me",
		"id": 96,
		"meetup_link": "https://www.meetup.com/find/?keywords=Art%20Gallery%20Tour%20near%20me",
		"name": "Art Gallery Tour",
		"why_worth": "It's an enriching experience that fosters creativity and cultural appreciation.",
		"youtube_link": "https://www.youtube.com/watch?v=rFYgGG2Rgd0",
        "tags": ["art", "relaxing", "indoor"]
	},
	{
		"description": "Spending time meditating to practice mindfulness and relaxation.",
		"google_link": "https://www.google.com/search?q=Meditation+near+me",
		"id": 97,
		"meetup_link": "https://www.meetup.com/find/?keywords=Meditation%20near%20me",
		"name": "Meditation",
		"why_worth": "It helps reduce stress and enhances mental clarity and emotional well-being.",
		"youtube_link": "https://www.youtube.com/watch?v=X3rl5O_92Co",
        "tags": ["relaxing", "mental challenge", "indoor"]
	},
	{
		"description": "Preparing a dinner based on a specific theme or cuisine.",
		"google_link": "https://www.google.com/search?q=Cooking+a+Themed+Dinner+near+me",
		"id": 98,
		"meetup_link": "https://www.meetup.com/find/?keywords=Cooking%20a%20Themed%20Dinner%20near%20me",
		"name": "Cooking a Themed Dinner",
		"why_worth": "It's a creative and educational way to explore new cultures and flavors.",
		"youtube_link": "https://www.youtube.com/watch?v=SMfYLjjIcVU",
        "tags": ["educational", "art", "indoor"]
	},
	{
		"description": "Going on a biking trail, enjoying the scenery, and getting a good workout.",
		"google_link": "https://www.google.com/search?q=Biking+Adventure+near+me",
		"id": 99,
		"meetup_link": "https://www.meetup.com/find/?keywords=Biking%20Adventure%20near%20me",
		"name": "Biking Adventure",
		"why_worth": "Biking is a fun and eco-friendly way to explore new areas and stay active.",
		"youtube_link": "https://www.youtube.com/watch?v=AAfcHMdPQ20",
        "tags": ["fitness", "high-physical", "outdoor"]
	},
	{
		"description": "Watching a series of movies from a specific genre or director, often with themed snacks.",
		"google_link": "https://www.google.com/search?q=Film+Festival+Night+near+me",
		"id": 100,
		"meetup_link": "https://www.meetup.com/find/?keywords=Film%20Festival%20Night%20near%20me",
		"name": "Film Festival Night",
		"why_worth": "It’s an entertaining way to appreciate cinema and discuss different films.",
		"youtube_link": "https://www.youtube.com/watch?v=v3P_UvYOQgw",
        "tags": ["entertainment", "relaxing", "outdoor"]
	},
	{
		"description": "Navigating a small boat on a calm lake or river, providing relaxation and a mild workout.",
		"google_link": "https://www.google.com/search?q=Paddle+Boating+near+me",
		"id": 101,
		"meetup_link": "https://www.meetup.com/find/?keywords=Paddle%20Boating%20near%20me",
		"name": "Paddle Boating",
		"why_worth": "Paddle boating is a serene way to enjoy nature and spend quality time with friends or family.",
		"youtube_link": "https://www.youtube.com/watch?v=uoOw9hrVQbk",
        "tags": ["nature", "medium-physical", "outdoor"]
	},
	{
		"description": "Playing a round of mini golf on a themed course, combining fun and mild physical activity.",
		"google_link": "https://www.google.com/search?q=Mini+Golf+near+me",
		"id": 102,
		"meetup_link": "https://www.meetup.com/find/?keywords=Mini%20Golf%20near%20me",
		"name": "Mini Golf",
		"why_worth": "It’s a lighthearted way to enjoy outdoor recreation with others.",
		"youtube_link": "https://www.youtube.com/watch?v=9bfOP0uRQug",
        "tags": ["outdoor", "low-physical", "social"]
	},
	{
		"description": "Touring historical sites or museums to learn about local history and culture.",
		"google_link": "https://www.google.com/search?q=Historical+Site+Visit+near+me",
		"id": 103,
		"meetup_link": "https://www.meetup.com/find/?keywords=Historical%20Site%20Visit%20near%20me",
		"name": "Historical Site Visit",
		"why_worth": "It’s an educational activity that enriches knowledge and perspective.",
		"youtube_link": "https://www.youtube.com/watch?v=fq70UHD8DrM",
        "tags": ["outdoor", "educational", "social"]
        
	},
	{
		"description": "Paddling through rivers, lakes, or coastal waters, offering adventure and a full-body workout.",
		"google_link": "https://www.google.com/search?q=Kayaking+near+me",
		"id": 104,
		"meetup_link": "https://www.meetup.com/find/?keywords=Kayaking%20near%20me",
		"name": "Kayaking",
		"why_worth": "Kayaking connects you with nature and improves physical fitness.",
		"youtube_link": "https://www.youtube.com/watch?v=TAEkR13ChPs",
         "tags": ["outdoor", "high-physical", "nature"],
	},
	{
		"description": "Gliding along cables through treetop canopies, offering adrenaline and stunning views.",
		"google_link": "https://www.google.com/search?q=Ziplining+near+me",
		"id": 105,
		"meetup_link": "https://www.meetup.com/find/?keywords=Ziplining%20near%20me",
		"name": "Ziplining",
		"why_worth": "Ziplining is exhilarating and a great way to experience nature.",
		"youtube_link": "https://www.youtube.com/watch?v=mrBrfKi4vpI",
        "tags": ["outdoor", "high-physical", "nature"]
	},
	{
		"description": "Visiting a botanical garden to appreciate diverse plant species and beautiful landscapes.",
		"google_link": "https://www.google.com/search?q=Botanical+Garden+Tour+near+me",
		"id": 106,
		"meetup_link": "https://www.meetup.com/find/?keywords=Botanical%20Garden%20Tour%20near%20me",
		"name": "Botanical Garden Tour",
		"why_worth": "This activity is relaxing, educational, and visually pleasing.",
		"youtube_link": "https://www.youtube.com/watch?v=FSotOLHxB5M",
        "tags": ["outdoor", "relaxing", "educational"]
	},
	{
		"description": "Gliding on ice at a rink or frozen pond, offering fun and exercise.",
		"google_link": "https://www.google.com/search?q=Ice+Skating+near+me",
		"id": 107,
		"meetup_link": "https://www.meetup.com/find/?keywords=Ice%20Skating%20near%20me",
		"name": "Ice Skating",
		"why_worth": "Ice skating improves balance and coordination while providing a festive activity.",
		"youtube_link": "https://www.youtube.com/watch?v=XcDw55IWWYQ",
         "tags": ["outdoor", "medium-physical", "social"]
	},
	{
		"description": "Swimming is a water-based activity involving moving through water using arms and legs, either for recreation, sport, or exercise",
		"google_link": "https://www.google.com/search?q=Swimming+near+me",
		"id": 89,
		"meetup_link": "https://www.meetup.com/find/?keywords=swimming%20",
		"name": "Swimming",
		"why_worth": "Swimming improves cardiovascular health, strengthens muscles, and provides a full-body workout while being gentle on joints",
		"youtube_link": "https://www.youtube.com/watch?v=jKqQRC_D5aM",
        "tags": ["outdoor", "high-physical", "indoor"]
	},
	{
		"description": "Reading and discussing books, expanding knowledge, and fostering community.",
		"google_link": "https://www.google.com/search?q=Book+Club+near+me",
		"id": 83,
		"meetup_link": "https://www.meetup.com/find/?keywords=Book%20Club%20near%20me",
		"name": "Book Club",
		"why_worth": "It encourages critical thinking and introduces diverse perspectives.",
		"youtube_link": "https://www.youtube.com/watch?v=V-futZ4915s",
        "tags": ["indoor", "social", "educational"]
	},

	{
		"name": "Bowling",
		"description": "A fun indoor sport where players roll a ball to knock down pins.",
		"google_link": "https://www.google.com/search?q=Bowling+near+me",
        "id": 108,
		"meetup_link": "https://www.meetup.com/find/?keywords=Bowling",
		"why_worth": "It's a casual and social game suitable for all ages and skill levels.",
        "youtube_link": "https://www.youtube.com/watch?v=q921f42q7eE",
         "tags": ["indoor", "social", "low-physical"]
	},
    
	{
		"name": "Laser Tag",
		"description": "A high-energy game where players use infrared-emitting guns to tag opponents in a maze.",
		"google_link": "https://www.google.com/search?q=Laser+Tag+near+me",
        "id": 109,
		"meetup_link": "https://www.meetup.com/find/?keywords=Laser%20Tag",
		"why_worth": "A great way to have fun with friends while staying active and competitive.",
        "youtube_link": "https://www.youtube.com/watch?v=o4DDnbtexzU",
         "tags": ["indoor", "social", "medium-physical"]
        
	},
    
	{
        "name": "Paintball",
		"description": "A competitive team sport where players eliminate opponents by hitting them with paint-filled pellets.",
		"google_link": "https://www.google.com/search?q=Paintball+near+me",
        "id": 110,
		"meetup_link": "https://www.meetup.com/find/?keywords=Paintball",
		"why_worth": "Exciting, fast-paced action that gets your adrenaline pumping.",
        "youtube_link": "https://www.youtube.com/watch?v=Pan4htMS_lA",
        "tags": ["outdoor", "social", "high-physical"]
	},
	{
		"name": "Zumba",
		"description": "A fitness program combining Latin and international music with dance moves.",
		"google_link": "https://www.google.com/search?q=Zumba+classes+near+me",
        "id": 111,
		"meetup_link": "https://www.meetup.com/find/?keywords=Zumba",
		"why_worth": "It's a fun way to burn calories and improve fitness through dancing.",
        "youtube_link": "https://www.youtube.com/watch?v=yhW1mO3y7dc",
        "tags": ["indoor", "fitness", "social"]
	},
    
	{
        "name": "Axe Throwing",
		"description": "A fun and challenging activity where players throw axes at a wooden target.",
		"google_link": "https://www.google.com/search?q=Axe+Throwing+near+me",
        "id": 112,
		"meetup_link": "https://www.meetup.com/find/?keywords=Axe%20Throwing",
		"why_worth": "A unique way to relieve stress and develop precision skills.",
        "youtube_link": "https://www.youtube.com/watch?v=O4ZDvRa9Dk4",
         "tags": ["indoor", "social", "low-physical"]
	},
    
	{
        "name": "Disc Golf",
		"description": "A sport in which players throw a disc at a target, with rules similar to golf.",
		"google_link": "https://www.google.com/search?q=Disc+Golf+near+me",
        "id": 113,
		"meetup_link": "https://www.meetup.com/find/?keywords=Disc%20Golf",
		"why_worth": "It combines outdoor fun with friendly competition and low-impact exercise.",
        "youtube_link": "https://www.youtube.com/watch?v=T7Buk1Hn8jM",
        "tags": ["outdoor", "low-physical", "social"]
	},
    
	{
		"name": "Origami",
		"description": "Origami is a relaxing and creative way to make beautiful shapes from paper, improving focus and patience.",
		"google_link": "https://www.google.com/search?q=Origami+near+me",
        "id": 114,
		"meetup_link": "https://www.meetup.com/find/?keywords=Origami",
		"why_worth": "It combines outdoor fun with friendly competition and low-impact exercise.",
        "youtube_link": "https://www.youtube.com/watch?v=GC_Szxdqh2Y",
        "tags": ["indoor", "relaxing", "solo"]
	},
    
	{
		"name": "Martial Arts",
		"description": "Training in various combat techniques for self-defense, fitness, and discipline.",
		"google_link": "https://www.google.com/search?q=Martial+Arts+classes+near+me",
        "id": 115,
		"meetup_link": "https://www.meetup.com/find/?keywords=Martial%20Arts",
		"why_worth": "It improves physical fitness, self-defense skills, and mental discipline.",
        "youtube_link": "https://www.youtube.com/watch?v=e64AtWekQVo",
        "tags": ["indoor", "fitness", "medium-physical"]
	},
    
	{
        "name": "Upcycling",
		"description": "Transforming old or discarded items into new, functional, or artistic creations.",
		"google_link": "https://www.google.com/search?q=Upcycling+workshops+near+me",
        "id": 116,
		"meetup_link": "https://www.meetup.com/find/?keywords=Upcycling",
		"why_worth": "It promotes sustainability and creativity by repurposing materials.",
        "youtube_link": "https://www.youtube.com/watch?v=fGqfWvm4TnQ",
        "tags": ["indoor", "art", "social"]
	}
    
]


# Adding cherry-picked activities to the database
for activity_data in cherry_picked_activities:
    new_activity = Activity(
        name=activity_data['name'],
        description=activity_data['description'],
        why_worth=activity_data['why_worth'],
        youtube_link=activity_data['youtube_link'],
        google_link=activity_data['google_link'],
        meetup_link=activity_data['meetup_link'],
        cherry_picked=True
    )
    db.session.add(new_activity)


db.session.commit()

print("Cherry-picked activities added successfully.")



