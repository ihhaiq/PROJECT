from services.i18n import is_arabic


def cancel(language: str | None = None):
    return "✖️ إلغاء" if is_arabic(language) else "✖️ Cancel"


def welcome_message(language: str | None = None):
    if is_arabic(language):
        return (
            '<b>مرحبًا بك في MaxLoad <tg-emoji emoji-id="5420141555233071341">❤️</tg-emoji></b>\n\n'
            "أرسل رابطًا واحدًا أو أكثر في رسالة واحدة، وسأقوم بتنزيل ما أستطيع.\n\n"
            "<b>المواقع المدعومة</b>\n"
            '<tg-emoji emoji-id="5233671414023753035">📷</tg-emoji> إنستغرام\n'
            '<tg-emoji emoji-id="5370693953236539466">🧵</tg-emoji> Threads\n'
            '<tg-emoji emoji-id="5233597424622144804">🎵</tg-emoji> تيك توك\n'
            '<tg-emoji emoji-id="5233311027612913110">▶️</tg-emoji> يوتيوب\n'
            '<tg-emoji emoji-id="5231309843435919433">🐦</tg-emoji> X / Twitter\n'
            '<tg-emoji emoji-id="5233448977667492819">🎧</tg-emoji> ساوند كلاود\n'
            '<tg-emoji emoji-id="5391001065418172193">🟢</tg-emoji> Spotify\n'
            '<tg-emoji emoji-id="5233210422298974231">📌</tg-emoji> Pinterest\n\n'
            "استخدم الأزرار أدناه لتجربة الوضع الداخلي، ضبط الإعدادات، أو مشاركة البوت."
        )
    return (
        '<b>Welcome to MaxLoad <tg-emoji emoji-id="5420141555233071341">❤️</tg-emoji></b>\n\n'
        "Send one link, or paste several links in one message, and I'll download what I can.\n\n"
        "<b>Supported sites</b>\n"
        '<tg-emoji emoji-id="5233671414023753035">📷</tg-emoji> Instagram\n'
        '<tg-emoji emoji-id="5370693953236539466">🧵</tg-emoji> Threads\n'
        '<tg-emoji emoji-id="5233597424622144804">🎵</tg-emoji> TikTok\n'
        '<tg-emoji emoji-id="5233311027612913110">▶️</tg-emoji> YouTube\n'
        '<tg-emoji emoji-id="5231309843435919433">🐦</tg-emoji> X / Twitter\n'
        '<tg-emoji emoji-id="5233448977667492819">🎧</tg-emoji> SoundCloud\n'
        '<tg-emoji emoji-id="5391001065418172193">🟢</tg-emoji> Spotify\n'
        '<tg-emoji emoji-id="5233210422298974231">📌</tg-emoji> Pinterest\n\n'
        "Use the buttons below to try inline mode, tune settings, or share the bot."
    )


def settings(language: str | None = None):
    if is_arabic(language):
        return (
            "<b>⚙️ الإعدادات</b>\n"
            "استخدم الأزرار أدناه لتخصيص كيفية إرسال التنزيلات. "
            "تُطبق هذه التغييرات على حسابك فقط."
        )
    return (
        "<b>⚙️ Settings</b>\n"
        "Use the buttons below to customize how downloads are sent. "
        "These changes apply only to your account."
    )


def settings_private_only(language: str | None = None):
    if is_arabic(language):
        return "الإعدادات متاحة فقط في الدردشة الخاصة. افتح دردشة خاصة مع البوت لتغيير التفضيلات."
    return (
        "Settings are available only in private chat. Open DM with the bot to change preferences."
    )


