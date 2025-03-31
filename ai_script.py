# ai_script.py : File Name

# Try to import Brython modules; if unavailable, we assume Terminal mode.
try:
    import os
    import json
    from difflib import get_close_matches
    import re
    import torch
    import torch.optim as optim
    import torch.nn as nn
    from browser import document, html, timer
    IS_BROWSER = True
except ModuleNotFoundError:
    IS_BROWSER = False


print("                 ⚠ WORK IN PROGRESS ⚠                    ")
print("=========================================================")

# ==============================================================
# 1. Data Definitions
# ==============================================================

# (a) Word-level JSON array.
data = [
    {"word": "Hi", "number": 1},
    {"word": "Hello", "number": 2},
    {"word": "Greetings", "number": 3},
    {"word": "Hey", "number": 4},
    {"word": "Awesome", "number": 5},
    {"word": "Good", "number": 5},
    {"word": "holla", "number": 1},
    {"word": "Funny", "number": 5},
    {"word": "Curious", "number": 7},
    {"word": "Brilliant", "number": 8},
    {"word": "Mysterious", "number": 6},
    {"word": "Innovative", "number": 8},
    {"word": "Lazy", "number": 4},
    {"word": "Generous", "number": 9},
    {"word": "Hot", "number": 3},
    {"word": "Run", "number": 2},
    {"word": "Jump", "number": 2},
    {"word": "Think", "number": 3},
    {"word": "Feel", "number": 3},
    {"word": "See", "number": 2},
    {"word": "Hear", "number": 2},
    {"word": "Taste", "number": 2},
    {"word": "Smell", "number": 2},
    {"word": "Touch", "number": 2},
    {"word": "Play", "number": 3},
    {"word": "Work", "number": 4},
    {"word": "Study", "number": 4},
    {"word": "Travel", "number": 5},
    {"word": "Create", "number": 6},
    {"word": "Imagine", "number": 7},
    {"word": "Explore", "number": 7},
    {"word": "Build", "number": 6},
    {"word": "Learn", "number": 5},
    {"word": "Teach", "number": 6},
    {"word": "Share", "number": 5},
    {"word": "Help", "number": 5},
    {"word": "Enjoy", "number": 4},
    {"word": "Celebrate", "number": 6},
    {"word": "Appreciate", "number": 7},
    {"word": "Respect", "number": 8},
    {"word": "Trust", "number": 8},
    {"word": "Hope", "number": 5},
    {"word": "Dream", "number": 6},
    {"word": "Believe", "number": 7},
    {"word": "Thought", "number": 6},
    {"word": "Idea", "number": 5},
    {"word": "Plan", "number": 5},
    {"word": "Project", "number": 6},
    {"word": "Task", "number": 4},
    {"word": "Responsibility", "number": 8},
    {"word": "Success", "number": 7},
    {"word": "Failure", "number": 6},
    {"word": "Challenge", "number": 6},
    {"word": "Opportunity", "number": 7},
    {"word": "Future", "number": 5},
    {"word": "Present", "number": 4},
    {"word": "Past", "number": 4},
    {"word": "Journey", "number": 6},
    {"word": "Adventure", "number": 7},
    {"word": "Freedom", "number": 8},
    {"word": "Peace", "number": 7},
    {"word": "Happy", "number": 5},
    {"word": "Sad", "number": 6},
    {"word": "Angry", "number": 6},
    {"word": "Excited", "number": 7},
    {"word": "Frustrated", "number": 6},
    {"word": "Bored", "number": 4},
    {"word": "Confused", "number": 6},
    {"word": "Anxious", "number": 6},
    {"word": "Relaxed", "number": 5},
    {"word": "Tired", "number": 4},
    {"word": "Energetic", "number": 7},
    {"word": "Curious", "number": 7},
    {"word": "Inspired", "number": 8},
    {"word": "Motivated", "number": 8},
    {"word": "Determined", "number": 8},
    {"word": "Hopeful", "number": 7},
    {"word": "Disappointed", "number": 6},
    {"word": "Proud", "number": 7},
    {"word": "Jealous", "number": 6},
    {"word": "Grateful", "number": 8},
    {"word": "Lonely", "number": 5},
    {"word": "Exciting", "number": 7},
    {"word": "Interesting", "number": 7},
    {"word": "Dull", "number": 4},
    {"word": "Confident", "number": 8},
    {"word": "Shy", "number": 5},
    {"word": "Brave", "number": 7},
    {"word": "Courageous", "number": 8},
    {"word": "Friendly", "number": 7},
    {"word": "Helpful", "number": 6},
    {"word": "Honest", "number": 8},
    {"word": "Loyal", "number": 8},
    {"word": "Polite", "number": 7},
    {"word": "Rude", "number": 4},
    {"word": "Generous", "number": 9},
    {"word": "Selfish", "number": 5},
    {"word": "Creative", "number": 8},
    {"word": "Innovative", "number": 8},
    {"word": "Resourceful", "number": 8},
    {"word": "Persistent", "number": 7},
    {"word": "Flexible", "number": 7},
    {"word": "Adaptable", "number": 7},
    {"word": "Reliable", "number": 8},
    {"word": "Responsible", "number": 8},
    {"word": "Ambitious", "number": 8},
    {"word": "Passionate", "number": 8},
    {"word": " ", "number": 9999}
]

# (b) Sentence-level JSON array.
sentence_data = [
    {"sentence": "I love programming and building websites.", "number": 5},
    {"sentence": "I am feeling down about my project.", "number": 6},
    {"sentence": "This is a great day to learn something new!", "number": 1},
    {"sentence": "I'm excited about the new project I'm working on.", "number": 8},
    {"sentence": "I find it hilarious when things go wrong in a funny way.", "number": 5},
    {"sentence": "I'm curious about how AI can help with my tasks.", "number": 7}
]

# (c) Paragraph-level JSON array.
paragraph_data = [
    {
        "paragraph": "I'm working on a big project that involves building a comprehensive website with advanced AI features and responsive design. I have many ideas on how to merge different technologies into one cohesive system.",
        "number": 7
    },
    {
        "paragraph": "My projects include creating complex systems that generate diverse responses and even adapt to the complexity of user input, enabling storytelling and rich, in-depth conversations.",
        "number": 8
    }
]

# (d) Conversation-level JSON array (exact input–output pairs).
conversation_data = [
    {
        "input": "how are you",
        "response": "I'm doing great, {username}! Thanks for asking."
    },
    {
        "input": "what's up",
        "response": "Not much, {username}. Just here to chat!"
    }
]

# (e) Emotion data mapping keywords to responses.
emotion_data = {
    "happy": "I'm glad to see you happy, {username}!",
    "sad": "I'm sorry you're feeling sad, {username}.",
    "angry": "It seems you're upset, {username}. I understand your frustration.",
    "excited": "Your excitement is contagious, {username}!",
    "frustrated": "Take a deep breath, {username}. I know things can be tough.",
    "bored": "Let's find something fun to do, {username}!",
    "confused": "It's okay to feel confused sometimes, {username}. I'm here to help.",
    "anxious": "I can sense your anxiety, {username}. Let's try to relax.",
    "relaxed": "It's great to see you relaxed, {username}!",
    "tired": "You seem tired, {username}. Make sure to take a break.",
    "energetic": "Your energy is inspiring, {username}!",
    "curious": "Your curiosity is admirable, {username}!",
    "inspired": "I'm glad you're feeling inspired, {username}!",
    "motivated": "Your motivation is impressive, {username}!",
    "determined": "Your determination will lead you to success, {username}!",
    "hopeful": "It's wonderful to see you hopeful, {username}!",
    "disappointed": "I'm sorry to hear you're disappointed, {username}.",
    "proud": "You should be proud of yourself, {username}!",
    "jealous": "It's okay to feel jealous sometimes, {username}.",
    "grateful": "Your gratitude is appreciated, {username}!",
    "lonely": "I'm here for you, {username}. You're not alone.",
    "exciting": "Your enthusiasm is exciting, {username}!",
    "interesting": "I'm glad you find this interesting, {username}!",
    "dull": "Let's try to make things more exciting, {username}!",
    "confident": "Your confidence is admirable, {username}!",
    "shy": "It's okay to be shy, {username}. Take your time.",
    "brave": "Your bravery is inspiring, {username}!",
    "courageous": "Your courage is commendable, {username}!",
    "friendly": "It's great to see you being friendly, {username}!",
    "helpful": "Your helpfulness is appreciated, {username}!",
    "honest": "Your honesty is valued, {username}!",
    "loyal": "Your loyalty is admirable, {username}!",
    "polite": "Your politeness is commendable, {username}!",
    "rude": "Let's try to be more polite, {username}.",
    "generous": "Your generosity is inspiring, {username}!",
    "selfish": "Let's think about others too, {username}.",
    "creative": "Your creativity is impressive, {username}!",
    "innovative": "Your innovative ideas are inspiring, {username}!",
    "resourceful": "Your resourcefulness is admirable, {username}!",
    "persistent": "Your persistence will pay off, {username}!",
    "flexible": "Your flexibility is a great asset, {username}!",
    "adaptable": "Your adaptability is impressive, {username}!",
    "reliable": "You can always be counted on, {username}!",
    "responsible": "Your sense of responsibility is admirable, {username}!",
    "ambitious": "Your ambition will take you far, {username}!",
    "passionate": "Your passion is inspiring, {username}!",
    "neutral": "I'm here to chat, {username}. What would you like to talk about?"
}

