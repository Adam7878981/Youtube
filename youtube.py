import telebot
import yt_dlp
import os

# Replace this with your bot token from BotFather
BOT_TOKEN = "7056737675:AAFkr1uyUUlUSJKMtSRXiWOlayvKq31vXRc"

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Start/Help command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a YouTube URL, and I'll download the video for you.")

# Handle messages (YouTube URLs)
@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "Please send a valid YouTube URL.")
        return

    bot.reply_to(message, "Processing your request. Please wait...")

    try:
        # Set up yt-dlp options
        ydl_opts = {
            'format': 'best[ext=mp4]',  # Download the best available MP4 video
            'outtmpl': '%(title)s.%(ext)s',  # Output filename template
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the video and get the file name
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        # Send the video file to the user
        with open(file_name, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file)

        # Remove the file after sending it
        os.remove(file_name)

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Start polling for updates
print("Bot is running...")
bot.polling()