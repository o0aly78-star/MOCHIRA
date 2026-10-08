from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .config import BOT_TOKEN
from .db import (
    init_db, ensure_player, get_player, add_currency, add_xp,
    add_mochi, get_mochi, leaderboard
)
from .game import roll_mochi, random_event, COMMANDS


def player_name(update):
    u = update.effective_user
    return u.full_name or u.username or "Player"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    ensure_player(u.id, u.username, player_name(update))
    await update.message.reply_text(
        "🍡 Welcome to MOCHIRA!\n\n"
        "Your group adventure starts here.\n"
        "Try /mochi, /profile, /collection or /leaderboard."
    )


async def mochi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    ensure_player(u.id, u.username, player_name(update))

    species, rarity, power = roll_mochi()
    add_mochi(u.id, species, rarity, power)
    add_currency(u.id, coins=10)
    add_xp(u.id, 15)

    await update.message.reply_text(
        f"🍡 A wild {species} appeared!\n"
        f"✨ Rarity: {rarity}\n"
        f"⚡ Power: {power}\n"
        f"🪙 +10 Coins / ⭐ +15 XP"
    )


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    ensure_player(u.id, u.username, player_name(update))
    p = get_player(u.id)

    await update.message.reply_text(
        f"👤 {p['name']}\n"
        f"🏆 Level: {p['level']}\n"
        f"⭐ XP: {p['xp']}\n"
        f"🪙 Coins: {p['coins']}\n"
        f"💎 Gems: {p['gems']}\n"
        f"🎟 Tickets: {p['tickets']}"
    )


async def collection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    ensure_player(u.id, u.username, player_name(update))
    items = get_mochi(u.id)

    if not items:
        await update.message.reply_text(
            "🍡 Your collection is empty. Try /mochi!"
        )
        return

    lines = ["🍡 Your MOCHIRA collection:"]

    for x in items[:20]:
        lines.append(
            f"• {x['species']} — {x['rarity']} — "
            f"Lv.{x['level']} — ⚡{x['power']}"
        )

    await update.message.reply_text("\n".join(lines))


async def event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    ensure_player(u.id, u.username, player_name(update))

    kind, amount = random_event()

    if kind == "coin":
        add_currency(u.id, coins=amount)
        reward = f"🪙 +{amount} Coins"

    elif kind == "gem":
        add_currency(u.id, gems=amount)
        reward = f"💎 +{amount} Gems"

    elif kind == "ticket":
        add_currency(u.id, tickets=amount)
        reward = f"🎟 +{amount} Ticket"

    else:
        add_xp(u.id, amount)
        reward = f"⭐ +{amount} XP"

    await update.message.reply_text(
        f"🎲 Random event!\n{reward}"
    )


async def board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = leaderboard()

    if not rows:
        await update.message.reply_text("No players yet.")
        return

    lines = ["🏆 MOCHIRA Leaderboard"]

    for i, p in enumerate(rows, 1):
        lines.append(
            f"{i}. {p['name']} — Lv.{p['level']} ({p['xp']} XP)"
        )

    await update.message.reply_text("\n".join(lines))


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🍡 MOCHIRA commands\n\n"
        "/start — start your profile\n"
        "/mochi — discover a Mochi\n"
        "/profile — your profile\n"
        "/collection — your Mochis\n"
        "/event — random event\n"
        "/leaderboard — top players\n"
        "/help — commands"
    )


async def phrase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    key = update.message.text.strip().lower().lstrip("/").split()[0]

    if key in COMMANDS:
        await update.message.reply_text(COMMANDS[key])


def main():
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mochi", mochi))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("collection", collection))
    app.add_handler(CommandHandler("event", event))
    app.add_handler(CommandHandler("leaderboard", board))
    app.add_handler(CommandHandler("help", help_cmd))

    for cmd in COMMANDS:
        app.add_handler(CommandHandler(cmd, phrase))

    app.run_polling()


if __name__ == "__main__":
    main()