def get_field_text(field: str, language: str | None = None):
    if is_arabic(language):
        texts = {
            "captions": (
                "<b>📝 الوصف</b>\n"
                "إظهار أو إخفاء وصف المنشور في الملفات المنزلة. "
                "قد لا توفر بعض المصادر أوصافًا."
            ),
            "delete_message": (
                "<b>🗑️ حذف الرسائل</b>\n"
                "احذف رابطك تلقائيًا بعد معالجة التنزيل."
            ),
            "info_buttons": (
                "<b>ℹ️ أزرار المعلومات</b>\n"
                "تشغيل أو إيقاف أزرار المعلومات الإضافية أسفل الوسائط المنزلة."
            ),
            "url_button": (
                "<b>🔗 زر الرابط</b>\n"
                "إظهار أو إخفاء زر رابط المنشور الأصلي."
            ),
            "audio_button": (
                "<b>🎧 زر MP3</b>\n"
                "تشغيل أو إيقاف زر تنزيل MP3 عندما يكون الصوت متاحًا."
            ),
            "file_button": (
                "<b>📄 زر الملف</b>\n"
                "إظهار أو إخفاء زر تنزيل الملف أسفل الفيديوهات للحصول على الملفات الأصلية غير المضغوطة حسب الطلب."
            ),
            "video_quality": (
                "<b>🎬 جودة الفيديو</b>\n"
                "اختر جودة تنزيل الفيديو المفضلة:\n\n"
                "• <b>الأفضل (1080p+)</b>: الحد الأقصى الممكن من الدقة.\n"
                "• <b>المتوازن (720p)</b>: توازن جيد بين الجودة والسرعة.\n"
                "• <b>توفير البيانات (480p)</b>: تنزيلات أسرع مع استخدام أقل للبيانات."
            ),
            "as_document": (
                "<b>📄 الإرسال كملف</b>\n"
                "عند التفعيل، تُرسل الفيديوهات والصور كملفات غير مضغوطة (.mp4 / .jpg) مع الاحتفاظ بجودة أصلية 100%."
            ),
            "audio_format": (
                "<b>🎵 تنسيق الصوت</b>\n"
                "اختر التنسيق الافتراضي للصوت:\n\n"
                "• <b>MP3</b>: التنسيق الشائع والموحد.\n"
                "• <b>M4A (AAC)</b>: تنسيق مضغوط عالي الجودة لنظام iOS وMac.\n"
                "• <b>FLAC / الأصلي</b>: صوت فاقد للإتلاف بدون ضغط عند توفره."
            ),
        }
        return texts.get(field, "<b>الإعدادات</b>\nلا يوجد وصف لهذه الخيارة بعد.")

    texts = {
        "captions": (
            "<b>📝 Descriptions</b>\n"
            "Show or hide post captions in downloaded media. "
            "Some sources may not provide captions."
        ),
        "delete_message": (
            "<b>🗑️ Delete Messages</b>\n"
            "Automatically remove your link once the download is handled."
        ),
        "info_buttons": (
            "<b>ℹ️ Info Buttons</b>\n"
            "Toggle additional info buttons under downloaded media."
        ),
        "url_button": (
            "<b>🔗 URL Button</b>\n"
            "Show or hide a button with the original post link."
        ),
        "audio_button": (
            "<b>🎧 MP3 Button</b>\n"
            "Toggle the Download MP3 button when audio is available."
        ),
        "file_button": (
            "<b>📄 File Button</b>\n"
            "Show or hide the Download File button under videos to get original uncompressed files on demand."
        ),
        "video_quality": (
            "<b>🎬 Video Quality</b>\n"
            "Select your preferred video download resolution:\n\n"
            "• <b>Best (1080p+)</b>: Maximum possible resolution.\n"
            "• <b>Balanced (720p)</b>: Great balance of quality and speed.\n"
            "• <b>Data Saver (480p)</b>: Faster downloads with minimal data usage."
        ),
        "as_document": (
            "<b>📄 Send as File</b>\n"
            "When enabled, videos and photos will be sent as uncompressed documents (.mp4 / .jpg) preserving 100% original quality."
        ),
        "audio_format": (
            "<b>🎵 Audio Format</b>\n"
            "Choose default audio format for music downloads:\n\n"
            "• <b>MP3</b>: Standard universal audio format.\n"
            "• <b>M4A (AAC)</b>: High quality compact format for iOS & Mac.\n"
            "• <b>FLAC / Original</b>: Uncompressed lossless audio where available."
        ),
    }
    return texts.get(field, "<b>Settings</b>\nThis option doesn't have a description yet.")


