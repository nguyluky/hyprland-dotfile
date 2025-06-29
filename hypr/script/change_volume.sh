

case $1 in 
    "increase")
        wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+
        ;;
    "decrease")
        wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
        ;;
    "toggle")
        wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
        ;;
    "*")
        # do nothing
        exit 0
        ;;
esac



CUR=$(pactl get-sink-volume @DEFAULT_SINK@ | grep -o '[0-9]\+%' | head -1)
eww update volume_level=${CUR%?}

widget_open=$(eww active-windows | grep volume-control | wc -l)
if [ "$widget_open" -eq 0 ]; then
    eww open volume-control
    # start timer to auto close the widget after 5 seconds
    python ~/.config/eww/scripts/timer_client.py add volume-control 5 "eww close volume-control"
else
    python ~/.config/eww/scripts/timer_client.py set volume-control 5
fi
