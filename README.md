Clipboard manager using rofi.

remade version of Sergey Kurikalov's rofi-clipboard-manager, regaining functionality for python3 on linux mint. 

TEXT ONLY, images do not function. 


run this on startup to summon the daemon (Ie. in the .config/i3/config for i3wm):
set $clip /path/to/clip/clip.py
$clip daemon &



Use this to set a hotkey to open clipboard with rofi menu, and place selection in keyboard:

set $clip /path/to/clip/clip.py #if not previously used in setting up the daemon
bindsym $mod+shift+v exec rofi -modi "clipboard:$clip menu" -show clipboard && $clip paste
exec --no-startup-id $clip daemon &