def captions(user_captions, post_caption, bot_url, *, limit: int = 1024):
    import html

    def _truncate_escaped(value: str, max_len: int) -> str:
        if max_len <= 0:
            return ""
        if len(value) <= max_len:
            return value
        cut = value[:max_len]
        amp = cut.rfind("&")
        semi = cut.rfind(";")
        if amp > semi:
            cut = cut[:amp]
        return cut

    footer_label = "بواسطة" if is_arabic() else "Powered by"
    footer = '<tg-emoji emoji-id="5283080528818360566">🚀</tg-emoji> {label} <a href="{bot_url}">byhussin</a>'.format(
        label=footer_label,
        bot_url=bot_url,
    )

    if user_captions == "on" and post_caption:
        body = html.escape(str(post_caption))
        sep = "\n\n"
        # Keep footer intact; only shrink the body.
        budget = limit - len(sep) - len(footer)
        if budget <= 0:
            return _truncate_escaped(footer, limit)

        if len(body) > budget:
            suffix = "…"
            body = _truncate_escaped(body, max(0, budget - len(suffix))).rstrip() + suffix

        return f"{body}{sep}{footer}"

    return _truncate_escaped(footer, limit)


def downloading_audio_status(language: str | None = None):
    return "🎧 جار تنزيل الصوت..." if is_arabic(language) else "🎧 Downloading audio..."


def downloading_video_status(language: str | None = None):
    text = "جار تنزيل الفيديو..." if is_arabic(language) else "Downloading video..."
    return f"<tg-emoji emoji-id='5375464961822695044'>🎬</tg-emoji> {text}"


def pending_download_status(language: str | None = None):
    if is_arabic(language):
        return "⏳ جار التحميل... سأرسل لك النتيجة فور انتهائها."
    return "⏳ Downloading... I will send the result as soon as it is ready."


def uploading_status(language: str | None = None):
    return "☁️ جار رفع الملف إلى Telegram..." if is_arabic(language) else "☁️ Uploading file to Telegram..."


def retrying_again_status(next_attempt: int, total_attempts: int, language: str | None = None):
    if is_arabic(language):
        return f"حدث خطأ، جار المحاولة مجددًا... ({next_attempt}/{total_attempts})"
    return f"Error, trying again... ({next_attempt}/{total_attempts})"


def dm_start_required(language: str | None = None):
    if is_arabic(language):
        return "<tg-emoji emoji-id='5472308992514464048'>🔒</tg-emoji> الإعداد الأولي مطلوب: افتح الدردشة الخاصة، اضغط Start، ثم أعد إرسال الرابط."
    return "<tg-emoji emoji-id='5472308992514464048'>🔒</tg-emoji> First-time setup needed: open DM, press Start, and resend the link."


def duplicate_link_processing(language: str | None = None):
    if is_arabic(language):
        return "هذا الرابط قيد المعالجة بالفعل. انتظر بضع ثوانٍ."
    return "This link is already being processed. Wait a few seconds."


def duplicate_link_recently_processed(language: str | None = None):
    if is_arabic(language):
        return "تم التعامل مع هذا الرابط مؤخرًا. إذا كنت لا تزال تحتاجه، حاول مرة أخرى بعد بضع ثوانٍ."
    return "This link was just handled. If you still need it, try again in a few seconds."


def settings_admin_only(language: str | None = None):
    if is_arabic(language):
        return "يمكن للمشرفين فقط فتح /settings داخل المجموعات."
    return "Only group admins can open /settings in group chats."


def invalid_settings_option(language: str | None = None):
    if is_arabic(language):
        return "خيار الإعدادات غير صالح."
    return "Invalid settings option."


def settings_update_failed(language: str | None = None):
    if is_arabic(language):
        return "تعذر تحديث الإعدادات الآن. حاول مرة أخرى لاحقًا."
    return "Couldn't update settings right now. Please try again later."


