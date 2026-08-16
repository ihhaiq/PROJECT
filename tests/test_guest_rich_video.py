from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiogram.types import (
    InputRichBlockAudio,
    InputRichBlockDetails,
    InputRichBlockPhoto,
    InputRichBlockSlideshow,
)

from handlers.guest_rich_video import build_media_rich_message
from handlers.guest_video import _edit_guest_result


def test_build_media_rich_message_uses_details_for_cached_video():
    rich_message = build_media_rich_message(
        entries=[{"kind": "video", "file_id": "cached-video-id"}],
        caption_text="caption",
    )

    assert rich_message is not None
    assert len(rich_message.blocks) == 1
    assert isinstance(rich_message.blocks[0], InputRichBlockDetails)
    assert rich_message.blocks[0].blocks[0].video.media == "cached-video-id"


def test_build_media_rich_message_uses_slideshow_for_photos():
    rich_message = build_media_rich_message(
        entries=[
            {"kind": "photo", "file_id": "photo-1"},
            {"kind": "photo", "file_id": "photo-2"},
        ],
        caption_text="album",
    )

    assert rich_message is not None
    assert len(rich_message.blocks) == 1
    slideshow = rich_message.blocks[0]
    assert isinstance(slideshow, InputRichBlockSlideshow)
    assert [block.photo.media for block in slideshow.blocks] == ["photo-1", "photo-2"]


def test_build_media_rich_message_preserves_mixed_single_photo():
    rich_message = build_media_rich_message(
        entries=[
            {"kind": "photo", "file_id": "photo-1"},
            {"kind": "video", "file_id": "video-1"},
        ]
    )

    assert rich_message is not None
    assert isinstance(rich_message.blocks[0], InputRichBlockPhoto)
    assert isinstance(rich_message.blocks[1], InputRichBlockDetails)


def test_build_media_rich_message_splits_large_slideshow_without_data_loss():
    rich_message = build_media_rich_message(
        entries=[{"kind": "photo", "file_id": f"photo-{index}"} for index in range(13)]
    )

    assert rich_message is not None
    assert len(rich_message.blocks) == 2
    assert all(isinstance(block, InputRichBlockSlideshow) for block in rich_message.blocks)
    assert [len(block.blocks) for block in rich_message.blocks] == [10, 3]


def test_build_media_rich_message_keeps_slideshow_and_audio_in_one_message():
    rich_message = build_media_rich_message(
        entries=[
            {"kind": "photo", "file_id": "photo-1"},
            {"kind": "photo", "file_id": "photo-2"},
            {
                "kind": "audio",
                "file_id": "audio-1",
                "title": "Original sound",
                "performer": "@creator",
                "duration": 15,
            },
        ],
        caption_text="album",
    )

    assert rich_message is not None
    assert isinstance(rich_message.blocks[0], InputRichBlockSlideshow)
    assert isinstance(rich_message.blocks[1], InputRichBlockAudio)
    assert rich_message.blocks[1].audio.media == "audio-1"
    assert rich_message.blocks[1].audio.title == "Original sound"
    assert rich_message.blocks[1].audio.performer == "@creator"


@pytest.mark.asyncio
async def test_guest_loading_result_is_edited_to_rich_details():
    bot = SimpleNamespace(edit_message_text=AsyncMock())
    message = SimpleNamespace(bot=bot)
    sent = SimpleNamespace(inline_message_id="inline-guest-id")

    await _edit_guest_result(
        message,
        sent,
        [{"kind": "video", "file_id": "cached-video-id"}],
        "caption",
    )

    bot.edit_message_text.assert_awaited_once()
    kwargs = bot.edit_message_text.await_args.kwargs
    assert kwargs["inline_message_id"] == "inline-guest-id"
    assert "rich_message" in kwargs
    assert isinstance(kwargs["rich_message"].blocks[0], InputRichBlockDetails)
