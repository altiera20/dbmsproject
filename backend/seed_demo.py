#!/usr/bin/env python3
"""Populate Threaddit with demo data that covers the full product surface."""

from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone

import bcrypt
import psycopg2
from dotenv import dotenv_values

NOW = datetime.now(timezone.utc)
PASSWORD = "password123"
HASH = bcrypt.hashpw(PASSWORD.encode(), bcrypt.gensalt()).decode()
RNG = random.Random(42)


def hours_ago(hours: float) -> datetime:
    return NOW - timedelta(hours=hours)


def days_ago(days: float) -> datetime:
    return NOW - timedelta(days=days)


def avatar(seed: str) -> str:
    return f"https://api.dicebear.com/7.x/adventurer/png?seed={seed}&size=128"


def logo(seed: str) -> str:
    return f"https://api.dicebear.com/7.x/identicon/png?seed={seed}&size=256"


USERS = [
    ("DemoUser", "demo@threaddit.local", "Logged-in demo account. Join threads, vote, comment, save posts, and check inbox."),
    ("Admin", "admin@threaddit.local", "Site administrator. Can moderate any community."),
    ("NovaCoder", "nova@threaddit.local", "Builds side projects at 2am and pretends that is a personality."),
    ("PixelSage", "pixel@threaddit.local", "Takes photos, then takes more photos of the photos."),
    ("ByteBard", "byte@threaddit.local", "Writes code like poetry and poetry like bug reports."),
    ("LunaPark", "luna@threaddit.local", "Always down for a snack rec and a hot take."),
    ("OakThread", "oak@threaddit.local", "Slow living, fast replies. Moderator energy."),
    ("MiraVolt", "mira@threaddit.local", "Hardware tinkerer. If it sparks, I probably meant to do that."),
    ("KaiNotes", "kai@threaddit.local", "Reads one extra paper so you do not have to."),
    ("RioSketch", "rio@threaddit.local", "Storyboards, stickers, and too many tabs."),
    ("AdaLoop", "ada@threaddit.local", "Compilers, cats, and carefully named variables."),
    ("ZenHarvest", "zen@threaddit.local", "Gardens, bread, and unusually calm arguments."),
    ("FoxCircuit", "fox@threaddit.local", "Retro games and modern bugs."),
    ("IvyQuill", "ivy@threaddit.local", "Books first, notifications never."),
    ("SamOrbit", "sam@threaddit.local", "Space nerd with a playlist for every launch."),
    ("TheoLens", "theo@threaddit.local", "Cinema takes served extra salty."),
    ("NiaForge", "nia@threaddit.local", "Lifts, logs, and leftover pasta."),
    ("ColeSpark", "cole@threaddit.local", "Stand-up notes in a grocery list app."),
    ("JadeVector", "jade@threaddit.local", "Design systems and sidewalk chalk."),
    ("RemyCloud", "remy@threaddit.local", "Always traveling toward the next bakery."),
    ("QuinnByte", "quinn@threaddit.local", "Security-minded, snack-motivated."),
    ("AriMaple", "ari@threaddit.local", "Folk songs and filesystem rants."),
    ("LeoNimbus", "leo@threaddit.local", "Weather, widgets, and weekend hikes."),
    ("PiaCopper", "pia@threaddit.local", "Home cooking experiments, 60% success rate."),
    ("WesHarbor", "wes@threaddit.local", "Board games until the trains stop running."),
]

