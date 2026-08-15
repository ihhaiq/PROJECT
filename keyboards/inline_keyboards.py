from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


from urllib.parse import quote
from services.i18n import is_arabic


def start_keyboard(
    bot_username: str | None = None,
    ref_user_id: int | None = None,
    language: str | None = None,
) -> InlineKeyboardMarkup:
    username = bot_username or "MaxLoadBot"
    base_link = f"https://t.me/{username}"

    arabic = is_arabic(language)
    share_text = (
        "بوت تنزيل سريع من Instagram وTikTok وYouTube والمزيد!"
        if arabic
        else "Fast downloader bot for Instagram, TikTok, YouTube & more!"
    )
    share_url = f"https://t.me/share/url?url={quote(base_link)}&text={quote(share_text)}"
    add_to_group_url = f"https://t.me/{username}?startgroup=true"
    lang_label = "🌐 English" if arabic else "🌐 العربية"
    lang_callback = "set_lang:en" if arabic else "set_lang:ar"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ الوضع الداخلي" if arabic else "⚡ Try inline", switch_inline_query_current_chat=""),
                InlineKeyboardButton(text="⚙️ الإعدادات" if arabic else "⚙️ Settings", callback_data="back_to_settings"),
            ],
            [
                InlineKeyboardButton(text=lang_label, callback_data=lang_callback),
            ],
            [
                InlineKeyboardButton(text="🚀 مشاركة البوت" if arabic else "🚀 Share bot", url=share_url),
                InlineKeyboardButton(text="➕ إضافة للمجموعة" if arabic else "➕ Add to group", url=add_to_group_url),
            ],
        ]
    )


