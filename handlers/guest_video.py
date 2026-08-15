"""
Guest Mode media delivery.

Telegram 9.6+ sends messages in chats where the bot is not a member as the
dedicated `guest_message` update. This module therefore registers on
`router.guest_message`, not `router.message`.

Supported rich layouts:
- multiple photos -> Slideshow
- video -> Details / Toggle block
- mixed photo/video posts -> Slideshow + Details blocks

The normal message handlers keep their existing behaviour; this module only
handles guest_message updates.
"""

from __future__ import annotations

import datetime
import os
import json
import hashlib
from pathlib import Path
from typing import Any, Optional

from aiogram import Router, types

from app_context import bot, db, send_analytics
from config import CHANNEL_ID, MAX_FILE_SIZE, OUTPUT_DIR
from handlers.utils import get_message_text, remove_file
from services.links.detection import extract_supported_link
from services.logger import logger as logging, summarize_url_for_log

logging = logging.bind(service="guest_video")

router = Router(name=__name__)


async def _download_media_item(
    *,
    service: Any,
    media_url: str,
    filename: str,
    request_id: str,
    user_id: int | None,
    chat_id: int | None,
) -> Optional[str]:
    metrics = await service.download_media(
        media_url,
        filename,
        user_id=user_id,
        chat_id=chat_id,
        request_id=request_id,
    )
    return metrics.path if metrics else None


async def _resolve_youtube(url: str, *, user_id: int | None, chat_id: int | None) -> tuple[list[dict[str, Any]], str]:
    from handlers.youtube import (
        YTDLP_FORMAT_720,
        download_stream,
        download_with_ytdlp_metrics,
        get_video_stream,
        get_youtube_video,
    )
    import asyncio

    yt = await asyncio.to_thread(get_youtube_video, url)
    if not yt:
        return [], ""

    video = await asyncio.to_thread(get_video_stream, yt)
    name = f"{yt['id']}_guest_youtube.mp4"
    if video:
        metrics = await download_stream(video, name, "youtube_guest")
    else:
        metrics = await download_with_ytdlp_metrics(
            yt["webpage_url"], name, YTDLP_FORMAT_720, "youtube_guest_ytdlp"
        )

    if not metrics:
        return [], ""

    description = str(yt.get("title") or "")
    return [{"kind": "video", "path": metrics.path, "file_id": None, "url": video if isinstance(video, str) else None, "cached": False}], description


async def _resolve_tiktok(url: str, *, user_id: int | None, chat_id: int | None) -> tuple[list[dict[str, Any]], str]:
    from handlers.tiktok import (
        build_tiktok_video_url,
        fetch_tiktok_data_with_retry,
        strip_tiktok_tracking,
        tiktok_service,
        video_info,
    )

    clean_url = strip_tiktok_tracking(url)
    data = await fetch_tiktok_data_with_retry(clean_url)
    info = await video_info(data)
    if not info:
        return [], ""

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    name = f"{info.id}_{timestamp}_guest_tiktok.mp4"
    metrics = await tiktok_service.download_video(
        build_tiktok_video_url(info),
        name,
        download_data=data,
        request_id=f"tiktok_guest:{info.id}",
    )
    if not metrics:
        return [], ""

    return [{"kind": "video", "path": metrics.path, "file_id": None, "url": build_tiktok_video_url(info), "cached": False}], info.description or ""


async def _resolve_instagram(url: str, *, user_id: int | None, chat_id: int | None) -> tuple[list[dict[str, Any]], str]:
    from handlers.instagram import inst_service
    from services.platforms.instagram_media import strip_instagram_url

    clean_url = strip_instagram_url(url)
    post = await inst_service.fetch_data(clean_url)
    if not post or not post.media_list:
        return [], ""

    entries: list[dict[str, Any]] = []
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    for index, media in enumerate(post.media_list[:10]):
        extension = "mp4" if media.type == "video" else "jpg"
        path = await _download_media_item(
            service=inst_service,
            media_url=media.url,
            filename=f"{post.id}_{timestamp}_guest_instagram_{index}.{extension}",
            request_id=f"instagram_guest:{post.id}:{index}",
            user_id=user_id,
            chat_id=chat_id,
        )
        if path:
            entries.append(
                {
                    "kind": media.type,
                    "path": path,
                    "file_id": None,
                    "url": media.url,
                    "cached": False,
                }
            )

    return entries, post.description or ""