THREADS = [
    ("t/AskThreaddit", "Questions, advice, and the occasional overly honest answer.", "AskThreaddit"),
    ("t/News", "Headlines, context, and comments that go off the rails.", "News"),
    ("t/Programming", "Bugs, PRs, and the joy of it finally compiling.", "Programming"),
    ("t/Science", "Papers, explainers, and curious rabbit holes.", "Science"),
    ("t/Gaming", "Boss fights, backlog guilt, and couch co-op.", "Gaming"),
    ("t/Movies", "Spoilers behind markdown, opinions in bold.", "Movies"),
    ("t/Music", "Playlists, live shows, and that one chorus on loop.", "Music"),
    ("t/Food", "Recipes, disasters, and midnight snacks.", "Food"),
    ("t/Photography", "Light, grain, and the hunt for one honest frame.", "Photography"),
    ("t/Fitness", "Form checks, PRs, and rest-day philosophy.", "Fitness"),
    ("t/Books", "Currently reading, forever recommending.", "Books"),
    ("t/Funny", "The timeline's unofficial comedy club.", "Funny"),
    ("t/DIY", "Make it, break it, then make it again.", "DIY"),
    ("t/Travel", "Itineraries, missed trains, and perfect noodles.", "Travel"),
    ("t/Memes", "Templates, remixes, and peak internet.", "Memes"),
]

IMAGES = [
    "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1461988320302-91bde64fc8e4?auto=format&fit=crop&w=1200&q=80",
]

GIFS = [
    "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif",
]

VIDEOS = [
    "https://www.youtube.com/watch?v=aqz-KE-bpKQ",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    "https://www.youtube.com/watch?v=jNQXAC9IVRw",
]

MARKDOWN_BODIES = [
    """This is a **markdown** post so the renderer has something to chew on.

- One idea
- A second idea
- A third idea that got out of hand

> Quoted because it sounded smarter that way.

Use `code` when you mean it, and try not to ship on a Friday.""",
    """## Quick notes

1. The first draft was worse.
2. The second draft was longer.
3. This is the version I am pretending is final.

If you made it here, leave a comment with your own revision.""",
    """Honest take:

I liked it more than I expected. Not perfect, still worth the evening.

**Would repeat.** *Would also nap first.*""",
    """Checklist before you pile on:

- Did you read the whole thing?
- Did you check the date?
- Are you adding signal or just volume?

Carry on.""",
]


