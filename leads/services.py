import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

def send_telegram_notification(lead) -> bool:
    """
    Отправляет мгновенное структурированное уведомление в Telegram о новой заявке.
    Получатель: Наталья Попыкина (директор по развитию) и/или общий рабочий чат.
    """
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '')

    if not token or not chat_id:
        logger.warning(
            "Telegram Bot Token или Chat ID не настроены. "
            "Заявка ID #%s сохранена в CRM, но пуш в Telegram пропущен.",
            lead.id
        )
        return False

    # Формируем читаемое архитектурное сообщение
    source_title = lead.get_source_display() if hasattr(lead, 'get_source_display') else lead.source
    
    text_lines = [
        "🏛 <b>НОВАЯ ЗАЯВКА: GB STUDIO</b>",
        "────────────────────",
        f"👤 <b>Клиент:</b> {lead.name}",
    ]

    if lead.company:
        text_lines.append(f"🏢 <b>Компания:</b> {lead.company}")

    # Телефон кликабелен для мгновенного набора Наталье
    clean_phone = "".join(ch for ch in lead.phone if ch.isdigit() or ch == '+')
    text_lines.append(f"📞 <b>Телефон:</b> <a href=\"tel:{clean_phone}\">{lead.phone}</a>")

    if lead.email:
        text_lines.append(f"📧 <b>Email:</b> {lead.email}")

    # Если это расчет сметы (B2B Fit-Out)
    if lead.object_type or lead.area_range:
        text_lines.extend([
            "",
            "📐 <b>Параметры объекта:</b>",
            f"• <b>Тип:</b> {lead.object_type or 'Не указан'}",
            f"• <b>Площадь:</b> {lead.area_range or 'Не указана'}",
        ])
        if lead.service_needed:
            text_lines.append(f"• <b>Класс отделки:</b> {lead.service_needed}")
        if lead.timeline:
            text_lines.append(f"• <b>Сроки реализации:</b> {lead.timeline}")
        if lead.estimated_cost:
            text_lines.append(f"• 💰 <b>Предварительная смета:</b> <b>{lead.estimated_cost}</b>")

    # ТЗ, запрос на картины или комментарий
    if lead.message:
        text_lines.extend([
            "",
            f"📝 <b>Детали / ТЗ:</b>\n<i>{lead.message}</i>"
        ])

    text_lines.extend([
        "────────────────────",
        f"📍 <b>Источник:</b> {source_title}",
        f"⏱ <b>Время:</b> {lead.created_at.strftime('%d.%m.%Y в %H:%M') if lead.created_at else 'Только что'}"
    ])

    message_html = "\n".join(text_lines)
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                'chat_id': chat_id,
                'text': message_html,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            },
            timeout=5.0
        )
        if response.status_code == 200:
            logger.info("Уведомление по лиду #%s успешно отправлено в Telegram.", lead.id)
            return True
        else:
            logger.error("Ошибка Telegram API (%s): %s", response.status_code, response.text)
            return False
    except Exception as exc:
        logger.error("Сбой соединения с Telegram API при отправке лида #%s: %s", lead.id, exc)
        return False
