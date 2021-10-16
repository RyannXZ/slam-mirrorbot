import shutil, psutil
import signal
import os
import asyncio

from pyrogram import idle
from sys import executable

from telegram import ParseMode
from telegram.ext import CommandHandler
from telegraph import Telegraph
from wserver import start_server_async
from bot import bot, app, dispatcher, updater, botStartTime, IGNORE_PENDING_REQUESTS, IS_VPS, PORT, alive, web, OWNER_ID, AUTHORIZED_CHATS, telegraph_token
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper import button_build
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, shell, eval, torrent_search, delete, speedtest, count, leech_settings


def stats(update, context):
    currentTime = get_readable_time(time.time() - botStartTime)
    Total, Digunakan, Bebas = shutil.disk_usage('.')
    Total = get_readable_file_size(total)
    Digunakan = get_readable_file_size(used)
    Bebas = get_readable_file_size(free)
    Dikirim = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    Diterima = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    PemakaianCPU = psutil.cpu_percent(interval=0.5)
    Memori = psutil.virtual_memory().percent
    Penyimpanan = psutil.disk_usage('/').percent
    stats = f'<b>Bot telah dijalankan selama ⏰:</b> <code>{currentTime}</code>\n' \
            f'<b>Total Penyimpanan ✅:</b> <code>{total}</code>\n' \
            f'<b>Digunakan ⚠️:</b> <code>{used}</code> ' \
            f'<b>Bebas ♻️:</b> <code>{free}</code>\n\n' \
            f'<b>Upload 📤:</b> <code>{sent}</code>\n' \
            f'<b>Download 📥:</b> <code>{recv}</code>\n\n' \
            f'<b>PemakaianCPU 🔥:</b> <code>{cpuUsage}%</code> ' \
            f'<b>Memori 💬:</b> <code>{memory}%</code> ' \
            f'<b>Penyimpanan ⚠️:</b> <code>{disk}%</code>'
    sendMessage(stats, context.bot, update)


def start(update, context):
    buttons = button_build.ButtonMaker()
    buttons.buildbutton("RyannGanteng 😱", "t.me/ur_fatherr")
    buttons.buildbutton("MirrorX ⚡️", "https://t.me/SlamMirrorUpdates")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(2))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        start_string = f'''
Bot ini ajaib, diturunkan dari planet antahberantah dan diberikan untuk ryan ganteng :v
Ketik /{BotCommands.HelpCommand} Untuk Mendapatkan Perintah 🦋
'''
        sendMarkup(start_string, context.bot, update, reply_markup)
    else:
        sendMarkup(
            'Oops! not a Authorized user.\nPlease deploy your own <b>slam-mirrorbot</b>.',
            context.bot,
            update,
            reply_markup,
        )