async def _resolve_pinterest(url: str, *, user_id: int | None, chat_id: int | None) -> tuple[list[dict[str, Any]], str]:
    from handlers.pinterest import pinterest_service
    from services.platforms.pinterest_media import strip_pinterest_url

    clean_url = strip_pinterest_url(url)
    post = await pinterest_service.fetch_post(clean_url)
    if not post or not post.media_list:
        return [], ""

    entries: list[dict[str, Any]] = []
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    for index, media in enumerate(post.media_list[:10]):
        extension = "mp4" if media.type == "video" else "jpg"
        path = await _download_media_item(
            service=pinterest_service,
            media_url=media.url,
            filename=f"{post.id}_{timestamp}_guest_pinterest_{index}.{extension}",
            request_id=f"pinterest_guest:{post.id}:{index}",
            user_id=user_id,
            chat_id=chat_id,
        )
        if path:
            entries.append(
                {
                    "kind": media.type,
                    "path": path,
                    "file_id": None,
                    "url": media.url,
                    "cached": False,
                }
            )

    return entries, post.description or ""


async def _resolve_threads(url: str, *, user_id: int | None, chat_id: int | None) -> tuple[list[dict[str, Any]], str]:
    from handlers.threads import threads_service
    from services.platforms.threads_media import strip_threads_url

    clean_url = strip_threads_url(url)
    post = await threads_service.fetch_post(clean_url)
    if not post or not post.media_list:
        return [], ""

    entries: list[dict[str, Any]] = []
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    for index, media in enumerate(post.media_list[:10]):
        extension = "mp4" if media.type == "video" else "jpg"
        path = await _download_media_item(
            service=threads_service,
            media_url=media.url,
            filename=f"{post.id}_{timestamp}_guest_threads_{index}.{extension}",
            request_id=f"threads_guest:{post.id}:{index}",
            user_id=user_id,
            chat_id=chat_id,
        )
        if path:
            entries.append(
                {
                    "kind": media.type,
                    "path": path,
                    "file_id": None,
                    "url": media.url,
                    "cached": False,
                }
            )

    return entries, post.description or ""


async def _resolve_twitter(url: str, *, user_id: int | None, chat_id: int | None) -> tuple[list[dict[str, Any]], str]:
    from handlers.twitter import _get_tweet_context, _collect_media_entries

    context = await _get_tweet_context(url)
    if not context:
        return [], ""

    tweet_id, tweet_media = context
    tweet_dir_name = f"{tweet_id}_guest"
    entries = await _collect_media_entries(
        tweet_id,
        tweet_media,
        user_id=user_id,
        chat_id=chat_id,
        request_id=f"twitter_guest:{tweet_id}",
        download_dir_name=tweet_dir_name,
    )
    return entries, str(tweet_media.get("text") or "")


_RESOLVERS = {
    "youtube": _resolve_youtube,
    "tiktok": _resolve_tiktok,
    "instagram": _resolve_instagram,
    "pinterest": _resolve_pinterest,
    "threads": _resolve_threads,
    "twitter": _resolve_twitter,
}


async def _cache_file_path() -> Path:
    path = Path(OUTPUT_DIR) / "guest_file_cache.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _guest_cache_key(service: str, url: str) -> str:
    normalized = " ".join(str(url).strip().split())
    return hashlib.sha256(f"{service}|{normalized}".encode("utf-8")).hexdigest()


def _load_guest_file_cache() -> dict[str, Any]:
    path = Path(OUTPUT_DIR) / "guest_file_cache.json"
    try:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    except Exception:
        logging.debug("Failed to read guest file cache", exc_info=True)
    return {}


def _save_guest_file_cache(cache: dict[str, Any]) -> None:
    path = Path(OUTPUT_DIR) / "guest_file_cache.json"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(path)
    except Exception:
        logging.debug("Failed to save guest file cache", exc_info=True)


def _cached_entries(service: str, url: str) -> list[dict[str, Any]]:
    item = _load_guest_file_cache().get(_guest_cache_key(service, url))
    if not isinstance(item, dict):
        return []
    entries = item.get("entries")
    if not isinstance(entries, list):
        return []
    result = []
    for entry in entries:
        if isinstance(entry, dict) and entry.get("file_id"):
            result.append({
                "kind": entry.get("kind", "video"),
                "path": None,
                "file_id": str(entry["file_id"]),
                "url": None,
                "cached": True,
            })
    return result