# (f) Preset responses for general matching.
responses = {
    1: "Hello there, {username}!",
    2: "Hi {username}! How can I help you?",
    3: "Greetings, {username}! Nice to see you.",
    4: "Hey {username}! What's up?",
    5: "That's awesome, {username}! Your passion shines through.",
    6: "That's a detailed input, {username}. Thanks for providing that!",
    7: "Your ideas are shaping a amazing path, {username}! Keep it coming.",
    8: "I think your doing great! Keep it up {username}!"
}

# (g) Formatting templates (using a tilde for the header, for example).
format_templates = {
    "header": "~ AI Response ~"
}

# (h) Vocabulary data with definitions, usage, and synonyms.
# These are paramaters for info.
vocabulary_data = [
    {
        "word": "Hello",
        "definition": "A greeting or expression of goodwill.",
        "usage": "Used to greet someone warmly.",
        "synonyms": ["hi", "greetings", "hey"]
    },
    {
        "word": "Good",
        "definition": "Of high quality or satisfactory.",
        "usage": "Used to express approval.",
        "synonyms": ["great", "decent", "fine"]
    },
    {
        "word": "Awesome",
        "definition": "Inspiring great admiration or wonder.",
        "usage": "Used to describe something impressive.",
        "synonyms": ["amazing", "wonderful", "stunning"]
    },
    {
        "word": "Funny",
        "definition": "Causing laughter or amusement; humorous.",
        "usage": "Used to describe something that is amusing or makes you laugh.",
        "synonyms": ["hilarious", "comical", "amusing"]
    },
    {
        "word": "Curious",
        "definition": "Eager to know or learn something new.",
        "usage": "Used to describe someone who has a strong desire to learn or explore.",
        "synonyms": ["inquisitive", "inquiring", "questioning"]
    },
    {
        "word": "Brilliant",
        "definition": "Exceptionally clever or talented.",
        "usage": "Used to compliment someone's remarkable ability or ideas.",
        "synonyms": ["intelligent", "bright", "exceptional"]
    },
    {
        "word": "Mysterious",
        "definition": "Difficult or impossible to understand, explain, or identify.",
        "usage": "Used to describe something that is enigmatic or puzzling.",
        "synonyms": ["enigmatic", "cryptic", "secretive"]
    },
    {
        "word": "Innovative",
        "definition": "Featuring new methods; advanced and original.",
        "usage": "Used to describe ideas, methods, or products that are creative and novel.",
        "synonyms": ["creative", "inventive", "cutting-edge"]
    },
    {
        "word": "Lazy",
        "definition": "Unwilling to work or use energy.",
        "usage": "Used to describe someone who avoids exerting effort.",
        "synonyms": ["indolent", "idle", "sluggish"]
    },
    {
        "word": "Generous",
        "definition": "Showing kindness and willingness to give more than is necessary or expected.",
        "usage": "Used to describe someone who is unselfish and gives freely.",
        "synonyms": ["benevolent", "charitable", "philanthropic"]
    },
    {
        "word": "Hot",
        "definition": "Having a high temperature.",
        "usage": "Used to describe something that has a high temperature.",
        "synonyms": ["warm", "scorching", "sizzling"],
        "antonyms": ["cold", "cool", "chilly"]
    },
    {
        "word": "Run",
        "definition": "To move swiftly on foot.",
        "usage": [
            "She likes to run every morning.",
            "The company is expected to run smoothly.",
            "He was asked to run the meeting."
        ],
        "synonyms": ["jog", "sprint", "dash"]
    },
    {
        "word": "Jump",
        "definition": "To push oneself off a surface and into the air by using the muscles in one's legs and feet.",
        "usage": [
            "The cat can jump very high.",
            "He decided to jump into the pool.",
            "She felt like jumping for joy."
        ],
        "synonyms": ["leap", "hop", "spring"]
    },
    {
        "word": "Think",
        "definition": "To have a particular opinion, belief, or idea about someone or something.",
        "usage": [
            "I think this is a good idea.",
            "She thinks about her future often.",
            "He was thinking of calling you."
        ],
        "synonyms": ["believe", "consider", "ponder"]
    },
    {
        "word": "Feel",
        "definition": "To experience an emotion or sensation.",
        "usage": [
            "I feel happy today.",
            "She felt a sudden chill.",
            "He doesn't feel well."
        ],
        "synonyms": ["sense", "perceive", "experience"]
    },
    {
        "word": "See",
        "definition": "To perceive with the eyes; to understand or comprehend.",
        "usage": [
            "I see a bird in the tree.",
            "Do you see what I mean?",
            "She saw the movie last night."
        ],
        "synonyms": ["observe", "notice", "witness"]
    },
    {
        "word": "Hear",
        "definition": "To perceive sound with the ears; to listen to.",
        "usage": [
            "I can hear the music from here.",
            "Did you hear what she said?",
            "He hears the birds singing."
        ],
        "synonyms": ["listen", "perceive", "catch"]
    },
    {
        "word": "Taste",
        "definition": "To perceive or recognize the flavor of something.",
        "usage": [
            "I want to taste the cake.",
            "She tasted the soup and added salt.",
            "He has a refined taste in music."
        ],
        "synonyms": ["savor", "sample", "relish"]
    },
    {
        "word": "Smell",
        "definition": "To perceive or detect the odor or scent of something.",
        "usage": [
            "I can smell the flowers from here.",
            "She smelled the perfume and smiled.",
            "He has a keen sense of smell."
        ],
        "synonyms": ["scent", "odor", "fragrance"]
    },
    {
        "word": "Touch",
        "definition": "To make physical contact with something; to feel with the hands.",
        "usage": [
            "I want to touch the soft fabric.",
            "She touched his arm to get his attention.",
            "He felt a gentle touch on his shoulder."
        ],
        "synonyms": ["feel", "contact", "tap"]
    },
    {
        "word": "Play",
        "definition": "To engage in an activity for enjoyment and recreation rather than a serious or practical purpose.",
        "usage": [
            "The children love to play in the park.",
            "She plays the piano beautifully.",
            "He plays soccer every weekend."
        ],
        "synonyms": ["game", "sport", "amusement"]
    },
    {
        "word": "Work",
        "definition": "To engage in physical or mental activity to achieve a result; to perform a job or task.",
        "usage": [
            "I have to work late today.",
            "She works as a teacher.",
            "He is working on a new project."
        ],
        "synonyms": ["labor", "job", "task"]
    },
    {
        "word": "Study",
        "definition": "To apply oneself to acquiring knowledge, typically by reading or attending school.",
        "usage": [
            "I need to study for my exams.",
            "She studies biology at university.",
            "He is studying to become a doctor."
        ],
        "synonyms": ["learn", "research", "examine"]
    },
    {
        "word": "Travel",
        "definition": "To make a journey, typically of some length.",
        "usage": [
            "I love to travel to new places.",
            "She travels abroad every summer.",
            "He is traveling for work."
        ],
        "synonyms": ["journey", "voyage", "tour"]
    },
    {
        "word": "Create",
        "definition": "To bring something into existence; to produce through imaginative skill.",
        "usage": [
            "I want to create a masterpiece.",
            "She creates beautiful art.",
            "He is creating a new software application."
        ],
        "synonyms": ["make", "build", "invent"]
    },
    {
        "word": "Imagine",
        "definition": "To form a mental image or concept of something.",
        "usage": [
            "I can imagine a better future.",
            "She imagines herself traveling the world.",
            "He is good at imagining new possibilities."
        ],
        "synonyms": ["envision", "visualize", "dream"]
    },
    {
        "word": "Explore",
        "definition": "To travel through an unfamiliar area to learn about it; to examine or evaluate.",
        "usage": [
            "I want to explore the mountains.",
            "She explores different cultures through her travels.",
            "He is exploring new ideas in his research."
        ],
        "synonyms": ["discover", "investigate", "survey"]
    },
    {
        "word": "Build",
        "definition": "To construct something by putting parts or material together; to develop or form.",
        "usage": [
            "I want to build a house.",
            "She builds relationships with her clients.",
            "He is building a career in technology."
        ],
        "synonyms": ["construct", "assemble", "create"]
    },
    {
        "word": "Learn",
        "definition": "To acquire knowledge or skill through study, experience, or being taught.",
        "usage": [
            "I want to learn a new language.",
            "She learns quickly from her mistakes.",
            "He is learning to play the guitar."
        ],
        "synonyms": ["study", "master", "grasp"]
    },
    {
        "word": "Teach",
        "definition": "To impart knowledge or skill to someone; to instruct.",
        "usage": [
            "I want to teach others about my culture.",
            "She teaches mathematics at the high school.",
            "He is teaching himself how to code."
        ],
        "synonyms": ["instruct", "educate", "train"]
    },
    {
        "word": "Share",
        "definition": "To have a portion of (something) with another or others.",
        "usage": [
            "I want to share my thoughts with you.",
            "She shares her experiences on her blog.",
            "He is sharing his lunch with his friend."
        ],
        "synonyms": ["distribute", "communicate", "convey"]
    },
    {
        "word": "Help",
        "definition": "To make it easier or possible for (someone) to do something by offering one's services or resources.",
        "usage": [
            "I want to help you with your project.",
            "She helps her friends whenever they need it.",
            "He is always willing to help others."
        ],
        "synonyms": ["assist", "aid", "support"]
    },
    {
        "word": "Enjoy",
        "definition": "To take delight or pleasure in (an activity or occasion).",
        "usage": [
            "I enjoy reading books.",
            "She enjoys playing sports.",
            "He is enjoying his time at the party."
        ],
        "synonyms": ["like", "relish", "savor"]
    },
    {
        "word": "Celebrate",
        "definition": "To acknowledge (a significant or happy day or event) with a social gathering or enjoyable activity.",
        "usage": [
            "I want to celebrate my birthday with friends.",
            "She celebrates her achievements with a party.",
            "He is celebrating the success of his project."
        ],
        "synonyms": ["commemorate", "honor", "mark"]
    },
    {
        "word": "Appreciate",
        "definition": "To recognize the full worth of; to value highly.",
        "usage": [
            "I appreciate your help.",
            "She appreciates the beauty of nature.",
            "He appreciates the effort you put in."
        ],
        "synonyms": ["value", "cherish", "treasure"]
    },
    {
        "word": "Respect",
        "definition": "To admire someone or something deeply, as a result of their abilities, qualities, or achievements.",
        "usage": [
            "I respect your opinion.",
            "She respects her elders.",
            "He is respected for his hard work."
        ],
        "synonyms": ["esteem", "admire", "revere"]
    },
    {
        "word": "Trust",
        "definition": "Firm belief in the reliability, truth, or ability of someone or something.",
        "usage": [
            "I trust you to keep your word.",
            "She trusts her instincts.",
            "He is trusted by his colleagues."
        ],
        "synonyms": ["confidence", "faith", "belief"]
    },
    {
        "word": "Hope",
        "definition": "A feeling of expectation and desire for a certain thing to happen.",
        "usage": [
            "I hope you have a great day.",
            "She hopes to travel the world someday.",
            "He is hopeful about the future."
        ],
        "synonyms": ["wish", "aspire", "anticipate"]
    },
    {
        "word": "Dream",
        "definition": "A series of thoughts, images, and sensations occurring in a person's mind during sleep.",
        "usage": [
            "I had a dream about flying last night.",
            "She dreams of becoming an artist.",
            "He is living his dream.",
            "She dreams of a better world.",
            "He dreams of making a difference.",
            "They dream of a brighter future."
        ],
        "synonyms": ["vision", "fantasy", "imagination"]
    },
    {
        "word": "Believe",
        "definition": "To accept something as true, genuine, or real.",
        "usage": [
            "I believe in your abilities.",
            "She believes in the power of kindness.",
            "He believes that anything is possible."
        ],
        "synonyms": ["trust", "accept", "have faith"]
    },
    {
        "word": "Thought",
        "definition": "An idea or opinion produced by thinking or occurring suddenly in the mind.",
        "usage": [
            "I had a thought about our project.",
            "She shared her thoughts on the matter.",
            "He is deep in thought."
        ],
        "synonyms": ["idea", "notion", "concept", "thinking", "reflection"]
    },
    {
        "word": "Idea",
        "definition": "A thought or suggestion as to a possible course of action.",
        "usage": [
            "I have an idea for our project.",
            "She came up with a brilliant idea.",
            "He is full of innovative ideas."
        ],
        "synonyms": ["concept", "notion", "plan"]
    },
    {
        "word": "Plan",
        "definition": "A detailed proposal for doing or achieving something.",
        "usage": [
            "I have a plan for our project.",
            "She is making plans for her future.",
            "He has a backup plan just in case."
        ],
        "synonyms": ["strategy", "scheme", "blueprint"]
    },
    {
        "word": "Project",
        "definition": "An individual or collaborative enterprise that is carefully planned and designed to achieve a particular aim.",
        "usage": [
            "I am working on a new project.",
            "She is leading a research project.",
            "He has a project due next week."
        ],
        "synonyms": ["undertaking", "assignment", "task"]
    },
    {
        "word": "Task",
        "definition": "A piece of work to be done or undertaken.",
        "usage": [
            "I have a task to complete by the end of the day.",
            "She is assigned a difficult task.",
            "He is working on multiple tasks at once."
        ],
        "synonyms": ["job", "duty", "responsibility"]
    },
    {
        "word": "Responsibility",
        "definition": "The state or fact of having a duty to deal with something or of having control over someone.",
        "usage": [
            "I have a responsibility to my family.",
            "She takes her responsibilities seriously.",
            "He is responsible for managing the team."
        ],
        "synonyms": ["duty", "obligation", "accountability"]
    },
    {
        "word": "Success",
        "definition": "The accomplishment of an aim or purpose.",
        "usage": [
            "I hope for success in my endeavors.",
            "She achieved great success in her career.",
            "He is on the path to success."
        ],
        "synonyms": ["achievement", "triumph", "victory"]
    },
    {
        "word": "Failure",
        "definition": "Lack of success in achieving a goal or aim.",
        "usage": [
            "I learned from my failure.",
            "She faced failure but persevered.",
            "He is afraid of failure."
        ],
        "synonyms": ["defeat", "setback", "collapse"]
    },
    {
        "word": "Challenge",
        "definition": "A task or situation that tests a person's abilities.",
        "usage": [
            "I love a good challenge.",
            "She thrives on challenges.",
            "He is ready to take on new challenges."
        ],
        "synonyms": ["obstacle", "difficulty", "test"]
    },
    {
        "word": "Opportunity",
        "definition": "A set of circumstances that makes it possible to do something.",
        "usage": [
            "I see this as a great opportunity.",
            "She seized the opportunity to travel abroad.",
            "He is looking for new opportunities."
        ],
        "synonyms": ["chance", "prospect", "occasion"]
    },
    {
        "word": "Future",
        "definition": "The time or a period of time following the moment of speaking or writing; the time to come.",
        "usage": [
            "I am excited about the future.",
            "She is planning for her future.",
            "He believes in a bright future."
        ],
        "synonyms": ["tomorrow", "prospect", "outlook"]
    },
    {
        "word": "Present",
        "definition": "The period of time now occurring.",
        "usage": [
            "I want to enjoy the present moment.",
            "She is focused on the present.",
            "He lives in the present."
        ],
        "synonyms": ["now", "current", "contemporary"]
    },
    {
        "word": "Past",
        "definition": "The time before the present; a period of time that has already happened.",
        "usage": [
            "I often think about the past.",
            "She learned from her past experiences.",
            "He is haunted by his past."
        ],
        "synonyms": ["history", "yesteryear", "bygone"]
    },
    {
        "word": "Journey",
        "definition": "An act of traveling from one place to another.",
        "usage": [
            "I love the journey more than the destination.",
            "She is on a journey of self-discovery.",
            "He documented his journey through photography."
        ],
        "synonyms": ["trip", "voyage", "expedition"]
    },
    {
        "word": "Adventure",
        "definition": "An unusual and exciting, typically hazardous, experience or activity.",
        "usage": [
            "I crave adventure in my life.",
            "She went on an adventure to explore the unknown.",
            "He is always seeking new adventures."
        ],
        "synonyms": ["quest", "exploration", "excursion"]
    },
    {
        "word": "Freedom",
        "definition": "The power or right to act, speak, or think as one wants without hindrance or restraint.",
        "usage": [
            "I cherish my freedom.",
            "She fought for her freedom.",
            "He values his freedom above all."
        ],
        "synonyms": ["liberty", "independence", "autonomy"]
    },
    {
        "word": "Peace",
        "definition": "Freedom from disturbance; tranquility.",
        "usage": [
            "I seek peace in my life.",
            "She found peace in nature.",
            "He is an advocate for world peace."
        ],
        "synonyms": ["calm", "serenity", "harmony"]
    },
    {
        "word": "Happy",
        "definition": "Feeling or showing pleasure or contentment.",
        "usage": [
            "I am happy to see you.",
            "She is happy with her achievements.",
            "He makes me happy."
        ],
        "synonyms": ["joyful", "content", "cheerful"]
    },
    {
        "word": "Sad",
        "definition": "Feeling or showing sorrow; unhappy.",
        "usage": [
            "I feel sad about the news.",
            "She was sad to leave her friends.",
            "He is sad but hopeful."
        ],
        "synonyms": ["unhappy", "sorrowful", "dejected"]
    },
    {
        "word": "Angry",
        "definition": "Having a strong feeling of or showing annoyance, displeasure, or hostility.",
        "usage": [
            "I am angry about the situation.",
            "She was angry at the unfair treatment.",
            "He expressed his anger constructively."
        ],
        "synonyms": ["mad", "irate", "furious"]
    },
    {
        "word": "Excited",
        "definition": "Very enthusiastic and eager.",
        "usage": [
            "I am excited about the event.",
            "She felt excited to meet new people.",
            "He is excited for the future."
        ],
        "synonyms": ["enthusiastic", "eager", "thrilled"]
    },
    {
        "word": "Frustrated",
        "definition": "(of a person) feeling or expressing distress and annoyance, especially because of inability to change or achieve something.",
        "usage": [
            "I feel frustrated with the delays.",
            "She was frustrated by the lack of progress.",
            "He was frustrated by the lack of progress",
            "He expressed his frustration openly."
        ],
        "synonyms": ["annoyed", "exasperated", "irritated"]
    },
    {
        "word": "Accomplished",
        "definition": "To be (accomplished) means to be highly skilled, proficient, and successful in a particular area or field, or to have successfully completed or achieved something significant.",
        "usage": [
            "I was accomplished by how well I did on X and Y",
            "He was accomplished towards how amazing he worked on his project."
        ],
        "synonyms": ["expert", "skilled"]
    }
]

