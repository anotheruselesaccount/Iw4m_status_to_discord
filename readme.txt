# Iw4m api to discord status bot made with discord.py

In this example config.json bot seach all possible game servers every minute and send status message to discord channel.

Example config.json

{
    "discord_bot_token": "HTfsvbsdgh4bvffRBs.rheb.gjnetjetj5mhmt5k",
    "iw4m_webfront_url": "192.123.123.1:1234",
    "discord_channel_id": "23523428907523509",
    "refresh_time_in_minutes": "1",
    "game": ""
    "show_players": "true"
}


Get your iw4m_webfront_url by setting up iw4m at https://raidmax.org/IW4MAdmin/.

You can get your discord_bot_token from https://discord.com/developers/applications.

Here is few examples of available game options "", "ALL", "T4", "T5", "T6", "T7", "IW5".

You can get discord_channel_id by right clicking discord channel and selecting copy channel id.

"show_players" options are "true", "false" or "" 

############################################################################################################################

If you are not using prebuild exe file for the bot you do need to install python and the requirements for the bot to work.

Get python from https://www.python.org/downloads/.

Install requirements after installing python by double clicking install_requirements.bat

############################################################################################################################

Compile your own executable file with pyinstaller. First install with pip install pyinstaller

pyinstaller --noconfirm --onefile basic_iw4m_api_status.py