def _remember_guest_entries(service: str, url: str, entries: list[dict[str, Any]]) -> None:
    cache = _load_guest_file_cache()
    cache[_guest_cache_key(service, url)] = {
        "service": service,
        "source": str(url),
        "entries": [
            {"kind": e.get("kind"), "file_id": str(e["file_id"])}
            for e in entries
            if isinstance(e, dict) and e.get("file_id")
        ],
    }
    _save_guest_file_cache(cache)


async def _upload_guest_entries(message: types.Message, entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not CHANNEL_ID:
        raise RuntimeError("CHANNEL_ID is required for Guest media cache")

    uploaded: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("file_id"):
            uploaded.append({**entry, "file_id": str(entry["file_id"]), "path": None, "url": None})
            continue

        path = entry.get("path")
        if not path:
            raise RuntimeError("Guest media entry has no local path")

        kind = str(entry.get("kind", "")).lower()
        if kind == "video":
            sent = await message.bot.send_video(
                chat_id=CHANNEL_ID,
                video=types.FSInputFile(str(path)),
                disable_notification=True,
            )
            file_id = sent.video.file_id if sent.video else None
        elif kind == "photo":
            sent = await message.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=types.FSInputFile(str(path)),
                disable_notification=True,
            )
            file_id = sent.photo[-1].file_id if sent.photo else None
        else:
            continue

        if not file_id:
            raise RuntimeError(f"Telegram did not return file_id for Guest {kind}")
        uploaded.append({**entry, "file_id": file_id, "path": None, "url": None, "cached": True})

    if not uploaded:
        raise RuntimeError("No usable Guest media entries")
    return uploaded


async def _answer_guest_error(message: types.Message, guest_query_id: str) -> None:
    """
    A guest query must be answered exactly once. If media resolution fails,
    return a small rich text message instead of leaving the guest query hanging.
    """
    from aiogram.types import InlineQueryResultArticle, InputRichMessage, InputRichMessageContent, InputRichBlockParagraph

    result = InlineQueryResultArticle(
        id=f"guest-error:{message.message_id}",
        title="Download failed",
        description="The media could not be downloaded.",
        input_message_content=InputRichMessageContent(
            rich_message=InputRichMessage(
                blocks=[
                    InputRichBlockParagraph(
                        text="⚠️ Unable to download this media right now. Please try again."
                    )
                ]
            )
        ),
    )
    await message.bot.answer_guest_query(
        guest_query_id=guest_query_id,
        result=result,
    )


async def _answer_guest_loading(message: types.Message, guest_query_id: str) -> types.SentGuestMessage:
    from aiogram.types import InlineQueryResultArticle, InputRichMessage, InputRichMessageContent, InputRichBlockParagraph

    result = InlineQueryResultArticle(
        id=f"guest-loading:{message.message_id}",
        title="Loading",
        description="Downloading media…",
        input_message_content=InputRichMessageContent(
            rich_message=InputRichMessage(
                blocks=[InputRichBlockParagraph(text="⏳ جارِ تحميل المحتوى…")]
            )
        ),
    )
    return await message.bot.answer_guest_query(guest_query_id=guest_query_id, result=result)


async def _edit_guest_result(message: types.Message, sent: types.SentGuestMessage, entries: list[dict[str, Any]], description: str) -> None:
    if not sent.inline_message_id:
        raise RuntimeError("Guest response did not return inline_message_id")

    # Bot API 10.0 allows editMessageMedia to replace a text/rich message with media.
    # Inline edits cannot upload a new file, so entries MUST already contain file_id.
    if len(entries) != 1:
        raise RuntimeError("Guest loading edit currently supports one media item")

    entry = entries[0]
    file_id = entry.get("file_id")
    if not file_id:
        raise RuntimeError("Guest final media requires file_id")

    kind = str(entry.get("kind", "")).lower()
    if kind == "video":
        media = types.InputMediaVideo(media=str(file_id), caption=description[:1024] if description else None)
    elif kind == "photo":
        media = types.InputMediaPhoto(media=str(file_id), caption=description[:1024] if description else None)
    else:
        raise RuntimeError(f"Unsupported Guest media kind: {kind}")

    await message.bot.edit_message_media(
        inline_message_id=sent.inline_message_id,
        media=media,
    )