def showcase_posts() -> list[dict]:
    """Hand-written posts that hit specific UI features."""
    return [
        {
            "thread": "t/Programming",
            "author": "NovaCoder",
            "title": "Flask + React still slaps",
            "content": MARKDOWN_BODIES[0],
            "media": IMAGES[3],
            "hours": 3,
            "edited": True,
            "hot": True,
        },
        {
            "thread": "t/Photography",
            "author": "PixelSage",
            "title": "Golden hour on the ridge",
            "content": "No filter except waiting fifteen extra minutes.",
            "media": IMAGES[1],
            "hours": 8,
        },
        {
            "thread": "t/Memes",
            "author": "ColeSpark",
            "title": "When the build finally passes",
            "content": "This is the whole mood today.",
            "media": GIFS[0],
            "hours": 5,
        },
        {
            "thread": "t/Movies",
            "author": "TheoLens",
            "title": "Big Buck Bunny still rules",
            "content": "A public-domain classic for the video player demo.",
            "media": VIDEOS[1],
            "hours": 12,
        },
        {
            "thread": "t/Music",
            "author": "AriMaple",
            "title": "The first YouTube video",
            "content": "Embedded via URL so React Player has work to do.",
            "media": VIDEOS[2],
            "hours": 20,
        },
        {
            "thread": "t/AskThreaddit",
            "author": "DemoUser",
            "title": "What are you building?",
            "content": MARKDOWN_BODIES[1],
            "media": None,
            "hours": 2,
            "hot": True,
        },
        {
            "thread": "t/Food",
            "author": "PiaCopper",
            "title": "Midnight pasta, no notes",
            "content": "Garlic, chili, and the last of the parsley.",
            "media": IMAGES[5],
            "hours": 6,
        },
        {
            "thread": "t/News",
            "author": "KaiNotes",
            "title": "Open data week roundup",
            "content": MARKDOWN_BODIES[3],
            "media": None,
            "hours": 14,
            "edited": True,
        },
        {
            "thread": "t/Gaming",
            "author": "FoxCircuit",
            "title": "Co-op night went long",
            "content": "We said one more run. That was four hours ago.",
            "media": IMAGES[8],
            "hours": 9,
            "hot": True,
        },
        {
            "thread": "t/Science",
            "author": "SamOrbit",
            "title": "A quiet night sky",
            "content": "Telescope on the balcony, city glow and all.",
            "media": IMAGES[9],
            "hours": 28,
        },
        {
            "thread": "t/Travel",
            "author": "RemyCloud",
            "title": "Train window, somewhere",
            "content": "No itinerary. Just the next bakery.",
            "media": IMAGES[10],
            "hours": 40,
        },
        {
            "thread": "t/Fitness",
            "author": "NiaForge",
            "title": "Form check: deadlifts",
            "content": "Bar stays close. Pride stays farther.",
            "media": IMAGES[11],
            "hours": 16,
        },
        {
            "thread": "t/Books",
            "author": "IvyQuill",
            "title": "Finished it on the bus",
            "content": "Missed my stop. Worth it. **No spoilers** in the title.",
            "media": IMAGES[12],
            "hours": 22,
        },
        {
            "thread": "t/Funny",
            "author": "WesHarbor",
            "title": "The group chat at 1am",
            "content": None,
            "media": GIFS[1],
            "hours": 4,
        },
        {
            "thread": "t/DIY",
            "author": "MiraVolt",
            "title": "Shelf that almost held",
            "content": "Stud finder lied. Wall did not.",
            "media": IMAGES[15],
            "hours": 30,
            "edited": True,
        },
        {
            "thread": "t/Music",
            "author": "LunaPark",
            "title": "Tiny venue, huge chorus",
            "content": "Phone recording because I could not help it.",
            "media": VIDEOS[0],
            "hours": 18,
        },
        {
            "thread": "t/Photography",
            "author": "TheoLens",
            "title": "Fog ate the skyline",
            "content": "And I am not even mad.",
            "media": IMAGES[2],
            "hours": 1.5,
        },
        {
            "thread": "t/Programming",
            "author": "AdaLoop",
            "title": "Off-by-one of the week",
            "content": "It was the fencepost. It is always the fencepost.",
            "media": None,
            "hours": 0.8,
        },
        {
            "thread": "t/Memes",
            "author": "DemoUser",
            "title": "Deploying on a Friday",
            "content": "I would never. I would also maybe.",
            "media": GIFS[2],
            "hours": 7,
        },
        {
            "thread": "t/AskThreaddit",
            "author": "OakThread",
            "title": "Best small daily habit?",
            "content": "Looking for something under five minutes that actually sticks.",
            "media": None,
            "hours": 11,
            "hot": True,
        },
    ]


GENERIC_TITLES = [
    "A quiet win today",
    "Unpopular but true",
    "Help me name this",
    "Weekend recap",
    "I was not ready",
    "Tiny detail, huge mood",
    "Rate this setup",
    "First time posting",
    "Saw this and ran",
    "Still thinking about it",
    "Need a second opinion",
    "The comments will fight",
    "Worth the detour",
    "Tried it so you know",
    "Hot take, chilled later",
    "Before and after",
    "Dropped this here",
    "Someone had to say it",
    "Save this for later",
    "Not the headline",
]


