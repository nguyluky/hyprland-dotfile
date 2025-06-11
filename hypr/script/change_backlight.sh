

case $1 in 
    "increase")
        brightnessctl set +5%
        ;;
    "decrease")
        CUR=$(brightnessctl | grep -oP '\(\K[0-9]+(?=%\))')

        # Nếu lớn hơn MIN thì mới giảm
        if [ "$CUR" -gt "5" ]; then
            brightnessctl set 5%-
        else
            exit 0
        fi
        ;;
    "*")
        # do nothing
        exit 0
        ;;
esac
# open the backlight widget

widget_open=$(eww active-windows | grep backlight | wc -l)
if [ "$widget_open" -eq 0 ]; then
    # run the script to update the backlight percentage and open the widget
    #     ~/.config/eww/scripts/open_backlight.sh
    bash ~/.config/eww/scripts/open_backlight.sh
else
    # update the backlight percentage
    current_brightness=$(brightnessctl get)
    # get max backlight brightness percentage use brightnessctl
    max_brightness=$(brightnessctl max)
    # calculate the percentage
    percentage=$((current_brightness * 100 / max_brightness))
    # set eww variable
    eww update brightness_level=$percentage
fi