def inline_only_button(language: str | None = None):
    if is_arabic(language):
        return "هذا الزر يعمل في الوضع الداخلي فقط."
    return "This button works only in inline mode."


def unknown_data(language: str | None = None):
    return "بيانات غير معروفة" if is_arabic(language) else "Unknown data"


def callback_processing_error(language: str | None = None):
    return "حدث خطأ أثناء معالجة الزر" if is_arabic(language) else "Error processing callback"


def stat_value_label(key: str, language: str | None = None) -> str:
    labels = {
        "followers": "المتابعون",
        "videos": "الفيديوهات",
        "likes": "الإعجابات",
        "views": "المشاهدات",
        "comments": "التعليقات",
        "shares": "المشاركات",
    }
    if is_arabic(language):
        return labels.get(key, key)
    return key.replace("_", " ").title()


def join_group(chat_title: str, language: str | None = None) -> str:
    if is_arabic(language):
        return (
            "شكرًا لإضافتي إلى <b>{chat_title}</b> <tg-emoji emoji-id='5280764381804650651'>🌸</tg-emoji>\n"
            "يرجى منحي <b>صلاحيات المشرف</b> لتفعيل جميع الميزات 🔓"
        ).format(chat_title=chat_title)
    return (
        "Thanks for adding me to <b>{chat_title}</b> <tg-emoji emoji-id='5280764381804650651'>🌸</tg-emoji>\n"
        "Please grant me <b>admin rights</b> to unlock full functionality 🔓"
    ).format(chat_title=chat_title)


def admin_rights_granted(chat_title: str, language: str | None = None) -> str:
    if is_arabic(language):
        return (
            "شكرًا لمنحي صلاحيات المشرف في <b>{chat_title}</b> <tg-emoji emoji-id='5280764381804650651'>🌸</tg-emoji>\n"
            "💻 سأحافظ على عمل التنزيلات بسلاسة."
        ).format(chat_title=chat_title)
    return (
        "Thanks for granting admin rights in <b>{chat_title}</b> <tg-emoji emoji-id='5280764381804650651'>🌸</tg-emoji>\n"
        "💻 I'll keep downloads running smoothly."
    ).format(chat_title=chat_title)


def keyboard_removed(language: str | None = None):
    if is_arabic(language):
        return "تم حذف لوحة المفاتيح." 
    return "Reply keyboard removed."


def tiktok_live_not_supported(language: str | None = None):
    if is_arabic(language):
        return "بثوث TikTok المباشرة غير مدعومة بعد. أرسل رابط منشور TikTok عادي."
    return "TikTok LIVE streams aren't supported yet. Send a regular TikTok post link."


def delete_permission_warning(language: str | None = None):
    if is_arabic(language):
        return "فشل الحذف التلقائي: لا توجد صلاحية حذف الرسائل في هذه الدردشة. يُرجى منح صلاحية الحذف أو إيقاف الحذف التلقائي من الإعدادات."
    return "Auto-delete failed: missing permission to delete messages in this chat. Please grant delete permissions or turn off auto-delete in settings."


def stats_temporarily_unavailable(language: str | None = None):
    if is_arabic(language):
        return "تعذر إنشاء الإحصائيات الآن. حاول مرة أخرى لاحقًا."
    return "Couldn't generate stats right now. Please try again later."


def no_queue_metrics_yet(language: str | None = None):
    if is_arabic(language):
        return "لا توجد مقاييس قائمة انتظار بعد."
    return "No queue metrics yet."


def open_bot_for_audio(language: str | None = None):
    if is_arabic(language):
        return "افتح البوت في الدردشة الخاصة لتنزيل الصوت."
    return "Open the bot in private chat to download audio."


def audio_fetch_failed(language: str | None = None):
    if is_arabic(language):
        return "فشل في الحصول على معلومات الصوت. حاول مرة أخرى لاحقًا."
    return "Failed to get audio info. Please try again later."


def audio_download_failed(language: str | None = None):
    if is_arabic(language):
        return "فشل تنزيل الصوت. حاول مرة أخرى لاحقًا."
    return "Audio download failed. Please try again later."


