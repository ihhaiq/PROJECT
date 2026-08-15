"""
Telegram Rich Message helpers.

Normal delivery:
- multiple photos -> one Rich Message with a Slideshow block
- video -> one Rich Message with a Details (toggle) block containing the video

Guest delivery:
- the same Rich Message is embedded in InputRichMessageContent and returned
  through answerGuestQuery().

The helpers accept either a local filesystem path, a Telegram file_id, or a
remote URL. This is important because normal requests may be freshly
downloaded while cached requests only have Telegram file_ids.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from aiogram import Bot, types
from aiogram.types import (
    FSInputFile,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputMediaPhoto,
    InputMediaVideo,
    InputRichBlockDetails,
    InputRichBlockPhoto,
    InputRichBlockSlideshow,
    InputRichBlockVideo,
    InputRichMessage,
    InputRichMessageContent,
    RichBlockCaption,
)


def _media_ref(value: Any) -> str | FSInputFile:
    """Turn a local path into FSInputFile; keep file_ids/URLs as strings."""
    if value is None:
        raise ValueError("Rich media source is empty")

    if isinstance(value, FSInputFile):
        return value

    value = str(value)
    try:
        if Path(value).is_file():
            return FSInputFile(value)
    except (OSError, ValueError):
        # Telegram file_ids/URLs are not local filesystem paths.
        pass

    return value


def build_video_details_rich_message(
    *,
    video_path: str,
    summary_text: str = "▶️ Tap to expand video",
    caption_text: Optional[str] = None,
    is_open: bool = False,
) -> InputRichMessage:
    """Build a Details/Toggle block containing one video."""
    video_block = InputRichBlockVideo(
        video=InputMediaVideo(media=_media_ref(video_path)),
        caption=RichBlockCaption(text=caption_text) if caption_text else None,
    )

    details_block = InputRichBlockDetails(
        summary=summary_text,
        blocks=[video_block],
        is_open=is_open,
    )
    return InputRichMessage(blocks=[details_block])


def build_photo_slideshow_rich_message(
    *,
    photo_paths: list[str],
    caption_text: Optional[str] = None,
) -> InputRichMessage:
    """Build a Rich Message whose main block is a Slideshow."""
    sources = [item for item in photo_paths if item]
    if not sources:
        raise ValueError("photo_paths must contain at least one photo")

    photo_blocks = [
        InputRichBlockPhoto(
            photo=InputMediaPhoto(media=_media_ref(path)),
        )
        for path in sources[:10]
    ]

    slideshow_block = InputRichBlockSlideshow(
        blocks=photo_blocks,
        caption=RichBlockCaption(text=caption_text) if caption_text else None,
    )
    return InputRichMessage(blocks=[slideshow_block])


def build_media_rich_message(
    *,
    entries: list[dict[str, Any]],
    caption_text: Optional[str] = None,
) -> InputRichMessage | None:
    """
    Build a rich message from delivery entries.

    Supported layouts:
      - 2+ photos -> Slideshow
      - one photo -> Photo block
      - every video -> Details/Toggle block

    Mixed posts are supported too: photos are grouped into one slideshow and
    videos are rendered as individual Details blocks.
    """
    if not entries:
        return None

    photo_sources = [
        entry.get("path") or entry.get("file_id") or entry.get("url")
        for entry in entries
        if str(entry.get("kind", "")).lower() == "photo"
    ]
    video_sources = [
        entry.get("path") or entry.get("file_id") or entry.get("url")
        for entry in entries
        if str(entry.get("kind", "")).lower() == "video"
    ]

    photo_sources = [str(source) for source in photo_sources if source]
    video_sources = [str(source) for source in video_sources if source]

    blocks = []

    if len(photo_sources) > 1:
        slideshow = build_photo_slideshow_rich_message(
            photo_paths=photo_sources,
            caption_text=caption_text if not video_sources else None,
        )
        blocks.extend(slideshow.blocks or [])
    elif len(photo_sources) == 1 and not video_sources:
        photo_block = InputRichBlockPhoto(
            photo=InputMediaPhoto(media=_media_ref(photo_sources[0])),
            caption=RichBlockCaption(text=caption_text) if caption_text else None,
        )
        blocks.append(photo_block)

    for index, video_source in enumerate(video_sources):
        details = build_video_details_rich_message(
            video_path=video_source,
            summary_text="▶️ Tap to expand video" if index == 0 else "▶️ Video",
            caption_text=caption_text if len(video_sources) == 1 else None,
        )
        blocks.extend(details.blocks or [])

    return InputRichMessage(blocks=blocks) if blocks else None


async def send_video_details_rich_message(
    bot: Bot,
    chat_id: int | str,
    *,
    video_path: str,
    summary_text: str = "▶️ Tap to expand video",
    caption_text: Optional[str] = None,
    is_open: bool = False,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> types.Message:
    rich_message = build_video_details_rich_message(
        video_path=video_path,
        summary_text=summary_text,
        caption_text=caption_text,
        is_open=is_open,
    )
    return await bot.send_rich_message(
        chat_id=chat_id,
        rich_message=rich_message,
        reply_markup=reply_markup,
    )


async def send_photo_slideshow_rich_message(
    bot: Bot,
    chat_id: int | str,
    *,
    photo_paths: list[str],
    caption_text: Optional[str] = None,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> types.Message:
    rich_message = build_photo_slideshow_rich_message(
        photo_paths=photo_paths,
        caption_text=caption_text,
    )
    return await bot.send_rich_message(
        chat_id=chat_id,
        rich_message=rich_message,
        reply_markup=reply_markup,
    )


async def answer_guest_query_with_rich_message(
    bot: Bot,
    *,
    guest_query_id: str,
    result_id: str,
    rich_message: InputRichMessage,
    article_title: str = "Media",
    article_description: Optional[str] = None,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> types.SentGuestMessage:
    """Answer one guest_message update with a Rich Message."""
    result = InlineQueryResultArticle(
        id=result_id,
        title=article_title,
        description=article_description,
        input_message_content=InputRichMessageContent(rich_message=rich_message),
        reply_markup=reply_markup,
    )
    return await bot.answer_guest_query(
        guest_query_id=guest_query_id,
        result=result,
    )


async def answer_guest_query_with_video(
    bot: Bot,
    *,
    guest_query_id: str,
    result_id: str,
    video_path: str,
    summary_text: str = "▶️ Tap to expand video",
    caption_text: Optional[str] = None,
    is_open: bool = False,
    article_title: str = "Video",
    article_description: Optional[str] = None,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> types.SentGuestMessage:
    rich_message = build_video_details_rich_message(
        video_path=video_path,
        summary_text=summary_text,
        caption_text=caption_text,
        is_open=is_open,
    )
    return await answer_guest_query_with_rich_message(
        bot,
        guest_query_id=guest_query_id,
        result_id=result_id,
        rich_message=rich_message,
        article_title=article_title,
        article_description=article_description,
        reply_markup=reply_markup,
    )


async def answer_guest_query_with_photo_slideshow(
    bot: Bot,
    *,
    guest_query_id: str,
    result_id: str,
    photo_paths: list[str],
    caption_text: Optional[str] = None,
    article_title: str = "Photo Slideshow",
    article_description: Optional[str] = None,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> types.SentGuestMessage:
    rich_message = build_photo_slideshow_rich_message(
        photo_paths=photo_paths,
        caption_text=caption_text,
    )
    return await answer_guest_query_with_rich_message(
        bot,
        guest_query_id=guest_query_id,
        result_id=result_id,
        rich_message=rich_message,
        article_title=article_title,
        article_description=article_description,
        reply_markup=reply_markup,
    )