def extra_posts(n: int = 90) -> list[dict]:
    posts = []
    authors = [u[0] for u in USERS]
    thread_names = [t[0] for t in THREADS]
    for i in range(n):
        title = GENERIC_TITLES[i % len(GENERIC_TITLES)]
        if i % 4 == 0:
            title = f"{title} #{i + 1}"
        title = title[:30]
        age_hours = RNG.choice(
            [
                RNG.uniform(0.2, 20),
                RNG.uniform(24, 6 * 24),
                RNG.uniform(8 * 24, 25 * 24),
                RNG.uniform(40 * 24, 200 * 24),
            ]
        )
        media_roll = RNG.random()
        media = None
        if media_roll < 0.45:
            media = IMAGES[i % len(IMAGES)]
        elif media_roll < 0.52:
            media = GIFS[i % len(GIFS)]
        elif media_roll < 0.58:
            media = VIDEOS[i % len(VIDEOS)]
        posts.append(
            {
                "thread": thread_names[i % len(thread_names)],
                "author": authors[i % len(authors)],
                "title": title,
                "content": MARKDOWN_BODIES[i % len(MARKDOWN_BODIES)] if RNG.random() < 0.7 else None,
                "media": media,
                "hours": age_hours,
                "edited": i % 11 == 0,
            }
        )
    return posts


COMMENT_TEXTS = [
    "Came here to say this.",
    "This is the take I needed.",
    "Respectfully disagree, but I like the framing.",
    "Saving this for later.",
    "The markdown made it 10% smarter.",
    "I tried this last week. Same result.",
    "Can you expand on the second point?",
    "**Bold** of you to post this on a weekday.",
    "The comments are doing the most and I am here for it.",
    "This aged well in like four hours.",
    "I have a nested reply forming in real time.",
    "Officially a thread now.",
    "The video player worked. That is the post.",
    "That photo is doing a lot of quiet work.",
    "Edited because I remembered the actual point.",
    "As a lurker, I have thoughts.",
    "This belongs on hot, not just new.",
    "I upvoted, then I upvoted the replies too.",
    "> quoted because it was the line",
    "Okay but the sidebar communities are stacked.",
]