@router.guest_message()
async def handle_guest_link_message(message: types.Message) -> None:
    """Handle Telegram's dedicated guest_message update."""
    guest_query_id = getattr(message, "guest_query_id", None)
    if not guest_query_id:
        logging.warning(
            "Guest message received without guest_query_id: message_id=%s",
            getattr(message, "message_id", None),
        )
        return

    text = get_message_text(message)
    detected = extract_supported_link(text)
    if not detected:
        logging.debug(
            "Guest message has no supported link: message_id=%s text=%s",
            getattr(message, "message_id", None),
            text,
        )
        return

    service, url = detected
    resolver = _RESOLVERS.get(service)
    if resolver is None:
        await _answer_guest_error(message, str(guest_query_id))
        return

    user_id = getattr(getattr(message, "from_user", None), "id", None)
    chat_id = getattr(getattr(message, "chat", None), "id", None)

    logging.info(
        "Guest link accepted: service=%s url=%s guest_query_id=%s",
        service,
        summarize_url_for_log(url),
        guest_query_id,
    )

    try:
        await send_analytics(
            user_id=user_id or 0,
            chat_type=message.chat.type if message.chat else "unknown",
            action_name=f"guest_{service}",
        )

        # Answer the Guest query immediately. This prevents the query from
        # expiring while the media is being resolved/downloaded.
        loading_message = await _answer_guest_loading(message, str(guest_query_id))

        entries: list[dict[str, Any]] = _cached_entries(service, url)
        description = ""
        if entries:
            logging.info("Guest cache hit: service=%s entries=%s", service, len(entries))
        else:
            entries, description = await resolver(
                url,
                user_id=user_id,
                chat_id=chat_id,
            )

        if not entries:
            logging.warning(
                "Guest media resolve failed: service=%s url=%s guest_query_id=%s",
                service,
                summarize_url_for_log(url),
                guest_query_id,
            )
            if loading_message.inline_message_id:
                await message.bot.edit_message_text(
                    inline_message_id=loading_message.inline_message_id,
                    text="⚠️ تعذر تحميل المحتوى حالياً. حاول مرة أخرى.",
                )
            return

        if not entries:
            logging.warning(
                "Guest media resolve failed: service=%s url=%s guest_query_id=%s",
                service,
                summarize_url_for_log(url),
                guest_query_id,
            )
            if loading_message.inline_message_id:
                await message.bot.edit_message_text(
                    inline_message_id=loading_message.inline_message_id,
                    text="⚠️ تعذر تحميل المحتوى حالياً. حاول مرة أخرى.",
                )
            return

        if not all(entry.get("file_id") for entry in entries):
            entries = await _upload_guest_entries(message, entries)
            _remember_guest_entries(service, url, entries)

        # The loading Guest message is edited into the already-uploaded media.
        # No URL is ever used in the final Guest message.
        await _edit_guest_result(message, loading_message, entries, description)

        logging.info(
            "Guest rich media sent: service=%s guest_query_id=%s entries=%s",
            service,
            guest_query_id,
            len(entries),
        )
    except Exception as exc:
        logging.exception(
            "Guest media handling failed: service=%s url=%s guest_query_id=%s error=%s",
            service,
            summarize_url_for_log(url),
            guest_query_id,
            exc,
        )
        try:
            loading_message = locals().get("loading_message")
            if loading_message and getattr(loading_message, "inline_message_id", None):
                await message.bot.edit_message_text(
                    inline_message_id=loading_message.inline_message_id,
                    text="⚠️ تعذر تحميل المحتوى حالياً. حاول مرة أخرى.",
                )
            else:
                await _answer_guest_error(message, str(guest_query_id))
        except Exception:
            logging.exception(
                "Failed to update Guest error message: guest_query_id=%s",
                guest_query_id,
            )
    finally:
        # Guest replies are already uploaded by answerGuestQuery. Remove only
        # local temporary files; Telegram file_ids are never touched.
        for entry in locals().get("entries", []) or []:
            path = entry.get("path") if isinstance(entry, dict) else None
            if path:
                try:
                    await remove_file(str(path))
                except Exception:
                    logging.debug("Failed to clean guest media: path=%s", path)
