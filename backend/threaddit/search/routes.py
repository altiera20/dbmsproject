from flask import Blueprint, jsonify, request
from flask_login import current_user
from threaddit.posts.models import PostInfo
from threaddit.search.client import es_available
from threaddit.search.query import search_content
from threaddit.subthreads.models import SubthreadInfo
from threaddit.users.models import User

search = Blueprint("search", __name__, url_prefix="/api")


def _hydrate_results(results):
    post_ids = [item["id"] for item in results if item["type"] == "post"]
    posts_by_id = {}
    if post_ids:
        cur_user = current_user.id if current_user.is_authenticated else None
        for info in PostInfo.query.filter(PostInfo.post_id.in_(post_ids)).all():
            posts_by_id[info.post_id] = info.as_dict(cur_user)

    hydrated = []
    for item in results:
        source = item.get("source") or {}
        entry = {
            "type": item["type"],
            "id": item["id"],
            "score": item["score"],
            "highlight": item["highlight"],
        }
        if item["type"] == "post":
            entry["post"] = posts_by_id.get(item["id"])
            if not entry["post"]:
                continue
        elif item["type"] == "comment":
            entry["comment"] = {
                "id": source.get("id"),
                "content": source.get("content"),
                "user_name": source.get("user_name"),
                "user_avatar": source.get("user_avatar"),
                "post_id": source.get("post_id"),
                "post_title": source.get("post_title"),
                "created_at": source.get("created_at"),
                "comment_karma": source.get("comment_karma") or 0,
            }
        elif item["type"] == "thread":
            entry["thread"] = {
                "id": source.get("id"),
                "name": source.get("name"),
                "description": source.get("description"),
                "logo": source.get("logo"),
                "subscriberCount": source.get("subscriber_count") or 0,
                "PostsCount": source.get("posts_count") or 0,
                "CommentsCount": source.get("comments_count") or 0,
            }
        elif item["type"] == "user":
            entry["user"] = {
                "username": source.get("username"),
                "avatar": source.get("avatar"),
                "bio": source.get("bio"),
                "karma": {"user_karma": source.get("user_karma") or 0},
            }
        else:
            continue
        hydrated.append(entry)
    return hydrated


@search.route("/search", methods=["GET"])
def search_all():
    query = request.args.get("q", default="", type=str).strip()
    doc_type = request.args.get("type", default=None, type=str)
    if doc_type in ("", "all"):
        doc_type = None
    limit = min(request.args.get("limit", default=20, type=int), 50)
    offset = max(request.args.get("offset", default=0, type=int), 0)
    if not query:
        return jsonify({"query": query, "took": 0, "total": 0, "counts": {}, "results": []}), 200
    if not es_available():
        return jsonify({"message": "Search is temporarily unavailable"}), 503
    try:
        payload = search_content(query, doc_type=doc_type, limit=limit, offset=offset)
    except ValueError:
        return jsonify({"message": "Invalid search type"}), 400
    payload["results"] = _hydrate_results(payload["results"])
    return jsonify(payload), 200


@search.route("/search/status", methods=["GET"])
def search_status():
    return jsonify({"elasticsearch": es_available()}), 200


def search_threads_by_name(name):
    payload = search_content(name, doc_type="thread", limit=15, offset=0)
    threads = []
    for item in payload["results"]:
        source = item.get("source") or {}
        threads.append(
            {
                "id": source.get("id"),
                "name": source.get("name"),
                "logo": source.get("logo"),
                "subscriberCount": source.get("subscriber_count") or 0,
                "PostsCount": source.get("posts_count") or 0,
                "CommentsCount": source.get("comments_count") or 0,
            }
        )
    return threads


def search_users_by_name(name):
    payload = search_content(name, doc_type="user", limit=20, offset=0)
    users = []
    seen = set()
    for item in payload["results"]:
        username = (item.get("source") or {}).get("username")
        if not username or username in seen:
            continue
        seen.add(username)
        user = User.query.filter_by(username=username).first()
        if user:
            users.append(user.as_dict())
    return users


def fallback_thread_search(name):
    like = f"%{name}%"
    return [subthread.as_dict() for subthread in SubthreadInfo.query.filter(SubthreadInfo.name.ilike(like)).all()]


def fallback_user_search(name):
    return [user.as_dict() for user in User.query.filter(User.username.ilike(f"%{name}%")).all()]
