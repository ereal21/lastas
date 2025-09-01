import os
from aiogram import Bot

from bot.misc import EnvKeys


async def notify_owner_of_purchase(
    bot: Bot,
    username: str,
    formatted_time: str,
    item_name: str,
    item_price: float,
    parent_cat: str | None,
    category_name: str,
    photo_description: str,
    file_path: str | None,
) -> None:
    """Send purchase details to the bot owner.

    If ``file_path`` is provided and points to an existing file, the file is sent
    as a photo/video with the details in the caption. Otherwise a text message is
    sent.

    The notification includes the buyer's username, purchase date, product name,
    price, category, subcategory and photo description.
    """
    text = (
        f"User: {username}\n"
        f"Date: {formatted_time} GMT+3\n"
        f"Product: {item_name}\n"
        f"Price: {item_price}€\n"
        f"Category: {parent_cat or '-'}\n"
        f"Subcategory: {category_name}\n"
        f"Photo description: {photo_description or '-'}"
    )

    owner_id = EnvKeys.OWNER_ID
    if not owner_id:
        return
    try:
        owner_id = int(owner_id)
    except (TypeError, ValueError):
        pass

    owner_id = int(EnvKeys.OWNER_ID) if EnvKeys.OWNER_ID else None
    if owner_id is None:
        return


    if file_path and os.path.isfile(file_path):
        with open(file_path, "rb") as media:
            if file_path.endswith(".mp4"):
                await bot.send_video(owner_id, media, caption=text)
            else:
                await bot.send_photo(owner_id, media, caption=text)
    else:
        await bot.send_message(owner_id, text)
