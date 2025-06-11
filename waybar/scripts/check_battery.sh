#!/bin/bash

# Get battery percentage
battery_percent=$(cat /sys/class/power_supply/BAT*/capacity 2>/dev/null)
battery_status=$(cat /sys/class/power_supply/BAT*/status 2>/dev/null)

# Check if battery exists and is discharging
if [[ -n "$battery_percent" && "$battery_status" == "Discharging" ]]; then
    # Critical level with notification
    if (( battery_percent <= 10 )); then
        notify-send -u critical "Battery Critical" "Battery at $battery_percent%! Connect charger now."
    # Low level with notification
    elif (( battery_percent <= 20 )); then
        notify-send -u normal "Battery Low" "Battery at $battery_percent%. Please connect charger."
    fi
fi