def spotify_metadata_failed(language: str | None = None):
    if is_arabic(language):
        return "تعذر قراءة هذا المسار من Spotify. تحقق من الرابط ثم حاول مرة أخرى."
    return "Couldn't read this Spotify track. Please check the link and try again."


def spotify_source_not_found(language: str | None = None):
    if is_arabic(language):
        return "تعذر العثور على مصدر صوت مطابق لهذا المسار من Spotify."
    return "Couldn't find a matching audio source for this Spotify track."


def inline_album_link_invalid(language: str | None = None):
    if is_arabic(language):
        return "رابط الألبوم منتهي أو غير صالح."
    return "This album link is expired or invalid."


def inline_photo_title(service_name: str, language: str | None = None):
    return f"صورة {service_name}" if is_arabic(language) else f"{service_name} Photo"


def inline_photo_description(language: str | None = None):
    return "صورة واحدة" if is_arabic(language) else "Single photo"


def inline_album_title(service_name: str, language: str | None = None):
    return f"ألبوم {service_name}" if is_arabic(language) else f"{service_name} Album"


def inline_album_description(language: str | None = None):
    return "افتح الألبوم الكامل في البوت" if is_arabic(language) else "Open full album in bot"


def inline_open_full_album_button(language: str | None = None):
    return "فتح الألبوم الكامل" if is_arabic(language) else "Open Full Album"


def inline_photos_title(service_name: str, language: str | None = None):
    return f"صور {service_name}" if is_arabic(language) else f"{service_name} Photos"


def inline_photos_not_supported(service_name: str, language: str | None = None):
    if is_arabic(language):
        return f"صور {service_name} غير مدعومة في الوضع الداخلي."
    return f"{service_name} photos are not supported inline."


def inline_send_video_button(language: str | None = None):
    return "إرسال الفيديو داخليًا" if is_arabic(language) else "Send video inline"


def inline_send_video_prompt(service_name: str, language: str | None = None):
    if is_arabic(language):
        return f"جار تجهيز فيديو {service_name}...\nإذا لم يبدأ تلقائيًا، اضغط الزر أدناه."
    return f"{service_name} video is being prepared...\nIf it does not start automatically, tap the button below."


def inline_send_audio_prompt(service_name: str, language: str | None = None):
    if is_arabic(language):
        return f"جار تجهيز صوت {service_name}...\nإذا لم يبدأ تلقائيًا، اضغط الزر أدناه."
    return f"{service_name} audio is being prepared...\nIf it does not start automatically, tap the button below."


def inline_video_already_processing(language: str | None = None):
    return "هذا الفيديو قيد التجهيز بالفعل." if is_arabic(language) else "This inline video is already being prepared."


def inline_video_already_sent(language: str | None = None):
    return "تم إرسال هذا الفيديو بالفعل." if is_arabic(language) else "This inline video was already sent."


def supported_sites_message(bot_username: str | None = None, language: str | None = None):
    return help_message(bot_username, language=language)


def category_settings_text(category: str, language: str | None = None) -> str:
    if is_arabic(language):
        if category == "media":
            return (
                "<b>🎬 إعدادات الوسائط والجودة</b>\n\n"
                "اضبط دقة الفيديو، تنسيق الملف، وخيارات الصوت:"
            )
        if category == "appearance":
            return (
                "<b>🎨 الشكل والأزرار</b>\n\n"
                "خصص أوصاف المنشورات، روابط URL الأصلية، وأزرار الإجراءات:"
            )
        if category == "chat":
            return (
                "<b>💬 الدردشة والتنظيف</b>\n\n"
                "إدارة سلوك الدردشة الجماعية وإعدادات تنظيف الرسائل:"
            )
        return settings(language=language)

    if category == "media":
        return (
            "<b>🎬 Media & Quality Settings</b>\n\n"
            "Configure video resolution, file format, and audio options:"
        )
    if category == "appearance":
        return (
            "<b>🎨 Appearance & Buttons</b>\n\n"
            "Customize post descriptions, original URL links, and action buttons:"
        )
    if category == "chat":
        return (
            "<b>💬 Chat & Clean-up</b>\n\n"
            "Manage group chat behavior and message cleanup settings:"
        )
    return settings(language=language)


