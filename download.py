import customtkinter as ctk
from math import floor
from scrollable_customtk import ScrollableFrame
import yt_dlp

RESOLUTION_MAPPING = {
    "2160p (4K)": "2160p", "1440p (HD)": "1440p", "1080p (HD)": "1080p",
    "720p": "720p", "480p": "480p", "360p": "360p", "240p": "240p"
}
FPS_MAPPING = {
    "120 fps": 120, "60 fps": 60, "30 fps": 30, "24 fps": 24
}
PLAYBACK_MAPPING = {
    "0.5x": 0.5, "0.75x": 0.75, "1x": 1, "1.25x": 1.25, "1.5x": 1.5, "1.75x": 1.75, "2x": 2, "2.5x": 2.5, "3x": 3, "3.5x": 3.5, "4x": 4
}
FILE_EXT = {
    ".mp4 (MP4)": "mp4", ".webp (WEBP)": "webp", ".mkv (MKV)": "mkv", ".mov (MOV)": "mov"
}
AUDIO_FILE_EXT = {
    ".mp3 (MP3)": "mp3", ".wav (WAV)": "wav"
}

def set_placeholder(selected):
    mapping = {
        "Youtube": "https://youtube.com",
        "Instagram": "https://instagram.com",
        "Facebook": "https://facebook.com",
        "Reddit": "https://reddit.com",
        "Snapchat": "https://snapchat.com",
        "X": "https://x.com"
    }
    text = mapping.get(selected, "An Error Occurred...")
    url_entry.configure(placeholder_text=text)

current_mode = "Simple"

def toggle_mode():
    global current_mode
    media_type = download_type_var.get()

    if current_mode == "Simple":
        current_mode = "Advanced"
        mode_switch_button.configure(text="Simple")
        
        download_button_simple.grid_forget()
        download_button_advanced.pack(pady=20, padx=16, anchor="w")
        
        if media_type == "Video":
            advanced_audio_frame.grid_forget()
            advanced_video_frame.grid(row=2, column=1, padx=16, pady=16, sticky="nsew")
        else:
            advanced_video_frame.grid_forget()
            advanced_audio_frame.grid(row=2, column=1, padx=16, pady=16, sticky="nsew")
            
    else:
        current_mode = "Simple"
        mode_switch_button.configure(text="Advanced")
        
        advanced_video_frame.grid_forget()
        advanced_audio_frame.grid_forget()
        download_button_advanced.pack_forget()
        download_button_simple.grid(row=2, column=1, sticky="se", padx=20, pady=20)

def toggle_type(selected):
    if current_mode == "Advanced":
        if selected == "Audio":
            advanced_video_frame.grid_forget()
            advanced_audio_frame.grid(row=2, column=1, padx=16, pady=16, sticky="nsew")
        else:
            advanced_audio_frame.grid_forget()
            advanced_video_frame.grid(row=2, column=1, padx=16, pady=16, sticky="nsew")

def download():
    url = str(url_entry.get())

    if url.startswith(("https://")):
        error_label.configure(text="")
        errorframe.grid_remove()

    else:
        error_label.configure(text="Error: Your url must start with 'https://'")
        errorframe.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 0))
        return

    global current_mode, resolution_optionmenu_var

    #For Video
    if download_type_var.get() == "Video":

        #For Simple Mode
        if current_mode == "Simple":
            file_ext = "mp4"
            vid_res = "1080p"
            frame_rate = "30"
            vid_speed = "1"

        #For Advanced Mode
        else:
            file_ext = file_ext_optionmenu_var.get()
            file_ext = str(FILE_EXT.get(file_ext))

            vid_res = RESOLUTION_MAPPING.get(str(resolution_optionmenu_var.get()))

            frame_rate = FPS_MAPPING.get(str(frame_rate_optionmenu_var.get()))

            vid_speed = PLAYBACK_MAPPING.get(str(play_back_speed_optionmenu_var.get()))

    #For Audio
    else:

        #For simple Mode
        if current_mode == "Simple":
            file_ext = "mp3"
            audio_speed = "1"

        #For Advanced Mode
        else:
            file_ext = audio_file_ext_optionmenu_var.get()
            file_ext = str(AUDIO_FILE_EXT.get(file_ext))

            audio_speed = PLAYBACK_MAPPING.get(str(audio_play_backspeed_optionmenu_var.get()))