# ==============================================================
# 2. Helper Functions
# ==============================================================


def replace_tokens(text, tokens):
    """
    Replace token placeholders (e.g. {username} or ${username}) in text
    with the corresponding values from tokens.
    """
    for key, value in tokens.items():
        text = text.replace("{" + key + "}", str(value))
        text = text.replace("${" + key + "}", str(value))
    return text


def get_number_from_word(word):
    """
    Return the numerical ID associated with a word (case-insensitive)
    from the word-level data.
    """
    for item in data:
        if item["word"].lower() == word.lower():
            return item["number"]
    return None


def find_best_match(user_input):
    """
    Find a close match for user_input in the word-level data using difflib.
    Returns a tuple (matched_word, number) if found.
    """
    words = [item["word"] for item in data]
    matches = get_close_matches(user_input, words, n=1, cutoff=0.0)
    if matches:
        matched_word = matches[0]
        return matched_word, get_number_from_word(matched_word)
    return None, None


def find_best_sentence_match(user_sentence):
    """
    Find a close match for a sentence in the sentence-level data.
    Returns (matched_sentence, number) if found.
    """
    sentences = [item["sentence"] for item in sentence_data]
    matches = get_close_matches(user_sentence, sentences, n=1, cutoff=0.3)
    if matches:
        matched_sentence = matches[0]
        for item in sentence_data:
            if item["sentence"].lower() == matched_sentence.lower():
                return matched_sentence, item["number"]
    return None, None


