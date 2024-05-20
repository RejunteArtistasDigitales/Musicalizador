import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters
from pydub import AudioSegment

# Define the folder where audio files will be saved
MUSIC_FOLDER = "music"
os.makedirs(MUSIC_FOLDER, exist_ok=True)

# Function to handle audio messages
async def handle_audio(update: Update, context: CallbackContext) -> None:
    audio_file = await update.message.audio.get_file()

    original_file_name = audio_file.file_path.split('/')[-1]
    original_file_path = os.path.join(MUSIC_FOLDER, original_file_name)
    await audio_file.download_to_drive(original_file_path)

    # Check the audio format and convert to MP3 if necessary
    if not original_file_name.lower().endswith('.mp3'):
        audio = AudioSegment.from_file(original_file_path)
        mp3_file_name = os.path.splitext(original_file_name)[0] + '.mp3'
        mp3_file_path = os.path.join(MUSIC_FOLDER, mp3_file_name)
        audio.export(mp3_file_path, format='mp3')
        os.remove(original_file_path)  # Remove the original file after conversion
    else:
        mp3_file_path = original_file_path

    with open("playlist.txt", 'a') as f:
        f.write(mp3_file_path + " NEW_SONG\n")
        
    print(f"✅ Nuevo audio cargado a la playlist, {mp3_file_path}")
    await update.message.reply_text("✅ Audio cargado a la playlist")

# Function to handle non-audio messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Qué haces que no me estas mandando canciones nuevas?")

# Function to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hola! Mandame una canción y la sumo a la playlist.")


def main() -> None:
    application = Application.builder().token("6719756200:AAHZOmXj5RS_vun8u93eoIUQtQti64j3bdE").build()

    
    # Command handler for the /start command
    application.add_handler(CommandHandler("start", start))
    
    # Message handler for audio messages
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    
    # Message handler for non-audio messages
    application.add_handler(MessageHandler(~filters.AUDIO, handle_message))
    
    # Start the bot
    application.run_polling()
    
    # Run the bot until you press Ctrl+C
    application.idle()

# curl "https://api.telegram.org/bot6719756200:AAHZOmXj5RS_vun8u93eoIUQtQti64j3bdE/setWebhook?url=https://d40e-152-171-11-88.ngrok-free.app"

if __name__ == "__main__":
    main()