# ========== UI Setup ==========
root = ctk.CTk()
root.title("Box-Dlp - Download Audio and Video from Youube, Insta and More")

scr_w, scr_h = root.winfo_screenwidth(), root.winfo_screenheight()
win_w, win_h = floor(scr_w * (2/3)), floor(scr_h * (2/3))
scr_center_w = int((scr_w / 2) - (win_w / 2))
scr_center_h = int((scr_h / 2) - (win_h / 2))
root.geometry(f"{win_w}x{win_h}+{scr_center_w}+{scr_center_h}")

# Create a scrollable container and use its inner frame as the content parent
# Do not force any background or corner styling so the existing UI appearance is preserved
container = ScrollableFrame(root, fg_color="#242424", corner_radius=0)
container.pack(fill="both", expand=True)
content_parent = container.inner

# FIXED: Added explicit grid instructions for the error container
errorframe = ctk.CTkFrame(content_parent, height=50, fg_color="#3b2424")
errorframe.grid_propagate(False) 

# FIXED: Reusable static label created once inside the error container
error_label = ctk.CTkLabel(errorframe, text="", font=("Arial", -16, "bold"), text_color="#ff8888")
error_label.pack(expand=True, fill="both", padx=20, pady=5)

content_parent.columnconfigure(0, weight=1)
content_parent.columnconfigure(1, weight=1)
content_parent.rowconfigure(1, weight=0) 
content_parent.rowconfigure(2, weight=1) 

# --- Media Selection ---
select_media_frame = ctk.CTkFrame(content_parent, fg_color="#242424")
select_media_frame.grid(column=0, row=1, sticky="nw", padx=26, pady=20)

select_media_label = ctk.CTkLabel(select_media_frame, text="Select Social Media :", font=("Arial", -22, "bold"))
select_media_label.pack(pady=16)

s_media_options = ["Youtube", "Instagram", "Facebook", "Reddit", "Snapchat", "X"]
s_media_optionmenu_var = ctk.StringVar(value="Social Media  ")
s_media_optionmenu = ctk.CTkOptionMenu(select_media_frame, values=s_media_options, variable=s_media_optionmenu_var, command=set_placeholder)
s_media_optionmenu.pack(fill="x")

# --- Switch Mode ---
switch_mode_frame = ctk.CTkFrame(content_parent, fg_color="#242424")
switch_mode_frame.grid(column=1, row=1, sticky="ne", padx=20, pady=16)

switch_mode_label = ctk.CTkLabel(switch_mode_frame, text="Switch Mode To :", font=("Arial", -22, "bold"))
switch_mode_label.grid(column=0, row=0, padx=16, pady=16, sticky="w")

mode_switch_button = ctk.CTkButton(switch_mode_frame, text="Advanced", font=("Arial", -16, "bold"), width=100, height=36, command=toggle_mode)
mode_switch_button.grid(column=1, row=0, padx=16, pady=16, sticky="e")

# --- Left UI Control Panel ---
left_ui_frame = ctk.CTkFrame(content_parent, fg_color="#242424")
left_ui_frame.grid(column=0, row=2, pady=16, padx=16, sticky="nw")

url_label = ctk.CTkLabel(left_ui_frame, text="Url:", font=("Arial", -22, "bold"))
url_label.pack(pady=(28, 0), padx=16, anchor="w")

url_entry = ctk.CTkEntry(left_ui_frame, placeholder_text="Enter Url", height=30, width=300)
url_entry.pack(pady=16, padx=16, anchor="w")

download_type_label = ctk.CTkLabel(left_ui_frame, text="Download Type :", font=("Arial", -22, "bold"))
download_type_label.pack(pady=(28, 0), padx=16, anchor="w")

download_type_var = ctk.StringVar(value="Video")
download_type_optionmenu = ctk.CTkOptionMenu(left_ui_frame, values=["Video", "Audio"], variable=download_type_var, command=toggle_type)
download_type_optionmenu.pack(padx=16, pady=16, anchor="w")

download_button_advanced = ctk.CTkButton(left_ui_frame, text="Download", font=("Arial", -22, "bold"), height=40, command=download)