def find_best_paragraph_match(user_paragraph):
    """
    Find a close match for a paragraph from the paragraph-level data.
    Returns (matched_paragraph, number) if found.
    """
    paragraphs = [item["paragraph"] for item in paragraph_data]
    matches = get_close_matches(user_paragraph, paragraphs, n=1, cutoff=0.3)
    if matches:
        matched_paragraph = matches[0]
        for item in paragraph_data:
            if item["paragraph"].lower() == matched_paragraph.lower():
                return matched_paragraph, item["number"]
    return None, None


def find_best_conversation_match(user_text):
    """
    Look for a conversation-level match in conversation_data.
    Returns the conversation response (with tokens still intact) if found.
    """
    inputs = [item["input"] for item in conversation_data]
    low_text = user_text.lower()
    matches = get_close_matches(low_text, inputs, n=1, cutoff=0.3)
    if matches:
        matched = matches[0]
        for item in conversation_data:
            if item["input"].lower() == matched:
                return item["response"]
    return None


def extract_emotion_response(user_text, tokens):
    """
    Check if any emotion keyword from emotion_data is found within user_text.
    If so, return the corresponding response (with tokens replaced).
    """
    low_text = user_text.lower()
    for emotion, resp in emotion_data.items():
        if emotion in low_text:
            return replace_tokens(resp, tokens)
    return ""

# Add a new function for naive syllable splitting.


def split_into_syllables(word):
    vowels = "aeiouyAEIOUY"
    syllables = []
    current = ""
    for i, ch in enumerate(word):
        current += ch
        # Mark syllable boundary when a vowel is found and next character is not a vowel.
        if ch in vowels and (i + 1 == len(word) or word[i+1] not in vowels):
            syllables.append(current)
            current = ""
    if current:
        syllables.append(current)
    return syllables

# Modify tokenize_text to use syllables instead of letters.


def tokenize_text(text):
    tokens = []
    words = text.split()  # splitting by whitespace
    for word in words:
        sylls = split_into_syllables(word)
        tokens.extend(sylls)
        tokens.append(" ")  # append a delimiter token for word boundary
    if tokens and tokens[-1] == " ":
        tokens.pop()
    return tokens

# Replace detokenize_numbers with detokenize_tokens to convert token list back to text.


def detokenize_tokens(tokens):
    words = []
    current_word = ""
    for token in tokens:
        if token == " ":
            if current_word:
                words.append(current_word)
                current_word = ""
        else:
            current_word += token
    if current_word:
        words.append(current_word)
    return " ".join(words)


def build_token_model(text):
    """
    Build a token-based model from text. Each token maps to a list of tokens that follow it.
    """
    tokens = tokenize_text(text)
    model = {}
    for i in range(len(tokens) - 1):
        token = tokens[i]
        next_token = tokens[i + 1]
        model.setdefault(token, []).append(next_token)
    return model


def predict_next_token(last_token, token_model):
    """
    Predict the next token deterministically based on the token model.
    """
    if last_token in token_model:
        # Always pick the first option for determinism
        return token_model[last_token][0]
    return None


def cleanup_and_format_response(response):
    """
    Clean up the response by:
      - Splitting into sentences using punctuation.
      - Removing immediately consecutive duplicate sentences.
      - Prepending the custom header.
    """
    header = format_templates.get("header", "")
    sentences = re.split(r'(?<=[.!?])\s+', response.strip())
    cleaned = []
    for s in sentences:
        s_clean = s.strip()
        if s_clean:
            if not cleaned or s_clean.lower() != cleaned[-1].lower():
                cleaned.append(s_clean)
    return header + "\n" + "\n".join(cleaned)


def review_and_correct_response(response, token_model):
    """
    Review and correct the generated response iteratively until it meets quality standards.
    The AI will:
      - Check for coherence.
      - Avoid excessive repetition.
      - Refine the response using the token model.
    """
    max_iterations = 5
    for _ in range(max_iterations):
        tokens = tokenize_text(response)
        corrected_tokens = []
        seen_tokens = set()

        for token in tokens:
            if token not in seen_tokens:
                corrected_tokens.append(token)
                seen_tokens.add(token)
            else:
                # Predict a replacement token if repetition is detected
                next_token = predict_next_token(token, token_model)
                if next_token:
                    corrected_tokens.append(next_token)

        corrected_response = detokenize_tokens(corrected_tokens)
        if is_response_coherent(corrected_response):
            return corrected_response

        response = corrected_response  # Continue refining the response

    return response  # Return the best attempt after max iterations