def help_message(bot_username: str | None = None, language: str | None = None) -> str:
    username = bot_username or "byhusseinBot"
    is_ar = is_arabic(language)
    if is_ar:
        return (
            "<b>📖 دليل MaxLoad</b>\n\n"
            "أرسل رابطًا واحدًا أو أكثر في رسالة واحدة. سيقوم البوت باستخراج الوسائط وتسليمها تلقائيًا.\n\n"
            "<blockquote expandable><b>📷 إنستغرام & Threads</b>\n"
            "• تنزيل المنشورات، الريلز، IGTV، والقصص\n"
            "• ألبومات الصور والمحتوى المتعدد\n"
            "• انسخ الرابط عبر المشاركة → نسخ الرابط</blockquote>\n\n"
            "<blockquote expandable><b>🎵 تيك توك</b>\n"
            "• تنزيلات فيديو بدون علامة مائية\n"
            "• بطاقات الصور والعروض\n"
            "• دعم استخراج MP3</blockquote>\n\n"
            "<blockquote expandable><b>▶️ يوتيوب & يوتيوب ميوزيك</b>\n"
            "• Shorts والفيديوهات العادية\n"
            "• تدفقات صوتية وفيديو بجودة عالية\n"
            "• اضغط زر MP3 لتنزيل الصوت</blockquote>\n\n"
            "<blockquote expandable><b>🐦 X / Twitter & 📌 Pinterest</b>\n"
            "• فيديوهات X / Twitter، GIFs، وصور\n"
            "• فيديوهات وصور Pinterest</blockquote>\n\n"
            "<blockquote expandable><b>🎧 SoundCloud & 🟢 Spotify</b>\n"
            "• أغانٍ عالية الجودة من SoundCloud\n"
            "• مطابقة مسارات Spotify وتنزيل الصوت</blockquote>\n\n"
            f"<blockquote expandable><b>⚡ الوضع الداخلي</b>\n"
            f"• اكتب <code>@{username} [رابط]</code> في أي دردشة\n"
            "• معاينة فورية ومشاركة مباشرة</blockquote>\n\n"
            "<blockquote expandable><b>📦 التنزيلات المجمعة</b>\n"
            "• ألحق حتى 6 روابط في رسالة واحدة\n"
            "• يتم التوصيل واحدًا تلو الآخر للحفاظ على نظافة الدردشة</blockquote>"
        )

    return (
        "<b>📖 MaxLoad Help & Guide</b>\n\n"
        "Send one link or paste multiple links in one message. The bot will automatically extract and deliver the media.\n\n"
        "<blockquote expandable><b>📷 Instagram & Threads</b>\n"
        "• Download Posts, Reels, IGTV & Stories\n"
        "• Photo carousels & multi-media albums\n"
        "• Copy link via Share → Copy link</blockquote>\n\n"
        "<blockquote expandable><b>🎵 TikTok</b>\n"
        "• Watermark-free video downloads\n"
        "• Photo carousels & slideshows\n"
        "• MP3 audio extraction supported</blockquote>\n\n"
        "<blockquote expandable><b>▶️ YouTube & YouTube Music</b>\n"
        "• YouTube Shorts & regular Videos\n"
        "• High quality audio & video streams\n"
        "• Tap MP3 button to download audio</blockquote>\n\n"
        "<blockquote expandable><b>🐦 X / Twitter & 📌 Pinterest</b>\n"
        "• X / Twitter videos, GIFs & images\n"
        "• Pinterest video and image Pins</blockquote>\n\n"
        "<blockquote expandable><b>🎧 SoundCloud & 🟢 Spotify</b>\n"
        "• High quality SoundCloud audio tracks\n"
        "• Spotify track matching & audio download</blockquote>\n\n"
        f"<blockquote expandable><b>⚡ Inline Mode</b>\n"
        f"• Type <code>@{username} [link]</code> in any chat\n"
        "• Instant preview and direct media sharing</blockquote>\n\n"
        "<blockquote expandable><b>📦 Batch Downloading</b>\n"
        "• Paste up to 6 links in a single message\n"
        "• Delivered one by one to keep chat clean</blockquote>"
    )


