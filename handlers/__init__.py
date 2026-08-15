from aiogram import Router

from . import user, tiktok, youtube, spotify, admin, twitter, instagram, soundcloud, pinterest, threads, guest_video

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

__all__ = [
    router
]