def restart(update, context):
    restart_message = sendMessage("Sabar anjg!", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    fs_utils.clean_all()
    alive.terminate()
    web.terminate()
    os.execl(executable, executable, "-m", "bot")


def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


def log(update, context):
    sendLogFile(context.bot, update)


help_string_telegraph = f'''<br>

Pesan : yang ga di translate artinya ga penting :D
<b>/{BotCommands.HelpCommand}</b>: To get this message
<br><br>
<b>/{BotCommands.MirrorCommand}</b> [download_url][magnet_link]: Untuk memulai mirror ke google drive 🦋.
<br><br>
<b>/{BotCommands.TarMirrorCommand}</b> [download_url][magnet_link]: Untuk memulai mirror ke google drive namun dengan format tar 🦋
<br><br>
<b>/{BotCommands.ZipMirrorCommand}</b> [download_url][magnet_link]: Untuk memulai mirror ke google drive namun dengan format zip🦋
<br><br>
<b>/{BotCommands.UnzipMirrorCommand}</b> [download_url][magnet_link]: Untuk memulai mirror ke google drive dan mengekstraknya 🦋
<br><br>
<b>/{BotCommands.QbMirrorCommand}</b> [magnet_link]: Untuk memulai mirror menggunakan qBittorrent 🦋, Pakai <b>/{BotCommands.QbMirrorCommand} s</b> untuk memilih file sebelum download
<br><br>
<b>/{BotCommands.QbTarMirrorCommand}</b> [magnet_link]: Untuk memulai mirror menggunakan qBittorrent namun dengan format tar 🦋
<br><br>
<b>/{BotCommands.QbZipMirrorCommand}</b> [magnet_link]: Untuk memulai mirror menggunakan qBittorrent namun dengan format zip 🦋
<br><br>
<b>/{BotCommands.QbUnzipMirrorCommand}</b> [magnet_link]: Untuk memulai mirror menggunakan qBittorrent dan mengekstraknya 🦋
<br><br>
<b>/{BotCommands.LeechCommand}</b> [download_url][magnet_link]: Start leeching to Telegram, Use <b>/{BotCommands.LeechCommand} s</b> to select files before leeching
<br><br>
<b>/{BotCommands.TarLeechCommand}</b> [download_url][magnet_link]:  Start leeching to Telegram and upload it as (.tar)
<br><br>
<b>/{BotCommands.ZipLeechCommand}</b> [download_url][magnet_link]: Start leeching to Telegram and upload it as (.zip)
<br><br>
<b>/{BotCommands.UnzipLeechCommand}</b> [download_url][magnet_link]: Start leeching to Telegram and if downloaded file is any archive, extracts it to Telegram
<br><br>
<b>/{BotCommands.QbLeechCommand}</b> [magnet_link]: Start leeching to Telegram using qBittorrent, Use <b>/{BotCommands.QbLeechCommand} s</b> to select files before leeching
<br><br>
<b>/{BotCommands.QbTarLeechCommand}</b> [magnet_link]: Start leeching to Telegram using qBittorrent and upload it as (.tar)
<br><br>
<b>/{BotCommands.QbZipLeechCommand}</b> [magnet_link]: Start leeching to Telegram using qBittorrent and upload it as (.zip)
<br><br>
<b>/{BotCommands.QbUnzipLeechCommand}</b> [magnet_link]: Start leeching to Telegram using qBittorrent and if downloaded file is any archive, extracts it to Telegram
<br><br>
<b>/{BotCommands.CloneCommand}</b> [drive_url]: Menyalin Folder dengan menggunakan jurus kagebunshin no jutsu 🦋
<br><br>
<b>/{BotCommands.CountCommand}</b> [drive_url]: Menghitung File dalam Folder di Google Drive
<br><br>
<b>/{BotCommands.DeleteCommand}</b> [drive_url]: Hapus file pada google drive ( Hanya Admin Dan Owner )
<br><br>
<b>/{BotCommands.WatchCommand}</b> [youtube-dl supported link]: Mirror video youtube kamu 🦋 Klik <b>/{BotCommands.WatchCommand}</b> untuk pertolongan selanjutnya
<br><br>
<b>/{BotCommands.TarWatchCommand}</b> [youtube-dl supported link]: Mirror video youtube kamu namun dengan format tar 🦋
<br><br>
<b>/{BotCommands.ZipWatchCommand}</b> [youtube-dl supported link]: Mirror video youtube kamu namun dengan format zip 🦋
<br><br>
<b>/{BotCommands.LeechWatchCommand}</b> [youtube-dl supported link]: Leech through youtube-dl 
<br><br>
<b>/{BotCommands.LeechTarWatchCommand}</b> [youtube-dl supported link]: Leech through youtube-dl and tar before uploading 
<br><br>
<b>/{BotCommands.LeechZipWatchCommand}</b> [youtube-dl supported link]: Leech through youtube-dl and zip before uploading 
<br><br>
<b>/{BotCommands.LeechSetCommand}</b>: Leech Settings 
<br><br>
<b>/{BotCommands.SetThumbCommand}</b>: Reply/Tag foto untuk dijadikan thumbnail ( hanya owner )
<br><br>
<b>/{BotCommands.CancelMirror}</b>: Reply/Tag ke pesan mirror yang ingin dibatalkan 🦋
<br><br>
<b>/{BotCommands.CancelAllCommand}</b>: Batal semua tugas yang dijalankan ( hanya owner )
<br><br>
<b>/{BotCommands.ListCommand}</b> [search term]: Mencari file/folder yang sudah di mirror didalam google drive 🦋
<br><br>
<b>/{BotCommands.StatusCommand}</b>: Memperlihatkan semua tugas mirror yang ada :D
<br><br>
<b>/{BotCommands.StatsCommand}</b>: Untuk melihat status bot 🦋
'''
help = Telegraph(access_token=telegraph_token).create_page(
        title='MirrorX Help ⚡️',
        author_name='Ryan wibu pro tzi',
        author_url='https://github.com/SlamDevs/slam-mirrorbot',
        html_content=help_string_telegraph,
    )["path"]

help_string = f'''
/{BotCommands.PingCommand}: Mengecek ping bot 🦋

/{BotCommands.AuthorizeCommand}: Authorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)

/{BotCommands.UnAuthorizeCommand}: Unauthorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)

/{BotCommands.AuthorizedUsersCommand}: List Admin ( hanya owner )

/{BotCommands.AddSudoCommand}: Menambahkan admin ( hanya owner )

/{BotCommands.RmSudoCommand}: Menghapus admin ( hanya owner )

/{BotCommands.RestartCommand}: Merestart bot ( gunakan jika ada kesalahan fatal )

/{BotCommands.LogCommand}: Mendapatkan log bot 🦋

/{BotCommands.SpeedCommand}: Mengecek kekuatan internet stable atau tidak 🦋

/{BotCommands.ShellCommand}: Run commands in Shell (Only Owner)

/{BotCommands.ExecHelpCommand}: Get help for Executor module (Only Owner)

/{BotCommands.TsHelpCommand}: Get help for Torrent search module

🦋 Untuk Selengkapnya klik tombol dibawah 🦋
'''

def bot_help(update, context):
    button = button_build.ButtonMaker()
    button.buildbutton("🦋 Perintah Lainnya 🦋", f"https://telegra.ph/{help}")
    reply_markup = InlineKeyboardMarkup(button.build_menu(1))
    sendMarkup(help_string, context.bot, update, reply_markup)

'''
botcmds = [
        (f'{BotCommands.HelpCommand}','Get Detailed Help'),
        (f'{BotCommands.MirrorCommand}', 'Start Mirroring'),
        (f'{BotCommands.TarMirrorCommand}','Start mirroring and upload as .tar'),
        (f'{BotCommands.ZipMirrorCommand}','Start mirroring and upload as .zip'),
        (f'{BotCommands.UnzipMirrorCommand}','Extract files'),
        (f'{BotCommands.QbMirrorCommand}','Start Mirroring using qBittorrent'),
        (f'{BotCommands.QbTarMirrorCommand}','Start mirroring and upload as .tar using qb'),
        (f'{BotCommands.QbZipMirrorCommand}','Start mirroring and upload as .zip using qb'),
        (f'{BotCommands.QbUnzipMirrorCommand}','Extract files using qBitorrent'),
        (f'{BotCommands.CloneCommand}','Copy file/folder to Drive'),
        (f'{BotCommands.CountCommand}','Count file/folder of Drive link'),
        (f'{BotCommands.DeleteCommand}','Delete file from Drive'),
        (f'{BotCommands.WatchCommand}','Mirror Youtube-dl support link'),
        (f'{BotCommands.TarWatchCommand}','Mirror Youtube playlist link as .tar'),
        (f'{BotCommands.ZipWatchCommand}','Mirror Youtube playlist link as .zip'),
        (f'{BotCommands.CancelMirror}','Cancel a task'),
        (f'{BotCommands.CancelAllCommand}','Cancel all tasks'),
        (f'{BotCommands.ListCommand}','Searches files in Drive'),
        (f'{BotCommands.StatusCommand}','Get Mirror Status message'),
        (f'{BotCommands.StatsCommand}','Bot Usage Stats'),
        (f'{BotCommands.PingCommand}','Ping the Bot'),
        (f'{BotCommands.RestartCommand}','Restart the bot [owner/sudo only]'),
        (f'{BotCommands.LogCommand}','Get the Bot Log [owner/sudo only]'),
        (f'{BotCommands.TsHelpCommand}','Get help for Torrent search module')
    ]
'''

def main():
    fs_utils.start_cleanup()
    if IS_VPS:
        asyncio.get_event_loop().run_until_complete(start_server_async(PORT))
    # Check if the bot is restarting
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        bot.edit_message_text("Berhasil restart tod!", chat_id, msg_id)
        os.remove(".restartmsg")
    elif OWNER_ID:
        try:
            text = "<b>Halo saya online kembali dengan nama : MirrorX ⚡️</b>"
            bot.sendMessage(chat_id=OWNER_ID, text=text, parse_mode=ParseMode.HTML)
            if AUTHORIZED_CHATS:
                for i in AUTHORIZED_CHATS:
                    bot.sendMessage(chat_id=i, text=text, parse_mode=ParseMode.HTML)
        except Exception as e:
            LOGGER.warning(e)
    # bot.set_my_commands(botcmds)
    start_handler = CommandHandler(BotCommands.StartCommand, start, run_async=True)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling(drop_pending_updates=IGNORE_PENDING_REQUESTS)
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)

app.start()
main()
idle()
