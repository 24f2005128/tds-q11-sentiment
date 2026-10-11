from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


class SentimentRequest(BaseModel):
    sentences: list[str]


happy_words = [
    "love", "loved", "loving", "amazing", "awesome", "wonderful",
    "excited", "joy", "happy", "happiest", "fantastic", "overjoyed",
    "delighted", "blessed", "bliss", "beautiful", "ecstatic", "thrilled",
    "grateful", "proud", "fortunate", "spectacular", "celebrating",
    "celebrate", "pure joy", "dream come true", "cloud nine",
    "jumping for joy", "grinning", "smiling", "alive and energized",
    "exceeded", "best day", "wonderful surprise", "opportunity"
]

sad_words = [
    "worst", "terrible", "sad", "heartbroken", "failed", "tears",
    "lost", "devastated", "disappointed", "rejected", "falling apart",
    "depression", "ended badly", "hopeless", "pain", "miserable",
    "accident", "defeated", "sorrow", "failure", "empty inside",
    "anxiety", "lonely", "abandoned", "grief", "worried", "shattered",
    "betrayal", "overwhelmed with sadness", "regret", "crushed",
    "problems", "struggling", "suffering", "everything in the fire",
    "burdened", "crying", "broken"
]


def classify(text: str) -> str:
    t = text.lower()

    # Explicit negative phrases first
    if any(word in t for word in sad_words):
        return "sad"

    if any(word in t for word in happy_words):
        return "happy"

    return "neutral"


@app.post("/sentiment")
async def sentiment(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": classify(sentence)
            }
            for sentence in request.sentences
        ]
    }