def is_response_coherent(response):
    """
    Check if the response is coherent by ensuring:
      - It has no excessive repetition.
      - It forms complete sentences.
    """
    sentences = re.split(r'(?<=[.!?])\s+', response.strip())
    unique_sentences = set(sentences)
    return len(sentences) == len(unique_sentences) and all(len(s.split()) > 2 for s in sentences)


MEMORY_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "ai_memory.json")


def load_memory():
    """
    Load memory from the memory file. If the file doesn't exist or is invalid, return an empty list.
    """
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            memory = json.load(file)
            if not isinstance(memory, list):
                return []
            return memory
    return []

# NEW: Define update_memory() early so it is available when editing memory.


def update_memory(new_memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(new_memory, file, indent=4)


def save_to_memory(entry):
    """
    Save a new entry (input-response pair) to the memory file. Ensure memory is stored as a list.
    """
    memory = load_memory()
    if not isinstance(memory, list):
        memory = []
    memory.append(entry)
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


def review_memory(user_input):
    """
    Review past responses in memory to find related responses to the current input.
    Returns a list of related responses.
    """
    memory = load_memory()
    related_responses = []
    for entry in memory:
        # Ensure the entry is a dictionary with the expected keys
        if isinstance(entry, dict) and "input" in entry and "response" in entry:
            if user_input.lower() in entry["input"].lower():
                related_responses.append(entry["response"])
    return related_responses


def validate_response(user_input, response):
    """
    Validate the generated response by comparing it with past responses in memory.
    If the response is too similar to a past response, refine it.
    """
    past_responses = review_memory(user_input)
    for past_response in past_responses:
        if response.strip().lower() == past_response.strip().lower():
            # If the response is identical to a past response, refine it
            response += " (Refined based on memory)"
    return response


def get_valid_words():
    # Build a set of valid words from JSON arrays and vocabulary data.
    valid = set()
    # From word-level data.
    for entry in data:
        valid.add(entry["word"].lower())
    # From sentence-level responses.
    for entry in sentence_data:
        for word in entry["sentence"].split():
            valid.add(word.strip(".,!?").lower())
    # From conversation responses.
    for entry in conversation_data:
        for word in entry["response"].split():
            valid.add(word.strip(".,!?").lower())
    # From preset responses.
    for resp in responses.values():
        for word in resp.split():
            valid.add(word.strip(".,!?").lower())
    # From emotion data.
    for resp in emotion_data.values():
        for word in resp.split():
            valid.add(word.strip("{},!?").lower())
    # From vocabulary_data (include synonyms).
    for entry in vocabulary_data:
        valid.add(entry["word"].lower())
        for synonym in entry.get("synonyms", []):
            valid.add(synonym.lower())
    return valid

# Helper function to lookup vocabulary definitions.


def lookup_vocabulary(word):
    """
    Lookup vocabulary data for a given word.
    Returns a dictionary with 'definition', 'usage', and 'synonyms' if the word is found; otherwise, returns None.
    """
    lw = word.lower()
    for entry in vocabulary_data:
        if entry["word"].lower() == lw:
            return entry
    return None


def ensure_correct_words(response):
    """
    Correct words in the response using the valid words from JSON arrays
    instead of marking them as [INVALID_WORD].
    """
    valid_words = get_valid_words()
    corrected_response = []
    import difflib
    for word in response.split():
        clean_word = word.strip(".,!?")
        if not clean_word:
            corrected_response.append(word)
        elif clean_word.lower() in valid_words or word.istitle():
            corrected_response.append(word)
        else:
            matches = difflib.get_close_matches(
                clean_word.lower(), list(valid_words), n=1, cutoff=0.8)
            if matches:
                replaced = matches[0]
                if word[0].isupper():
                    replaced = replaced.capitalize()
                # Preserve punctuation from original word.
                punct = "".join(ch for ch in word if not ch.isalnum())
                corrected_response.append(replaced + punct)
            else:
                corrected_response.append(word)
    return " ".join(corrected_response)


def stream_response(response):
    import time
    for char in response:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()


def confirm_generation(response, token_model):
    """
    Confirmation phase: checks if all words in the response are among the valid words
    from the JSON arrays. If not, it iteratively reprocesses the response until it is confirmed
    or a maximum number of attempts is reached.
    """
    attempts = 3
    valid_set = get_valid_words()
    for _ in range(attempts):
        confirmed = True
        for word in response.split():
            clean_word = word.strip(".,!?").lower()
            if clean_word and clean_word not in valid_set and not word.istitle():
                confirmed = False
                break
        if confirmed:
            return response
        # reprocess the response with review_and_correct_response to try to yield better words/sentences
        response = review_and_correct_response(response, token_model)
    return response


# New Section: Neural Network Generation Module


def build_token_vocab(corpus):
    """
    Build a vocabulary dictionary mapping each unique token (number)
    to an index from the corpus generated via tokenize_text.
    """
    tokens = tokenize_text(corpus)
    vocab = sorted(set(tokens))
    token_to_idx = {token: idx for idx, token in enumerate(vocab)}
    idx_to_token = {idx: token for token, idx in token_to_idx.items()}
    return token_to_idx, idx_to_token


class RNNGenerator(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super(RNNGenerator, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.RNN(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden):
        embeds = self.embedding(x)
        out, hidden = self.rnn(embeds, hidden)
        out = self.fc(out)
        return out, hidden


def train_neural_model(corpus, num_epochs=10):
    """
    Train a small RNN on the tokenized corpus.
    """
    token_to_idx, idx_to_token = build_token_vocab(corpus)
    vocab_size = len(token_to_idx)
    embed_dim = 20
    hidden_dim = 30
    model = RNNGenerator(vocab_size, embed_dim, hidden_dim)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.09)

    tokens = tokenize_text(corpus)
    # Prepare training sequences (input: all tokens except last, target: all tokens except first)
    input_seq = tokens[:-1]
    target_seq = tokens[1:]
    X = torch.tensor([token_to_idx[t]
                     for t in input_seq], dtype=torch.long).unsqueeze(0)
    y = torch.tensor([token_to_idx[t]
                     for t in target_seq], dtype=torch.long).unsqueeze(0)

    for epoch in range(num_epochs):
        hidden = None
        optimizer.zero_grad()
        output, hidden = model(X, hidden)
        loss = criterion(output.view(-1, vocab_size), y.view(-1))
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")
    return model, token_to_idx, idx_to_token


def generate_neural_output(model, token_to_idx, idx_to_token, seed_tokens, num_generated=80):
    """
    Generate additional text using the trained neural model.
    """
    model.eval()
    input_indices = torch.tensor(
        [token_to_idx[t] for t in seed_tokens], dtype=torch.long).unsqueeze(0)
    hidden = None
    outputs = []
    with torch.no_grad():
        out, hidden = model(input_indices, hidden)
        last_idx = out[0, -1].argmax().item()
        outputs.append(last_idx)
        for _ in range(num_generated):
            input_tensor = torch.tensor([[last_idx]], dtype=torch.long)
            out, hidden = model(input_tensor, hidden)
            last_idx = out[0, -1].argmax().item()
            outputs.append(last_idx)
    # Convert generated indices back to tokens and then to text.
    generated_tokens = [idx_to_token[idx] for idx in outputs]
    return detokenize_tokens(generated_tokens)


# GLOBAL PARAMETER for context lookback (must be defined before its use)
CONTEXT_LOOKBACK = 50

# NEW FUNCTION: Iterative Neural Generation


def generate_iteratively(model, token_to_idx, idx_to_token, seed_tokens, total_tokens=1000, chunk_size=10, context_lookback=CONTEXT_LOOKBACK):
    """
    Generate output iteratively using only the last 'context_lookback' tokens as context.
    After each chunk, compress consecutive duplicates using the improved backspace simulation.
    Added a maximum iteration limit and break condition if no progress is made.
    """
    model.eval()
    generated = list(seed_tokens)  # start with seed tokens
    hidden = None
    default_idx = list(token_to_idx.values())[0]
    max_iterations = 15  # maximum iterations to prevent infinite loops
    iteration = 0
    while len(generated) < total_tokens and iteration < max_iterations:
        iteration += 1
        context = generated if context_lookback == 0 else generated[-context_lookback:]
        X = torch.tensor([[token_to_idx.get(t, default_idx)
                         for t in context]], dtype=torch.long)
        with torch.no_grad():
            output, hidden = model(X, hidden)
        chunk = []
        current_idx = output[0, -1].argmax().item()
        for _ in range(chunk_size):
            chunk.append(current_idx)
            input_tensor = torch.tensor([[current_idx]], dtype=torch.long)
            with torch.no_grad():
                out, hidden = model(input_tensor, hidden)
            current_idx = out[0, -1].argmax().item()
        # Compress duplicates and check progress
        new_generated = simulate_backspace_improved(generated, threshold=2)
        if new_generated == generated:
            break  # no change detected, break out to avoid infinite loop
        generated = new_generated + chunk
    return detokenize_tokens([idx_to_token[idx] for idx in generated[len(seed_tokens):]])

# NEW HELPER FUNCTION: Build vocabulary corpus from vocabulary_data.


def build_vocabulary_corpus():
    """
    Build additional corpus text from vocabulary data,
    including definitions and synonyms, to be used as additional training context.
    """
    corpus_text = ""
    for entry in vocabulary_data:
        syns = ", ".join(entry.get("synonyms", []))
        corpus_text += f"{entry['word']}: {entry['definition']} (synonyms: {syns}). "
    return corpus_text

# NEW HELPER FUNCTION: Simulate backspace editing.


def simulate_backspace(generated_tokens, threshold=3):
    """
    If the same token is repeated consecutively 'threshold' times, simulate a backspace by removing the last token.
    """
    if len(generated_tokens) >= threshold and all(t == generated_tokens[-1] for t in generated_tokens[-threshold:]):
        return generated_tokens[:-1]  # remove the last repeated token
    return generated_tokens

# NEW HELPER FUNCTION: Improved simulate backspace


def simulate_backspace_improved(generated_tokens, threshold=1):
    """
    Compress consecutive duplicate tokens.
    For non-period tokens, collapse duplicates to a single instance.
    For periods (ASCII 46), if the group size is exactly 2 or 3 (i.e. ".." or "..."), keep them;
    if more than 3 are consecutive, compress them to exactly 3.
    """
    if not generated_tokens:
        return generated_tokens
    new_tokens = []
    i = 0
    while i < len(generated_tokens):
        token = generated_tokens[i]
        count = 1
        while i + count < len(generated_tokens) and generated_tokens[i + count] == token:
            count += 1
        if token == 460:  # period character
            if count == 2 or count == 3:
                allowed = count
            elif count > 3:
                allowed = 3
            else:
                allowed = 1
        else:
            allowed = 1
        new_tokens.extend([token] * allowed)
        i += count
    return new_tokens

# NEW FUNCTION: Predict words ahead


def predict_words_ahead(model, token_to_idx, idx_to_token, seed_tokens, num_words=5):
    """
    Predict ahead until 'num_words' words are generated.
    Words are delimited by ASCII 64 (space).
    """
    model.eval()
    generated = list(seed_tokens)
    hidden = None
    predicted_words = []
    while len(predicted_words) < num_words:
        context = generated if CONTEXT_LOOKBACK == 0 else generated[-CONTEXT_LOOKBACK:]
        X = torch.tensor([[token_to_idx.get(t, list(token_to_idx.values())[0]) for t in context]],
                         dtype=torch.long)
        with torch.no_grad():
            output, hidden = model(X, hidden)
        next_idx = output[0, -1].argmax().item()
        generated.append(next_idx)
        # Convert current predicted token
        char = idx_to_token[next_idx]
        if char == 64:  # space delimiter
            # split generated text into words and count non-empty ones
            words = detokenize_tokens(generated).split()
            predicted_words = words
    return detokenize_tokens(generated[len(seed_tokens):])


# Integrate the neural network into generate_response.
# Add a global variable for the AI's own name.
AI_NAME = "HTP-1"


def handle_single_word(input_text):
    # If the input is a single word, return a clarifying message.
    if len(input_text.split()) == 1:
        return "I'm here! Can you elaborate on that?"
    return None

# NEW FUNCTION: determine_next_token


def determine_next_token(user_input, token_model):
    """
    Analyze user input and, using the token_model, determine an initial token for response generation.
    """
    tokens = tokenize_text(user_input)
    if tokens:
        determined = predict_next_token(tokens[-1], token_model)
        return determined if determined is not None else tokens[0]
    return " "


def generate_response(user_input):
    # Check for single-word input before proceeding.
    single_response = handle_single_word(user_input)
    if single_response is not None:
        return single_response
    # Check if the user is asking for the AI's name.
    if "your name" in user_input.lower():
        # Cache and return the answer immediately.
        RESPONSE_CACHE[user_input] = f"My name is {AI_NAME}."
        save_cache()
        return f"My name is {AI_NAME}."
    # Add bot's name to token placeholders.
    tokens_placeholder = {"username": "Maximus", "botname": AI_NAME}
    final_response = ""
    for attempt in range(3):
        # === Begin Generation Procedure ===
        matched_numbers = set()
        conv_resp = find_best_conversation_match(user_input)
        conv_text = replace_tokens(
            conv_resp, tokens_placeholder) if conv_resp else ""
        emotion_resp = extract_emotion_response(user_input, tokens_placeholder)
        for word in user_input.split():
            num = get_number_from_word(word)
            if num is None:
                _, num = find_best_match(word)
            if num is not None:
                matched_numbers.add(num)
        sentence_candidates = re.split(r'(?<=[.!?])\s+', user_input)
        for candidate in sentence_candidates:
            candidate = candidate.strip()
            if candidate:
                _, num = find_best_sentence_match(candidate)
                if num is not None:
                    matched_numbers.add(num)
        if len(user_input) > 50:
            _, num = find_best_paragraph_match(user_input)
            if num is not None:
                matched_numbers.add(num)
        combined_response = ""
        used_response_ids = set()
        for num in matched_numbers:
            if num in responses and num not in used_response_ids:
                combined_response += responses[num] + " "
                used_response_ids.add(num)
        if conv_text:
            combined_response = conv_text + " " + combined_response
        if emotion_resp:
            combined_response = emotion_resp + " " + combined_response
        if not combined_response.strip():
            combined_response = "AI: No response available for this input."
        else:
            combined_response = replace_tokens(
                combined_response, tokens_placeholder)
        replaced_responses = [replace_tokens(
            resp, tokens_placeholder) for resp in responses.values()]
        # Incorporate vocabulary corpus into the overall training corpus.
        vocab_corpus = build_vocabulary_corpus()
        corpus = (user_input + " ") * 3 + combined_response + " " + \
            conv_text + " " + " ".join(replaced_responses) + " " + vocab_corpus
        token_model = build_token_model(corpus)
        neural_model, token_to_idx, idx_to_token = train_neural_model(
            corpus, num_epochs=250)
        seed_text = conv_text if conv_text else combined_response
        tokens_seed = tokenize_text(seed_text)
        neural_iterative = ""
        if neural_model is not None and token_to_idx is not None:
            neural_iterative = generate_iteratively(
                neural_model, token_to_idx, idx_to_token, tokens_seed, total_tokens=50, chunk_size=5)
        determined_token = determine_next_token(user_input, token_model)
        generated_tokens = []
        num_generated = 20
        current_token = determined_token  # use the determined token as the starting point
        for _ in range(num_generated):
            next_token = predict_next_token(current_token, token_model)
            if next_token is None:
                break
            generated_tokens.append(next_token)
            current_token = next_token
        generated_extension = detokenize_tokens(generated_tokens)
        initial_response = combined_response + " " + generated_extension
        combined_final = initial_response + " " + neural_iterative
        final_response = review_and_correct_response(
            combined_final, token_model)
        final_response = validate_response(user_input, final_response)
        final_response = ensure_correct_words(final_response)
        final_response = confirm_generation(final_response, token_model)
        # NEW: Refine final response using punctuation cleanup and similar memory.
        final_response = refine_response_with_memory(
            final_response, user_input)
        # === End Generation Procedure ===

        prev = {resp.strip().lower() for resp in review_memory(user_input)}
        if final_response.strip().lower() not in prev:
            break
        else:
            print(
                f"Duplicate response detected, regenerating... Attempt {attempt+1}")
    if final_response.strip().lower() in prev:
        final_response += " (Fixed response)"
    save_to_memory({"input": user_input, "response": final_response})
    return cleanup_and_format_response(final_response)

# NEW FUNCTION: Refine response punctuation and spacing using regex cleanup.


def refine_response_with_memory(response, user_input):
    # Retrieve similar memory responses using input matching.
    memory = load_memory()
    similar = [entry["response"]
               for entry in memory if user_input.lower() in entry.get("input", "").lower()]
    # Clean up spacing around punctuation.
    # remove extra space before punctuation
    refined = re.sub(r'\s+([,.!?])', r'\1', response)
    # ensure one space after punctuation
    refined = re.sub(r'([,.!?])([^\s])', r'\1 \2', refined)
    # If similar memory exists and looks reasonably formatted, use it as basis.
    if similar:
        best_match = similar[0]
        if abs(len(best_match) - len(refined)) < len(best_match) * 0.5:
            refined = best_match
    return refined

# ==============================================================
# 3. Chat / Terminal Interface Integration
# ==============================================================

# NEW HELPER FUNCTION: Display memory entries.


def display_memory():
    """Display all memory entries with their index, input, and response."""
    memory = load_memory()
    if not memory:
        print("No memory stored.")
    else:
        print("----- Memory Entries -----")
        for i, entry in enumerate(memory):
            print(
                f"[{i}] Input: {entry.get('input','')} | Response: {entry.get('response','')}")
        print("--------------------------")


# In browser mode, we use Brython’s document and HTML to create a chat UI.
if IS_BROWSER:
    def add_message(sender, text):
        """Add a message bubble to the chatBox element."""
        chat_box = document["chatBox"]
        new_div = html.DIV(text, Class=f"message {sender}")
        chat_box <= new_div
        chat_box.scrollTop = chat_box.scrollHeight

    def send_message(event):
        """Callback when the user sends a message via the UI."""
        user_input_el = document["userInput"]
        user_text = user_input_el.value.strip()
        if not user_text:
            return
        add_message("user", user_text)
        user_input_el.value = ""
        # Display a temporary 'thinking...' indicator.
        thinking_div = html.DIV("AI is thinking...",
                                Class="message ai thinking")
        document["chatBox"] <= thinking_div

        def complete_response():
            thinking_div.remove()
            ai_reply = generate_response(user_text)
            add_message("ai", ai_reply)

        timer.set_timeout(complete_response, 1500)

    document["sendBtn"].bind("click", send_message)

# In Terminal mode, interact via console input/output.
else:
    if __name__ == '__main__':
        while True:
            print("Select mode:")
            print("1. Chat")
            print("2. Edit Memory")
            print("q. Quit")
            mode = input("Enter your choice: ").strip()
            if mode.lower() == 'q':
                break
            if mode == '1':
                # Chat mode (existing code)
                print("Interactive AI Chat (type 'quit' or 'exit' to leave)")
                while True:
                    user_text = input("You: ").strip()
                    if user_text.lower() in ['quit', 'exit']:
                        break
                    reply = generate_response(user_text)
                    print("AI: ", end='', flush=True)
                    stream_response(reply)
            elif mode == '2':
                # Display memory before editing.
                display_memory()

                # Memory edit mode: select operation mode: single select or multi-select deletion
                print("Memory Edit Mode:")
                print(
                    "Enter 's' for single selection (edit or deletion) or 'm' for multi-select deletion.")
                edit_mode = input("Your choice (s/m): ").strip().lower()
                memory = load_memory()
                if not memory:
                    print("No memory stored.")
                    continue
                # display_memory()
                if edit_mode == 's':
                    # Single selection mode: choose one index to either edit or delete.
                    sel = input("Enter the index number to select: ").strip()
                    try:
                        idx = int(sel)
                        if idx < 0 or idx >= len(memory):
                            print("Invalid index.")
                            continue
                    except ValueError:
                        print("Please enter a valid number.")
                        continue
                    print("Selected Entry:")
                    print(
                        f"{idx}: Input: '{memory[idx].get('input','')}' | Response: '{memory[idx].get('response','')}'")
                    print("Press 1 to Edit, 2 to Delete this entry")
                    action = input("Enter your choice: ").strip()
                    if action == '1':
                        new_resp = input("Enter new response text: ").strip()
                        memory[idx]["response"] = new_resp
                        update_memory(memory)
                        print("Memory updated.")
                    elif action == '2':
                        del memory[idx]
                        update_memory(memory)
                        print("Memory entry deleted.")
                    else:
                        print("Invalid choice.")
                elif edit_mode == 'm':
                    # Multi-select deletion mode.
                    print(
                        "Enter indices to delete one by one. Type 'd' when finished selection.")
                    indices_to_delete = []
                    while True:
                        selection = input(
                            "Enter index (or 'd' to finish): ").strip()
                        if selection.lower() == 'd':
                            break
                        try:
                            idx = int(selection)
                            if idx < 0 or idx >= len(memory):
                                print("Invalid index.")
                            else:
                                if idx not in indices_to_delete:
                                    indices_to_delete.append(idx)
                                    print(f"Index {idx} selected.")
                                else:
                                    print("Index already selected.")
                        except ValueError:
                            print("Please enter a valid number or 'd'.")
                    if not indices_to_delete:
                        print("No indices selected.")
                        continue
                    print("Selected Entries for deletion:")
                    for idx in indices_to_delete:
                        print(
                            f"{idx}: Input: '{memory[idx].get('input','')}' | Response: '{memory[idx].get('response','')}'")
                    confirm = input("Confirm deletion? (y/n): ").strip()
                    if confirm.lower() == 'y':
                        for idx in sorted(indices_to_delete, reverse=True):
                            del memory[idx]
                        update_memory(memory)
                        print("Selected memory entries deleted.")
                    else:
                        print("Deletion cancelled.")
                else:
                    print("Invalid selection mode.")
# NEW FUNCTION: Overwrite memory file with updated memory list.


def update_memory(new_memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(new_memory, file, indent=4)

# ==============================================================


# Add these near the top with other global definitions
CACHE_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "ai_cache.json")
RESPONSE_CACHE = {}
MODEL_CACHE = {}
TRAINING_CACHE = {
    'corpus_hash': {},  # Store hashes of training data
    'model_states': {},  # Store trained model states
    'embeddings': {},   # Store word embeddings
    'token_maps': {}    # Store token-to-index mappings
}


def save_cache():
    """Save cache to disk"""
    cache_data = {
        'response_cache': RESPONSE_CACHE,
        'training_cache': TRAINING_CACHE
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f)


def load_cache():
    """Load cache from disk"""
    global RESPONSE_CACHE, TRAINING_CACHE
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cache_data = json.load(f)
                RESPONSE_CACHE = cache_data.get('response_cache', {})
                TRAINING_CACHE = cache_data.get('training_cache', {
                    'corpus_hash': {},
                    'model_states': {},
                    'embeddings': {},
                    'token_maps': {}
                })
        except:
            print("Cache file corrupted, starting fresh")
            RESPONSE_CACHE = {}
            TRAINING_CACHE = {
                'corpus_hash': {},
                'model_states': {},
                'embeddings': {},
                'token_maps': {}
            }


def compute_corpus_hash(corpus):
    """Compute hash of corpus for cache lookup"""
    import hashlib
    return hashlib.md5(corpus.encode()).hexdigest()

# Modify train_neural_model to use cache


def train_neural_model(corpus, num_epochs=10):
    """Train neural model with caching"""
    corpus_hash = compute_corpus_hash(corpus)

    # Check cache first
    if corpus_hash in TRAINING_CACHE['corpus_hash']:
        cached_model_state = TRAINING_CACHE['model_states'].get(corpus_hash)
        cached_token_maps = TRAINING_CACHE['token_maps'].get(corpus_hash)

        if cached_model_state and cached_token_maps:
            # Reconstruct model from cache
            token_to_idx, idx_to_token = cached_token_maps
            vocab_size = len(token_to_idx)
            model = RNNGenerator(vocab_size, embed_dim=10, hidden_dim=20)
            model.load_state_dict(cached_model_state)
            return model, token_to_idx, idx_to_token

    # If not in cache, train normally
    token_to_idx, idx_to_token = build_token_vocab(corpus)
    vocab_size = len(token_to_idx)
    model = RNNGenerator(vocab_size, embed_dim=10, hidden_dim=20)

    # Prepare training sequences (input: all tokens except last, target: all tokens except first)
    tokens = tokenize_text(corpus)
    input_seq = tokens[:-1]
    target_seq = tokens[1:]
    X = torch.tensor([token_to_idx[t]
                     for t in input_seq], dtype=torch.long).unsqueeze(0)
    y = torch.tensor([token_to_idx[t]
                     for t in target_seq], dtype=torch.long).unsqueeze(0)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(num_epochs):
        hidden = None
        optimizer.zero_grad()
        output, hidden = model(X, hidden)
        loss = criterion(output.view(-1, vocab_size), y.view(-1))
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")

    # Cache the results
    TRAINING_CACHE['corpus_hash'][corpus_hash] = True
    TRAINING_CACHE['model_states'][corpus_hash] = model.state_dict()
    TRAINING_CACHE['token_maps'][corpus_hash] = (token_to_idx, idx_to_token)
    save_cache()

    return model, token_to_idx, idx_to_token

# Modify generate_response to use response cache


def generate_response(user_input):
    # Check response cache first
    if user_input in RESPONSE_CACHE:
        return RESPONSE_CACHE[user_input]

    # Check if the user is asking for the AI's name.
    if "your name" in user_input.lower():
        # Cache and return the answer immediately.
        RESPONSE_CACHE[user_input] = f"My name is {AI_NAME}."
        save_cache()
        return f"My name is {AI_NAME}."
    # Add bot's name to token placeholders.
    tokens_placeholder = {"username": "Maximus", "botname": AI_NAME}
    final_response = ""
    for attempt in range(3):
        # === Begin Generation Procedure ===
        matched_numbers = set()
        conv_resp = find_best_conversation_match(user_input)
        conv_text = replace_tokens(
            conv_resp, tokens_placeholder) if conv_resp else ""
        emotion_resp = extract_emotion_response(user_input, tokens_placeholder)
        for word in user_input.split():
            num = get_number_from_word(word)
            if num is None:
                _, num = find_best_match(word)
            if num is not None:
                matched_numbers.add(num)
        sentence_candidates = re.split(r'(?<=[.!?])\s+', user_input)
        for candidate in sentence_candidates:
            candidate = candidate.strip()
            if candidate:
                _, num = find_best_sentence_match(candidate)
                if num is not None:
                    matched_numbers.add(num)
        if len(user_input) > 50:
            _, num = find_best_paragraph_match(user_input)
            if num is not None:
                matched_numbers.add(num)
        combined_response = ""
        used_response_ids = set()
        for num in matched_numbers:
            if num in responses and num not in used_response_ids:
                combined_response += responses[num] + " "
                used_response_ids.add(num)
        if conv_text:
            combined_response = conv_text + " " + combined_response
        if emotion_resp:
            combined_response = emotion_resp + " " + combined_response
        if not combined_response.strip():
            combined_response = "AI: No response available for this input."
        else:
            combined_response = replace_tokens(
                combined_response, tokens_placeholder)
        replaced_responses = [replace_tokens(
            resp, tokens_placeholder) for resp in responses.values()]
        # Incorporate vocabulary corpus into the overall training corpus.
        vocab_corpus = build_vocabulary_corpus()
        corpus = (user_input + " ") * 3 + combined_response + " " + \
            conv_text + " " + " ".join(replaced_responses) + " " + vocab_corpus
        token_model = build_token_model(corpus)
        neural_model, token_to_idx, idx_to_token = train_neural_model(
            corpus, num_epochs=10)
        seed_text = conv_text if conv_text else combined_response
        tokens_seed = tokenize_text(seed_text)
        neural_iterative = ""
        if neural_model is not None and token_to_idx is not None:
            neural_iterative = generate_iteratively(
                neural_model, token_to_idx, idx_to_token, tokens_seed, total_tokens=50, chunk_size=5)
        determined_token = determine_next_token(user_input, token_model)
        generated_tokens = []
        num_generated = 20
        current_token = determined_token  # use the determined token as the starting point
        for _ in range(num_generated):
            next_token = predict_next_token(current_token, token_model)
            if next_token is None:
                break
            generated_tokens.append(next_token)
            current_token = next_token
        generated_extension = detokenize_tokens(generated_tokens)
        initial_response = combined_response + " " + generated_extension
        combined_final = initial_response + " " + neural_iterative
        final_response = review_and_correct_response(
            combined_final, token_model)
        final_response = validate_response(user_input, final_response)
        final_response = ensure_correct_words(final_response)
        final_response = confirm_generation(final_response, token_model)
        # NEW: Refine final response using punctuation cleanup and similar memory.
        final_response = refine_response_with_memory(
            final_response, user_input)
        # === End Generation Procedure ===

        prev = {resp.strip().lower() for resp in review_memory(user_input)}
        if final_response.strip().lower() not in prev:
            break
        else:
            print(
                f"Duplicate response detected, regenerating... Attempt {attempt+1}")
    if final_response.strip().lower() in prev:
        final_response += " (Enhanced)"
    save_to_memory({"input": user_input, "response": final_response})
    # Cache the final response
    RESPONSE_CACHE[user_input] = final_response
    save_cache()

    return cleanup_and_format_response(final_response)

# Add cache cleanup function


def cleanup_cache(max_size=1000):
    """Remove oldest entries if cache exceeds max_size"""
    if len(RESPONSE_CACHE) > max_size:
        # Convert to list to get oldest entries
        items = list(RESPONSE_CACHE.items())
        # Keep only the most recent max_size items
        RESPONSE_CACHE.clear()
        RESPONSE_CACHE.update(dict(items[-max_size:]))

    # Cleanup training cache
    if len(TRAINING_CACHE['corpus_hash']) > max_size:
        corpus_hashes = list(TRAINING_CACHE['corpus_hash'].keys())
        for old_hash in corpus_hashes[:-max_size]:
            TRAINING_CACHE['corpus_hash'].pop(old_hash, None)
            TRAINING_CACHE['model_states'].pop(old_hash, None)
            TRAINING_CACHE['embeddings'].pop(old_hash, None)
            TRAINING_CACHE['token_maps'].pop(old_hash, None)

    save_cache()


# Load cache at startup
load_cache()

# Add periodic cache cleanup to main loop
if __name__ == '__main__':
    load_cache()  # Load cache at startup
    while True:
        print("Select mode:")
        print("1. Chat")
        print("2. Edit Memory")
        print("q. Quit")
        mode = input("Enter your choice: ").strip()
        if mode.lower() == 'q':
            break
        if mode == '1':
            # Chat mode (existing code)
            print("Interactive AI Chat (type 'quit' or 'exit' to leave)")
            while True:
                user_text = input("You: ").strip()
                if user_text.lower() in ['quit', 'exit']:
                    break
                reply = generate_response(user_text)
                print("AI: ", end='', flush=True)
                stream_response(reply)
        elif mode == '2':
            # Display memory before editing.
            display_memory()

            # Memory edit mode: select operation mode: single select or multi-select deletion
            print("Memory Edit Mode:")
            print(
                "Enter 's' for single selection (edit or deletion) or 'm' for multi-select deletion.")
            edit_mode = input("Your choice (s/m): ").strip().lower()
            memory = load_memory()
            if not memory:
                print("No memory stored.")
                continue
            # display_memory()
            if edit_mode == 's':
                # Single selection mode: choose one index to either edit or delete.
                sel = input("Enter the index number to select: ").strip()
                try:
                    idx = int(sel)
                    if idx < 0 or idx >= len(memory):
                        print("Invalid index.")
                        continue
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                print("Selected Entry:")
                print(
                    f"{idx}: Input: '{memory[idx].get('input','')}' | Response: '{memory[idx].get('response','')}'")
                print("Press 1 to Edit, 2 to Delete this entry")
                action = input("Enter your choice: ").strip()
                if action == '1':
                    new_resp = input("Enter new response text: ").strip()
                    memory[idx]["response"] = new_resp
                    update_memory(memory)
                    print("Memory updated.")
                elif action == '2':
                    del memory[idx]
                    update_memory(memory)
                    print("Memory entry deleted.")
                else:
                    print("Invalid choice.")
            elif edit_mode == 'm':
                # Multi-select deletion mode.
                print(
                    "Enter indices to delete one by one. Type 'd' when finished selection.")
                indices_to_delete = []
                while True:
                    selection = input(
                        "Enter index (or 'd' to finish): ").strip()
                    if selection.lower() == 'd':
                        break
                    try:
                        idx = int(selection)
                        if idx < 0 or idx >= len(memory):
                            print("Invalid index.")
                        else:
                            if idx not in indices_to_delete:
                                indices_to_delete.append(idx)
                                print(f"Index {idx} selected.")
                            else:
                                print("Index already selected.")
                    except ValueError:
                        print("Please enter a valid number or 'd'.")
                if not indices_to_delete:
                    print("No indices selected.")
                    continue
                print("Selected Entries for deletion:")
                for idx in indices_to_delete:
                    print(
                        f"{idx}: Input: '{memory[idx].get('input','')}' | Response: '{memory[idx].get('response','')}'")
                confirm = input("Confirm deletion? (y/n): ").strip()
                if confirm.lower() == 'y':
                    for idx in sorted(indices_to_delete, reverse=True):
                        del memory[idx]
                    update_memory(memory)
                    print("Selected memory entries deleted.")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid selection mode.")

        # Add periodic cache cleanup
        cleanup_cache()
