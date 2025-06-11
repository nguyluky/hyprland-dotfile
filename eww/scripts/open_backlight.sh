

# get current backlight brightness percentage use brightnessctl
current_brightness=$(brightnessctl get)
# get max backlight brightness percentage use brightnessctl
max_brightness=$(brightnessctl max)
# calculate the percentage
percentage=$((current_brightness * 100 / max_brightness))
# set eww variable
eww update brightness_level=$percentage

eww open backlight
# start timer to auto close the widget after 5 seconds
python ~/.config/eww/scripts/timer_client.py add backlight 5 "eww close backlight"