def cancel_keyboard(language: str | None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ إلغاء" if is_arabic(language) else "❌ Cancel", callback_data="cancel_action")
    return builder.as_markup()


def format_number(value: int) -> str | None:
    if value is None:
        return None
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


FIELD_CATEGORY_MAP = {
    "video_quality": "media",
    "as_document": "media",
    "audio_format": "media",
    "captions": "appearance",
    "info_buttons": "appearance",
    "audio_button": "appearance",
    "file_button": "appearance",
    "url_button": "appearance",
    "delete_message": "chat",
}


def return_settings_categories_keyboard(language: str | None = None) -> InlineKeyboardMarkup:
    if is_arabic(language):
        labels = ("🎬 الوسائط والجودة", "🎨 الشكل والأزرار", "💬 الدردشة والتنظيف")
    else:
        labels = ("🎬 Media & Quality", "🎨 Appearance & Buttons", "💬 Chat & Clean-up")
    buttons = [
        [InlineKeyboardButton(text=labels[0], callback_data="settings_cat:media")],
        [InlineKeyboardButton(text=labels[1], callback_data="settings_cat:appearance")],
        [InlineKeyboardButton(text=labels[2], callback_data="settings_cat:chat")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def return_category_settings_keyboard(category: str, language: str | None = None) -> InlineKeyboardMarkup:
    arabic = is_arabic(language)
    if category == "media" and arabic:
        fields = [
            ("🎬 جودة الفيديو", "video_quality"),
            ("📄 الإرسال كملف", "as_document"),
            ("🎵 تنسيق الصوت", "audio_format"),
        ]
    elif category == "media":
        fields = [
            ("🎬 Video Quality", "video_quality"),
            ("📄 Send as File", "as_document"),
            ("🎵 Audio Format", "audio_format"),
        ]
    elif category == "appearance" and arabic:
        fields = [
            ("📝 الأوصاف", "captions"),
            ("ℹ️ أزرار المعلومات", "info_buttons"),
            ("🎧 زر MP3", "audio_button"),
            ("📄 زر الملف", "file_button"),
            ("🔗 زر الرابط", "url_button"),
        ]
    elif category == "appearance":
        fields = [
            ("📝 Descriptions", "captions"),
            ("ℹ️ Info Buttons", "info_buttons"),
            ("🎧 MP3 Button", "audio_button"),
            ("📄 File Button", "file_button"),
            ("🔗 URL Button", "url_button"),
        ]
    elif arabic:
        fields = [("🗑️ حذف الرسائل", "delete_message")]
    else:
        fields = [
            ("🗑️ Delete Messages", "delete_message"),
        ]

    buttons = [
        [InlineKeyboardButton(text=text, callback_data=f"settings:{field}")]
        for text, field in fields
    ]
    back_label = "⬅️ العودة إلى الأقسام" if arabic else "⬅️ Back to Categories"
    buttons.append([InlineKeyboardButton(text=back_label, callback_data="back_to_settings")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def return_field_keyboard(field: str, value: str | None, language: str | None = None):
    val = (value or "").strip().lower()
    arabic = is_arabic(language)
    cat = FIELD_CATEGORY_MAP.get(field, "media")
    back_cb = f"settings_cat:{cat}"

    if field == "video_quality":
        current = val or "best"
        best = "الأفضل (1080p+)" if arabic else "Best (1080p+)"
        balanced = "متوازن (720p)" if arabic else "Balanced (720p)"
        saver = "توفير البيانات (480p)" if arabic else "Data Saver (480p)"
        opt_best = f"{'✅ ' if current == 'best' else ''}🏆 {best}"
        opt_bal = f"{'✅ ' if current == 'balanced' else ''}⚖️ {balanced}"
        opt_saver = f"{'✅ ' if current == 'saver' else ''}⚡ {saver}"

        buttons = [
            [InlineKeyboardButton(text=opt_best, callback_data="setting:video_quality:best")],
            [InlineKeyboardButton(text=opt_bal, callback_data="setting:video_quality:balanced")],
            [InlineKeyboardButton(text=opt_saver, callback_data="setting:video_quality:saver")],
            [InlineKeyboardButton(text="⬅️ رجوع" if arabic else "⬅️ Back", callback_data=back_cb)],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    if field == "audio_format":
        current = val or "mp3"
        mp3 = "صوت MP3" if arabic else "MP3 Audio"
        original = "FLAC / الأصلي" if arabic else "FLAC / Original"
        opt_mp3 = f"{'✅ ' if current == 'mp3' else ''}🎧 {mp3}"
        opt_m4a = "✅ 📱 M4A (AAC)" if current == "m4a" else "📱 M4A (AAC)"
        opt_best = f"{'✅ ' if current == 'best' else ''}🎼 {original}"

        buttons = [
            [InlineKeyboardButton(text=opt_mp3, callback_data="setting:audio_format:mp3")],
            [InlineKeyboardButton(text=opt_m4a, callback_data="setting:audio_format:m4a")],
            [InlineKeyboardButton(text=opt_best, callback_data="setting:audio_format:best")],
            [InlineKeyboardButton(text="⬅️ رجوع" if arabic else "⬅️ Back", callback_data=back_cb)],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    is_enabled = val == "on"
    if arabic:
        status_text = "🟢 مفعّل حاليًا" if is_enabled else "🔴 معطّل حاليًا"
        action_text = "🔴 إيقاف" if is_enabled else "🟢 تفعيل"
    else:
        status_text = "🟢 Currently ON" if is_enabled else "🔴 Currently OFF"
        action_text = "🔴 Turn OFF" if is_enabled else "🟢 Turn ON"
    next_value = "off" if is_enabled else "on"

    buttons = [
        [InlineKeyboardButton(text=status_text, callback_data="noop")],
        [InlineKeyboardButton(text=action_text, callback_data=f"setting:{field}:{next_value}")],
        [InlineKeyboardButton(text="⬅️ رجوع" if arabic else "⬅️ Back", callback_data=back_cb)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def return_settings_keyboard(language: str | None = None):
    return return_settings_categories_keyboard(language=language)


def stats_keyboard(current_period: str = "Week", mode: str = "total", language: str | None = None):
    periods = ["Week", "Month", "Year"]
    labels = {"Week": "أسبوع", "Month": "شهر", "Year": "سنة"} if is_arabic(language) else {}
    period_buttons = [
        InlineKeyboardButton(
            text=f"[{labels.get(period, period)}]" if period == current_period else labels.get(period, period),
            callback_data=f"stats:{period}:{mode}",
        )
        for period in periods
    ]

    toggle_target = "split" if mode == "total" else "total"
    if is_arabic(language):
        toggle_label = "العرض: حسب المنصة" if mode == "total" else "العرض: الإجمالي"
    else:
        toggle_label = "View: By platform" if mode == "total" else "View: Overall"

    buttons = [
        period_buttons,
        [InlineKeyboardButton(text=toggle_label, callback_data=f"stats:{current_period}:{toggle_target}")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="🩺 Health", callback_data="admin_ops"),
            InlineKeyboardButton(text="📦 Runtime", callback_data="admin_runtime_storage"),
        ],
        [InlineKeyboardButton(text="🔄 Refresh", callback_data="admin_refresh")],
        [InlineKeyboardButton(text="👥 Check Active Users", callback_data="check_active_users")],
        [InlineKeyboardButton(text="📬 Mailing", callback_data="send_to_all")],
        [InlineKeyboardButton(text="✉️ Message by Chat ID", callback_data="message_chat_id")],
        [
            InlineKeyboardButton(text="📄 View Log", callback_data="download_log"),
            InlineKeyboardButton(text="🗑️ Delete Log", callback_data="delete_log"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_detail_keyboard(refresh_callback: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Refresh", callback_data=refresh_callback)],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_admin")],
        ]
    )


def downloads_admin_keyboard(can_cleanup: bool = True, refresh_callback: str = "admin_downloads"):
    buttons = [[InlineKeyboardButton(text="🔄 Refresh", callback_data=refresh_callback)]]
    if can_cleanup:
        buttons.append([InlineKeyboardButton(text="🧹 Clean downloads", callback_data="admin_cleanup_downloads")])
    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_admin")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def return_back_to_admin_keyboard():
    back_button = [
        [InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_admin")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=back_button)


def start_private_chat_keyboard(bot_username: str, language: str | None = None):
    url = f"https://t.me/{bot_username}?start=from_group"
    text = "💬 فتح دردشة البوت" if is_arabic(language) else "💬 Open bot chat"
    button = [[InlineKeyboardButton(text=text, url=url)]]
    return InlineKeyboardMarkup(inline_keyboard=button)


def return_audio_download_keyboard(platform, url, language: str | None = None):
    audio_button = [
        [InlineKeyboardButton(text="🎧 تنزيل MP3" if is_arabic(language) else "🎧 Download MP3", callback_data=f"{platform}_audio_{url}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=audio_button)


def inline_send_video_keyboard(token: str, language: str | None = None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="إرسال الفيديو داخليًا" if is_arabic(language) else "Send video inline", callback_data=f"inline:tiktok:{token}")]
        ]
    )


def inline_send_media_keyboard(text: str, callback_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=callback_data)]
        ]
    )


def return_user_info_keyboard(nickname, followers, videos, likes, url):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=nickname, url=url))

    row1 = []
    if followers is not None:
        row1.append(
            InlineKeyboardButton(
                text=f"👥 {format_number(followers)}",
                callback_data=f"followers_{format_number(followers)}",
            )
        )
    if videos is not None:
        row1.append(
            InlineKeyboardButton(
                text=f"🎬 {format_number(videos)}",
                callback_data=f"videos_{format_number(videos)}",
            )
        )
    if likes is not None:
        row1.append(
            InlineKeyboardButton(
                text=f"❤️ {format_number(likes)}",
                callback_data=f"likes_{format_number(likes)}",
            )
        )

    if row1:
        builder.row(*row1)

    return builder.as_markup()


def return_video_info_keyboard(
    views,
    likes,
    comments,
    shares,
    music_play_url,
    video_url,
    user_settings,
    audio_callback_data: str | None = None,
    file_callback_data: str | None = None,
    language: str | None = None,
):
    builder = InlineKeyboardBuilder()

    if user_settings["info_buttons"] == "on":
        row1 = []
        if views is not None:
            formatted_views = format_number(views)
            row1.append(
                InlineKeyboardButton(
                    text=f"👁 {formatted_views}",
                    callback_data=f"views_{formatted_views}",
                )
            )
        if likes is not None:
            formatted_likes = format_number(likes)
            row1.append(
                InlineKeyboardButton(
                    text=f"❤️ {formatted_likes}",
                    callback_data=f"likes_{formatted_likes}",
                )
            )
        if comments is not None:
            formatted_comments = format_number(comments)
            row1.append(
                InlineKeyboardButton(
                    text=f"💬 {formatted_comments}",
                    callback_data=f"comments_{formatted_comments}",
                )
            )
        if shares is not None:
            formatted_shares = format_number(shares)
            row1.append(
                InlineKeyboardButton(
                    text=f"🔁 {formatted_shares}",
                    callback_data=f"shares_{formatted_shares}",
                )
            )

        if row1:
            builder.row(*row1)

    if user_settings.get("audio_button") == "on" and audio_callback_data:
        builder.row(InlineKeyboardButton(text="🎧 تنزيل MP3" if is_arabic(language) else "🎧 Download MP3", callback_data=audio_callback_data))

    if (
        user_settings.get("file_button") == "on"
        and user_settings.get("as_document") != "on"
        and file_callback_data
    ):
        builder.row(InlineKeyboardButton(text="📄 تنزيل الملف" if is_arabic(language) else "📄 Download File", callback_data=file_callback_data))

    if user_settings["url_button"] == "on" and video_url:
        builder.row(InlineKeyboardButton(text="🔗 الرابط" if is_arabic(language) else "🔗 URL", url=video_url))

    return builder.as_markup()


def _stats_keyboard_legacy_bottom(current_period: str = "Week", mode: str = "total"):
    periods = ["Week", "Month", "Year"]
    period_buttons = [
        InlineKeyboardButton(
            text=f"{'· ' if period == current_period else ''}{period}",
            callback_data=f"stats:{period}:{mode}",
        )
        for period in periods
    ]

    toggle_target = "split" if mode == "total" else "total"
    toggle_label = f"Split view: {'On' if mode == 'split' else 'Off'}"

    buttons = [
        period_buttons,
        [InlineKeyboardButton(text=toggle_label, callback_data=f"stats:{current_period}:{toggle_target}")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
