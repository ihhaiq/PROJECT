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
from handlers.guest_video import _edit_guest_result, _resolve_tiktok, _upload_guest_entries


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


@pytest.mark.asyncio
async def test_guest_tiktok_photo_post_keeps_images_and_original_audio(monkeypatch):
    from handlers import tiktok as tiktok_handler

    info = SimpleNamespace(
        id="123",
        description="Photo post",
        music_play_url="https://example.com/sound.mp3",
        author="creator",
        duration_seconds=12,
    )
    downloader = SimpleNamespace(
        download=AsyncMock(
            side_effect=[
                SimpleNamespace(path="/tmp/photo-1.jpg"),
                SimpleNamespace(path="/tmp/photo-2.jpg"),
            ]
        )
    )
    service = SimpleNamespace(
        _downloader=downloader,
        _build_direct_download_headers=lambda *_args: {
            "User-Agent": "test-agent",
            "Referer": "https://www.tiktok.com/",
        },
        download_audio=AsyncMock(
            return_value=SimpleNamespace(path="/tmp/tiktok-audio.mp3", size=1024)
        ),
        download_video=AsyncMock(),
    )

    monkeypatch.setattr(
        tiktok_handler,
        "strip_tiktok_tracking",
        lambda url: url,
    )
    monkeypatch.setattr(
        tiktok_handler,
        "fetch_tiktok_data_with_retry",
        AsyncMock(
            return_value={
                "data": {
                    "images": [
                        "https://example.com/photo-1.jpg",
                        "https://example.com/photo-2.jpg",
                    ]
                }
            }
        ),
    )
    monkeypatch.setattr(tiktok_handler, "video_info", AsyncMock(return_value=info))
    monkeypatch.setattr(
        tiktok_handler,
        "build_tiktok_video_url",
        lambda _info: "https://www.tiktok.com/@creator/video/123",
    )
    monkeypatch.setattr(tiktok_handler, "tiktok_service", service)

    entries, description = await _resolve_tiktok(
        "https://www.tiktok.com/@creator/video/123",
        user_id=1,
        chat_id=-100,
    )

    assert description == "Photo post"
    assert [entry["kind"] for entry in entries] == ["photo", "photo", "audio"]
    assert entries[0]["path"] == "/tmp/photo-1.jpg"
    assert entries[0]["url"] is None
    assert entries[-1]["path"] == "/tmp/tiktok-audio.mp3"
    assert entries[-1]["performer"] == "@creator"
    assert downloader.download.await_count == 2
    assert downloader.download.await_args_list[0].kwargs["headers"]["Referer"] == (
        "https://www.tiktok.com/"
    )
    service.download_audio.assert_awaited_once()
    service.download_video.assert_not_awaited()


@pytest.mark.asyncio
async def test_upload_guest_entries_supports_remote_photos_and_audio(monkeypatch):
    monkeypatch.setattr("handlers.guest_video.CHANNEL_ID", -100123)
    bot = SimpleNamespace(
        send_photo=AsyncMock(
            return_value=SimpleNamespace(
                photo=[SimpleNamespace(file_id="photo-file-id")]
            )
        ),
        send_audio=AsyncMock(
            return_value=SimpleNamespace(
                audio=SimpleNamespace(file_id="audio-file-id")
            )
        ),
    )
    message = SimpleNamespace(bot=bot)

    uploaded = await _upload_guest_entries(
        message,
        [
            {
                "kind": "photo",
                "url": "https://example.com/photo.jpg",
                "path": None,
            },
            {
                "kind": "audio",
                "path": "/tmp/audio.mp3",
                "title": "Original sound",
                "performer": "@creator",
                "duration": 12,
            },
        ],
    )

    assert [entry["file_id"] for entry in uploaded] == [
        "photo-file-id",
        "audio-file-id",
    ]
    bot.send_photo.assert_awaited_once()
    bot.send_audio.assert_awaited_once()
    assert bot.send_audio.await_args.kwargs["title"] == "Original sound"
    assert bot.send_audio.await_args.kwargs["performer"] == "@creator"