def referral_message(bot_username: str, user_id: int, invited_count: int, language: str | None = None) -> str:
    username = bot_username or "MaxLoadBot"
    ref_link = f"https://t.me/{username}?start=ref_{user_id}"
    if is_arabic(language):
        return (
            "<b>👥 برنامج الإحالة الخاص بك</b>\n\n"
            "ادعُ أصدقاءك لاستخدام MaxLoad وشارك رابط الإحالة الخاص بك:\n"
            f"<code>{ref_link}</code>\n\n"
            f"المستخدمون المدعوون: <b>{invited_count}</b>"
        )
    return (
        "<b>👥 Your Referral Program</b>\n\n"
        "Invite friends to use MaxLoad! Share your personal referral link:\n"
        f"<code>{ref_link}</code>\n\n"
        f"Users invited: <b>{invited_count}</b>"
    )


def batch_links_started(processed_total: int, detected_total: int | None = None, language: str | None = None):
    if is_arabic(language):
        if detected_total is not None and detected_total > processed_total:
            return (
                f"عُثر على {detected_total} رابطًا مدعومًا. "
                f"سأعالج أول {processed_total} روابط واحدًا تلو الآخر للحفاظ على ترتيب الدردشة."
            )
        return f"عُثر على {processed_total} رابطًا مدعومًا. سأعالجها واحدًا تلو الآخر للحفاظ على ترتيب الدردشة."
    if detected_total is not None and detected_total > processed_total:
        return (
            f"Found {detected_total} supported links. "
            f"I'll process the first {processed_total} one by one so the chat stays readable."
        )
    return f"Found {processed_total} supported links. I'll process them one by one so the chat stays readable."


def batch_link_progress(current: int, total: int, service_name: str, language: str | None = None):
    if is_arabic(language):
        return f"جار معالجة الرابط {current}/{total}: {service_name}..."
    return f"Processing link {current}/{total}: {service_name}..."


def batch_links_finished(total: int, language: str | None = None):
    return f"اكتملت معالجة {total} روابط." if is_arabic(language) else f"Finished batch processing for {total} links."


def timeout_error(language: str | None = None):
    if is_arabic(language):
        return "انتهت مهلة الطلب. قد يكون المصدر بطيئًا الآن، حاول مرة أخرى لاحقًا."
    return "Request timed out. The source may be slow right now. Please try again later."


def something_went_wrong(language: str | None = None):
    if is_arabic(language):
        return (
            "تعذرت معالجة هذا الرابط الآن.\n"
            "قد يكون خاصًا، محذوفًا، محظورًا في منطقتك، أو محجوبًا مؤقتًا من المصدر. "
            "حاول مرة أخرى لاحقًا."
        )
    return (
        "Couldn't process this link right now.\n"
        "It may be private, deleted, region-limited, or temporarily blocked by the source. "
        "Please try again later."
    )


def video_too_large(language: str | None = None):
    if is_arabic(language):
        return "حجم الفيديو أكبر من حد Telegram. جرّب فيديو أقصر أو خيار MP3/الصوت إن كان متاحًا."
    return "The video is too large for Telegram. Try a shorter video or an MP3/audio option if available."


def audio_too_large(language: str | None = None):
    if is_arabic(language):
        return "حجم الملف الصوتي أكبر من حد Telegram. جرّب مقطعًا أقصر أو رابط مصدر آخر."
    return "The audio is too large for Telegram. Try a shorter track or another source link."


def nothing_found(language: str | None = None):
    if is_arabic(language):
        return "لم يُعثر على وسائط. تأكد أن الرابط عام وغير منتهٍ ويشير مباشرةً إلى منشور أو فيديو."
    return "No media found. Check that the link is public, not expired, and points directly to a post or video."
