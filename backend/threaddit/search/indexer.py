import logging
from datetime import datetime

from elasticsearch.helpers import bulk
from threaddit.search.client import INDEX_NAME, document_id, ensure_index, es_available, get_es

logger = logging.getLogger(__name__)


def _iso(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _index_doc(doc_type, entity_id, body):
    if not ensure_index():
        return
    try:
        get_es().index(
            index=INDEX_NAME,
            id=document_id(doc_type, entity_id),
            document={"doc_type": doc_type, "id": entity_id, **body},
            refresh=False,
        )
    except Exception as exc:
        logger.warning("Failed to index %s %s: %s", doc_type, entity_id, exc)


def delete_document(doc_type, entity_id):
    if not es_available():
        return
    try:
        get_es().delete(index=INDEX_NAME, id=document_id(doc_type, entity_id), ignore_status=[404])
    except Exception as exc:
        logger.warning("Failed to delete %s %s from search: %s", doc_type, entity_id, exc)


def index_post(post_id):
    from threaddit.posts.models import PostInfo

    info = PostInfo.query.filter_by(post_id=post_id).first()
    if not info:
        return
    _index_doc(
        "post",
        info.post_id,
        {
            "title": info.title or "",
            "content": info.content or "",
            "thread_id": info.thread_id,
            "thread_name": info.thread_name,
            "thread_logo": info.thread_logo,
            "user_id": info.user_id,
            "user_name": info.user_name,
            "user_avatar": info.user_avatar,
            "media": info.media,
            "created_at": _iso(info.created_at),
            "post_karma": info.post_karma or 0,
            "comments_count": info.comments_count or 0,
        },
    )


def index_comment(comment_id):
    from threaddit.comments.models import CommentInfo
    from threaddit.posts.models import Posts

    info = CommentInfo.query.filter_by(comment_id=comment_id).first()
    if not info:
        return
    post = Posts.query.filter_by(id=info.post_id).first()
    _index_doc(
        "comment",
        info.comment_id,
        {
            "content": info.content or "",
            "user_name": info.user_name,
            "user_avatar": info.user_avatar,
            "post_id": info.post_id,
            "post_title": post.title if post else "",
            "created_at": _iso(info.created_at),
            "comment_karma": info.comment_karma or 0,
        },
    )


def index_thread(thread_id):
    from threaddit.subthreads.models import Subthread, SubthreadInfo

    thread = Subthread.query.filter_by(id=thread_id).first()
    info = SubthreadInfo.query.filter_by(id=thread_id).first()
    if not thread:
        return
    _index_doc(
        "thread",
        thread.id,
        {
            "name": thread.name or "",
            "description": thread.description or "",
            "logo": thread.logo or (info.logo if info else None),
            "created_at": _iso(thread.created_at),
            "subscriber_count": (info.members_count if info else None) or 0,
            "posts_count": (info.posts_count if info else None) or 0,
            "comments_count": (info.comments_count if info else None) or 0,
        },
    )


def index_user(user_id):
    from threaddit.users.models import User

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return
    karma = user.user_karma[0].user_karma if user.user_karma else 0
    _index_doc(
        "user",
        user.id,
        {
            "username": user.username or "",
            "bio": user.bio or "",
            "avatar": user.avatar,
            "created_at": _iso(user.registration_date),
            "user_karma": karma or 0,
        },
    )


def reindex_all():
    from threaddit.comments.models import Comments
    from threaddit.posts.models import Posts
    from threaddit.subthreads.models import Subthread
    from threaddit.users.models import User

    if not ensure_index():
        raise RuntimeError("Elasticsearch is not available")

    client = get_es()
    if client.indices.exists(index=INDEX_NAME):
        client.indices.delete(index=INDEX_NAME)
    ensure_index()

    actions = []

    def add_action(doc_type, entity_id, body):
        actions.append(
            {
                "_op_type": "index",
                "_index": INDEX_NAME,
                "_id": document_id(doc_type, entity_id),
                "_source": {"doc_type": doc_type, "id": entity_id, **body},
            }
        )

    for post in Posts.query.all():
        info = post.post_info[0] if post.post_info else None
        if not info:
            continue
        add_action(
            "post",
            info.post_id,
            {
                "title": info.title or "",
                "content": info.content or "",
                "thread_id": info.thread_id,
                "thread_name": info.thread_name,
                "thread_logo": info.thread_logo,
                "user_id": info.user_id,
                "user_name": info.user_name,
                "user_avatar": info.user_avatar,
                "media": info.media,
                "created_at": _iso(info.created_at),
                "post_karma": info.post_karma or 0,
                "comments_count": info.comments_count or 0,
            },
        )

    for comment in Comments.query.all():
        info = comment.comment_info[0] if comment.comment_info else None
        if not info:
            continue
        add_action(
            "comment",
            info.comment_id,
            {
                "content": info.content or "",
                "user_name": info.user_name,
                "user_avatar": info.user_avatar,
                "post_id": info.post_id,
                "post_title": comment.post.title if comment.post else "",
                "created_at": _iso(info.created_at),
                "comment_karma": info.comment_karma or 0,
            },
        )

    for thread in Subthread.query.all():
        info = thread.subthread_info[0] if thread.subthread_info else None
        add_action(
            "thread",
            thread.id,
            {
                "name": thread.name or "",
                "description": thread.description or "",
                "logo": thread.logo or (info.logo if info else None),
                "created_at": _iso(thread.created_at),
                "subscriber_count": (info.members_count if info else None) or 0,
                "posts_count": (info.posts_count if info else None) or 0,
                "comments_count": (info.comments_count if info else None) or 0,
            },
        )

    for user in User.query.all():
        karma = user.user_karma[0].user_karma if user.user_karma else 0
        add_action(
            "user",
            user.id,
            {
                "username": user.username or "",
                "bio": user.bio or "",
                "avatar": user.avatar,
                "created_at": _iso(user.registration_date),
                "user_karma": karma or 0,
            },
        )

    if actions:
        bulk(client, actions, refresh=True)
    else:
        client.indices.refresh(index=INDEX_NAME)
    return len(actions)