download_button_simple = ctk.CTkButton(content_parent, text="Download", font=("Arial", -22, "bold"), height=40, command=download)
download_button_simple.grid(row=2, column=1, sticky="se", padx=20, pady=20)

# --- Advanced Video Settings ---
advanced_video_frame = ctk.CTkFrame(content_parent, fg_color="#535260")
advanced_video_frame.columnconfigure(1, weight=1)

resolution_label = ctk.CTkLabel(advanced_video_frame, text="Resolution :", font=("Arial", -22))
resolution_label.grid(column=0, row=0, pady=(28, 0), padx=22, sticky="w")

resolution_optionmenu_var = ctk.StringVar(value="1080p (HD)")
resolution_optionmenu = ctk.CTkOptionMenu(advanced_video_frame, values=list(RESOLUTION_MAPPING.keys()), variable=resolution_optionmenu_var)
resolution_optionmenu.grid(column=1, row=0, pady=(28, 0), padx=16, sticky="ew")

frame_rate_label = ctk.CTkLabel(advanced_video_frame, text="Frame Rate :", font=("Arial", -22))
frame_rate_label.grid(column=0, row=2, pady=(28, 0), padx=22, sticky="w")

frame_rate_optionmenu_var = ctk.StringVar(value="30 fps")
frame_rate_optionmenu = ctk.CTkOptionMenu(advanced_video_frame, values=list(FPS_MAPPING.keys()), variable=frame_rate_optionmenu_var)
frame_rate_optionmenu.grid(column=1, row=2, pady=(28, 0), padx=16, sticky="ew")

play_back_speed_label = ctk.CTkLabel(advanced_video_frame, text="Playback Speed :", font=("Arial", -22))
play_back_speed_label.grid(column=0, row=4, pady=28, padx=22, sticky="w")

play_back_speed_optionmenu_var = ctk.StringVar(value="1x")
play_back_speed_optionmenu = ctk.CTkOptionMenu(advanced_video_frame, values=list(PLAYBACK_MAPPING.keys()), variable=play_back_speed_optionmenu_var)
play_back_speed_optionmenu.grid(column=1, row=4, pady=28, padx=16, sticky="ew")

file_ext_label = ctk.CTkLabel(advanced_video_frame, text="File Extension :", font=("Arial", -22))
file_ext_label.grid(column=0, row=5, padx=22, sticky="w")

file_ext_optionmenu_var = ctk.StringVar(value=".mp4 (MP4)")
file_ext_optionmenu = ctk.CTkOptionMenu(advanced_video_frame, values=list(FILE_EXT.keys()), variable=file_ext_optionmenu_var)
file_ext_optionmenu.grid(column=1, row=5, padx=16, sticky="ew")

# --- Advanced Audio Settings ---
advanced_audio_frame = ctk.CTkFrame(content_parent, fg_color="#535260")
advanced_audio_frame.columnconfigure(1, weight=1)

audio_file_ext_label = ctk.CTkLabel(advanced_audio_frame, text="File Extension :", font=("Arial", -22))
audio_file_ext_label.grid(column=0, row=0, pady=(28, 0), padx=22, sticky="w")

audio_file_ext_optionmenu_var = ctk.StringVar(value=".mp3 (MP3)")
audio_file_ext_optionmenu = ctk.CTkOptionMenu(advanced_audio_frame, values=list(AUDIO_FILE_EXT.keys()), variable=audio_file_ext_optionmenu_var)
audio_file_ext_optionmenu.grid(column=1, row=0, pady=(28, 0), padx=16, sticky="ew")

audio_playback_speed_label = ctk.CTkLabel(advanced_audio_frame, text="Playback Speed :", font=("Arial", -22))
audio_playback_speed_label.grid(column=0, row=2, pady=28, padx=22, sticky="w")

audio_play_backspeed_optionmenu_var = ctk.StringVar(value="1x")
audio_playback_speed_optionmenu = ctk.CTkOptionMenu(advanced_audio_frame, values=list(PLAYBACK_MAPPING.keys()), variable=audio_play_backspeed_optionmenu_var)
audio_playback_speed_optionmenu.grid(column=1, row=2, pady=28, padx=16, sticky="ew")

root.mainloop() 