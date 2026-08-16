from aiogram import F, Router, types

from app_context import bot
from services.links.detection import extract_supported_links

from . import (
    admin,
    guest_video,
    instagram,
    media_download,
    pinterest,
    soundcloud,
    spotify,
    threads,
    tiktok,
    twitter,
    user,
    youtube,
)

router = Router(name=__name__)

router.include_routers(
    user.router,
    tiktok.router,
    youtube.router,
    spotify.router,
    admin.router,
    twitter.router,
    instagram.router,
    threads.router,
    soundcloud.router,
    pinterest.router,
    guest_video.router,
)


def _with_channel_actor(message: types.Message, actor: types.User) -> types.Message:
    """Return a channel message with a usable actor for shared download handlers.

    Telegram normally omits ``from_user`` from channel posts.  The existing
    platform handlers use it for analytics and request de-duplication, so the
    bot identity is supplied without changing the destination channel.
    """
    if message.from_user is not None:
        return message
    return message.model_copy(update={"from_user": actor})


@router.channel_post(F.text | F.caption)
async def process_channel_post(message: types.Message) -> None:
    """Download supported links posted directly in a channel."""
    links = extract_supported_links(message.text or message.caption or "")
    if not links:
        return

    channel_message = _with_channel_actor(message, await bot.get_me())

    if len(links) > 1:
        await media_download.process_batch_links(channel_message)
        return

    service, url = links[0]
    await media_download._process_supported_link(channel_message, service, url)


__all__ = ["router"]
