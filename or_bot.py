import os                                      
import telebot                                 
import time         
import yt_dlp                           
from telebot.types import InlineKeyboardMarkup , InlineKeyboardButton , ReplyKeyboardMarkup , KeyboardButton
from helpers.check import is_youtube_url , get_thumbnail_url

BOT_TOKEN = "7149742875:AAGU1ualqVIM7WIduOcdpjoDlsttyHV8AOA"
bot = telebot.TeleBot(BOT_TOKEN)

ydl_opts = {
    'listformats': True
}

Down_potion_url = ""
Down_title = ""

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
        #bot.reply_to(message, "Howdy, how are you doing?")

        bot.send_message(message.chat.id,"Work Manual")



@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    text = message.text
    chat_id = message.chat.id
    global Down_potion_url
    bot.delete_message(chat_id,message.message_id)
    video_id = is_youtube_url(text)

    if video_id:
        #bot.send_message(message.chat.id,"This is a valid youtube link")

        Down_potion_url = text 
        listing_qualities(text,message.chat.id,get_thumbnail_url(video_id))


    else:
        #bot.send_message(message.chat.id,"This is a valid youtube link")
        bot.send_message(message.chat.id,'Please Provide a valid youtube link')
        Down_potion_url = ""


    



    # fname = "*" + message.from_user.first_name + " " + message.from_user.last_name + "*"

    # bot.send_message(message.chat.id,f'{fname} : " {message.text} "',parse_mode="MarkDown" )

    #bot.reply_to(message,"Bot start Loop now!")

    # chat_id = message.chat.id
    # text = message.text

    # if text == "loop":
    #     for i in range(11):
    #         #txt = "*" * (i*10)
    #         send_and_delete(chat_id,"space x")
    #         time.sleep(1)

    # elif text == "bg":
    #     img_url = ""

    #     bot.send_photo(chat_id,img_url,caption="This Image from URL")

    # elif text == "Option 1":
    #     bot.send_message(chat_id,"You have steal a lemon!")


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id  = call.message.chat.id
    global Down_potion_url
    global Down_title
    if Down_potion_url != "":
        bot.send_message(chat_id,"Video is Downloading 🌠")
        download_video(call.data,Down_title,Down_potion_url)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        time.sleep(5)

        # Define the path to the video file
        current_directory = os.getcwd()  # Gets the current working directory
        video_path = os.path.join(current_directory, Down_title)

        print(f"Attempting to send video from path: {video_path}")

        try:
            # Check if the file exists before trying to open it
            if os.path.exists(video_path):
                with open(video_path, 'rb') as video_file:
                    bot.send_video(chat_id, video=video_file)
                bot.send_message(chat_id, "Video sent successfully!")
            else:
                bot.send_message(chat_id, "The video file was not found.")
                
        except FileNotFoundError:
            bot.send_message(chat_id, "The video file was not found.")
        except Exception as e:
            # Send detailed error information for debugging
            bot.send_message(chat_id, f"Something went wrong: {str(e)}")
            print(f"Error: {e}")

        
        time.sleep(4)
        if os.path.exists(Down_title):
            try:
                os.remove(Down_title)
                bot.send_message(chat_id,"file removed successfully")
            except Exception as e:
                bot.send_message(chat_id,"an error occured while deleting file")

        else:
            bot.send_message(chat_id,"file not exists")

        
        time.sleep(5)
        Down_potion_url = ""
        Down_title = ""
        
    else:
        Down_potion_url = ""
        bot.send_message(chat_id,"zero")
    # if call.data == "btn1":
    #     for i in range(11):

    #         bot.answer_callback_query(call.id,f"You pressed button {i}")
    # elif call.data == "btn2":
    #     bot.answer_callback_query(call.id,"You pressed button 2")


    # bot.send_message(call.message.chat.id,f"You Pressed {call.data}!")




def listing_qualities(url,chat_id,thumbnail_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        tile =  info_dict.get("title","No Title Found")
        title = tile.replace(" ","_") + ".mp4"
        global Down_title
        Down_title = title

        formats = info_dict.get("formats", [])

        # Filter formats with mp4 extension
        mp4_formats = [f for f in formats if f['ext'] == "mp4"]

        # Desired resolutions
        desired_resolutions = {
            '360p': (640, 338),
            '480p': (854, 450),
            '720p': (1280, 676),
            '1080p60': (1920, 1080)  # Assuming 1080p60 is listed as 1920x1080
        }

        # Dictionary to keep track of the best format for each resolution based on file size
        best_formats = {}

        # Iterate through the formats to find the best one for each resolution based on file size
        for idx, format in enumerate(mp4_formats):
            width = format.get('width', None)
            height = format.get('height', None)
            file_size = format.get("filesize", None)

            if width is not None and height is not None and file_size is not None:
                # Check if width and height match any of the desired resolutions
                resolution_str = [k for k, v in desired_resolutions.items() if v == (width, height)]
                resolution_str = resolution_str[0] if resolution_str else None

                if resolution_str:
                    # Check if file_size is a number
                    try:
                        file_size = float(file_size)
                    except (TypeError, ValueError):
                        file_size = None

                    if file_size is not None:
                        # If the resolution is already in the dictionary, compare file sizes
                        if resolution_str in best_formats:
                            current_best = best_formats[resolution_str]
                            if file_size > current_best['filesize']:
                                best_formats[resolution_str] = {
                                    'format_id': format['format_id'],
                                    'filesize': file_size
                                }
                        else:
                            best_formats[resolution_str] = {
                                'format_id': format['format_id'],
                                'filesize': file_size
                            }

        # Print the selected formats with the largest file size for each resolution
        print("\nAvailable MP4 formats based on file size:")
        resolution_list = list(best_formats.keys())
        mark_up = InlineKeyboardMarkup()
        for idx, resolution in enumerate(resolution_list):
            print(resolution_list)
            format_info = best_formats[resolution]
            btn = InlineKeyboardButton(f"{resolution} |🐱‍👤| {format_info['filesize'] / (1024 * 1024):.2f} MB",callback_data=format_info['format_id'])
            mark_up.add(btn)
            print(f"{idx + 1}. Resolution: {resolution}, Format ID: {format_info['format_id']}, Size: {format_info['filesize'] / (1024 * 1024):.2f} MB")

        bot.send_photo(chat_id,photo=thumbnail_url)
        bot.send_message(chat_id,tile,reply_markup=mark_up)

     

def download_video(selected_format_id,title,url):
    download_opts = {
                'format': selected_format_id,
                'outtmpl': title,
                'merge_output_format': 'mp4',  # Ensure merging into MP4 if needed
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',  # Convert to MP4 format if needed
                    'preferedformat': 'mp4'
                }]
            }
    
    with yt_dlp.YoutubeDL(download_opts) as ydl:
        ydl.download([url])


bot.infinity_polling()