def main() -> None:
    uri = dotenv_values()["DATABASE_URI"]
    conn = psycopg2.connect(uri)
    conn.autocommit = False
    cur = conn.cursor()

    cur.execute(
        """
        TRUNCATE TABLE
            comments, posts, reactions, saved, subscriptions,
            user_roles, messages, subthreads, users
        RESTART IDENTITY CASCADE
        """
    )

    user_ids: dict[str, int] = {}
    for i, (username, email, bio) in enumerate(USERS):
        created = days_ago(400 - i * 12)
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash, avatar, bio, registration_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (username, email, HASH, avatar(username), bio, created),
        )
        user_ids[username] = cur.fetchone()[0]

    thread_ids: dict[str, int] = {}
    creator_cycle = [u[0] for u in USERS[2:]]
    for i, (name, description, seed) in enumerate(THREADS):
        creator = creator_cycle[i % len(creator_cycle)]
        created = days_ago(350 - i * 8)
        cur.execute(
            """
            INSERT INTO subthreads (name, description, logo, created_by, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (name, description, logo(seed), user_ids[creator], created),
        )
        thread_ids[name] = cur.fetchone()[0]

    # role 1 = mod, role 2 = admin
    cur.execute(
        "INSERT INTO user_roles (user_id, role_id, subthread_id) VALUES (%s, 2, NULL)",
        (user_ids["Admin"],),
    )
    cur.execute(
        "INSERT INTO user_roles (user_id, role_id, subthread_id) VALUES (%s, 1, %s)",
        (user_ids["DemoUser"], thread_ids["t/AskThreaddit"]),
    )
    mod_map = {
        "NovaCoder": "t/Programming",
        "PixelSage": "t/Photography",
        "OakThread": "t/AskThreaddit",
        "TheoLens": "t/Movies",
        "NiaForge": "t/Fitness",
        "IvyQuill": "t/Books",
        "FoxCircuit": "t/Gaming",
        "PiaCopper": "t/Food",
        "RemyCloud": "t/Travel",
        "ColeSpark": "t/Funny",
        "MiraVolt": "t/DIY",
        "KaiNotes": "t/Science",
        "AriMaple": "t/Music",
        "LunaPark": "t/Memes",
        "LeoNimbus": "t/News",
    }
    for username, thread in mod_map.items():
        cur.execute(
            "INSERT INTO user_roles (user_id, role_id, subthread_id) VALUES (%s, 1, %s)",
            (user_ids[username], thread_ids[thread]),
        )

    usernames = [u[0] for u in USERS]
    for username in usernames:
        for thread_name, tid in thread_ids.items():
            subscribe = username == "DemoUser" or RNG.random() < 0.55
            if username == "DemoUser" and thread_name in {
                "t/AskThreaddit",
                "t/Programming",
                "t/Photography",
                "t/Food",
                "t/Memes",
                "t/Movies",
                "t/Gaming",
            }:
                subscribe = True
            if subscribe:
                cur.execute(
                    "INSERT INTO subscriptions (user_id, subthread_id) VALUES (%s, %s)",
                    (user_ids[username], tid),
                )

    all_posts = showcase_posts() + extra_posts(90)
    post_ids: list[int] = []
    hot_post_ids: list[int] = []
    demo_post_ids: list[int] = []

    for spec in all_posts:
        created = hours_ago(spec["hours"])
        cur.execute(
            """
            INSERT INTO posts (user_id, subthread_id, title, media, content, created_at, is_edited)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                user_ids[spec["author"]],
                thread_ids[spec["thread"]],
                spec["title"][:30],
                spec.get("media"),
                spec.get("content"),
                created,
                bool(spec.get("edited")),
            ),
        )
        pid = cur.fetchone()[0]
        post_ids.append(pid)
        if spec.get("hot"):
            hot_post_ids.append(pid)
        if spec["author"] == "DemoUser":
            demo_post_ids.append(pid)

    comment_ids: list[int] = []
    for idx, pid in enumerate(post_ids):
        n_top = 8 if pid in hot_post_ids else RNG.randint(1, 4)
        parents_for_post: list[int] = []
        for j in range(n_top):
            author = usernames[(idx + j + 3) % len(usernames)]
            text = COMMENT_TEXTS[(idx + j) % len(COMMENT_TEXTS)]
            edited = j == 0 and idx % 5 == 0
            created = hours_ago(max(0.1, (all_posts[idx]["hours"] if idx < len(all_posts) else 10) - j * 0.3))
            cur.execute(
                """
                INSERT INTO comments (user_id, post_id, parent_id, has_parent, content, created_at, is_edited)
                VALUES (%s, %s, NULL, FALSE, %s, %s, %s)
                RETURNING id
                """,
                (user_ids[author], pid, text, created, edited),
            )
            cid = cur.fetchone()[0]
            comment_ids.append(cid)
            parents_for_post.append(cid)

        # nested replies, 2 extra levels on hotter posts
        depth_parents = parents_for_post[: min(4, len(parents_for_post))]
        for level in range(2 if pid in hot_post_ids else 1):
            next_parents = []
            for pidx, parent in enumerate(depth_parents):
                author = usernames[(idx + pidx + level + 7) % len(usernames)]
                text = COMMENT_TEXTS[(idx + pidx + level + 4) % len(COMMENT_TEXTS)]
                if level == 1:
                    text = f"Replying down the tree: {text}"
                cur.execute(
                    """
                    INSERT INTO comments (user_id, post_id, parent_id, has_parent, content, created_at, is_edited)
                    VALUES (%s, %s, %s, TRUE, %s, %s, FALSE)
                    RETURNING id
                    """,
                    (user_ids[author], pid, parent, text, hours_ago(0.2 + level)),
                )
                child = cur.fetchone()[0]
                comment_ids.append(child)
                next_parents.append(child)
            depth_parents = next_parents

    # Votes: more upvotes on earlier/showcase posts so Top vs New vs Hot differ
    post_vote_pairs = set()
    for pid_index, pid in enumerate(post_ids):
        n_up = 22 - min(pid_index, 18) if pid_index < 20 else RNG.randint(1, 8)
        n_up = max(1, n_up)
        voters = usernames[:]
        RNG.shuffle(voters)
        for v_i, voter in enumerate(voters[: n_up + 3]):
            key = (user_ids[voter], pid)
            if key in post_vote_pairs:
                continue
            post_vote_pairs.add(key)
            upvote = v_i < n_up
            cur.execute(
                """
                INSERT INTO reactions (user_id, post_id, comment_id, is_upvote, created_at)
                VALUES (%s, %s, NULL, %s, %s)
                """,
                (user_ids[voter], pid, upvote, hours_ago(RNG.uniform(0.1, 40))),
            )

    comment_vote_pairs = set()
    for cid in comment_ids:
        voters = RNG.sample(usernames, k=RNG.randint(1, 8))
        for voter in voters:
            key = (user_ids[voter], cid)
            if key in comment_vote_pairs:
                continue
            comment_vote_pairs.add(key)
            cur.execute(
                """
                INSERT INTO reactions (user_id, post_id, comment_id, is_upvote, created_at)
                VALUES (%s, NULL, %s, %s, %s)
                """,
                (user_ids[voter], cid, RNG.random() > 0.12, hours_ago(RNG.uniform(0.1, 30))),
            )

    # Saved posts for DemoUser
    save_targets = post_ids[:12] + demo_post_ids
    for pid in dict.fromkeys(save_targets):
        cur.execute(
            "INSERT INTO saved (user_id, post_id, created_at) VALUES (%s, %s, %s)",
            (user_ids["DemoUser"], pid, hours_ago(RNG.uniform(1, 72))),
        )

    messages = [
        ("NovaCoder", "DemoUser", "Did you see the Flask + React post? The comment tree is wild.", False, 2),
        ("DemoUser", "NovaCoder", "Just voted. That nested reply is doing too much in the best way.", True, 1.5),
        ("PixelSage", "DemoUser", "Mind if I steal the ridge photo framing for a thread banner?", False, 5),
        ("IvyQuill", "DemoUser", "Saving your AskThreaddit post. Also: what are you reading?", True, 8),
        ("DemoUser", "IvyQuill", "Currently a bus novel and three READMEs. Classic.", True, 7),
        ("Admin", "DemoUser", "You are a mod on t/AskThreaddit — try manage mods from the thread menu.", False, 10),
        ("TheoLens", "DemoUser", "The bunny video is in Movies if you want a player demo.", True, 15),
        ("LunaPark", "DemoUser", "Inbox check: this one should still look unread.", False, 0.4),
        ("RemyCloud", "DemoUser", "Travel thread needs more bakery photos. That is science.", True, 26),
        ("NiaForge", "DemoUser", "Form check post is up. Be kind in the comments.", True, 18),
    ]
    for sender, receiver, content, seen, hours in messages:
        cur.execute(
            """
            INSERT INTO messages (sender_id, receiver_id, content, seen, seen_at, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                user_ids[sender],
                user_ids[receiver],
                content,
                seen,
                hours_ago(hours / 2) if seen else None,
                hours_ago(hours),
            ),
        )

    conn.commit()
    cur.execute("SELECT count(*) FROM users")
    n_users = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM subthreads")
    n_threads = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM posts")
    n_posts = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM comments")
    n_comments = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reactions")
    n_reactions = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM messages")
    n_messages = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(
        f"Seeded {n_users} users, {n_threads} threads, {n_posts} posts, "
        f"{n_comments} comments, {n_reactions} votes, {n_messages} messages."
    )
    print("Login as DemoUser / demo@threaddit.local / password123")
    print("Admin: Admin / admin@threaddit.local / password123")
    try:
        from threaddit import app
        from threaddit.search.indexer import reindex_all

        with app.app_context():
            indexed = reindex_all()
        print(f"Indexed {indexed} documents into Elasticsearch.")
    except Exception as exc:
        print(f"Search index skipped: {exc}")
        print("Start Elasticsearch and run: python reindex_search.py")


if __name__ == "__main__":
    main()
