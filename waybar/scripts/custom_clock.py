#!/usr/bin/env python3
import json
import datetime
import calendar

def generate_calendar():
    today = datetime.datetime.now()
    cal = calendar.monthcalendar(today.year, today.month)
    
    # Format header with month and year in Vietnamese style
    header = f"Tháng {today.month} Năm {today.year}"
    
    # Create calendar representation using Unicode box-drawing characters
    cal_str = f"┌{'─' * 28}┐\n"
    cal_str += f"│{header:^28}│\n"
    cal_str += f"├{'─' * 28}┤\n"
    cal_str += "│ Hai Ba Tư  Năm  Sáu Bảy CN │\n"
    cal_str += f"├{'─' * 28}┤\n"
    
    for week in cal:
        line = "│"
        for day in week:
            if day == 0:
                line += "    "  # Empty day
            elif day == today.day:
                # Highlight today's date
                line += f" <b><span foreground='#ff9500'>{day:2d}</span></b> "  # Highlight with ANSI color
            else:
                line += f" {day:2d} "
        line += "│\n"
        cal_str += line
    
    cal_str += f"└{'─' * 28}┘"
    return cal_str

def main():
    now = datetime.datetime.now()
    
    # Format time as specified
    # 24h format dd/mm/yyyy
    time_format = now.strftime("%H:%M %d/%m/%Y")
    
    # Generate calendar for tooltip
    tooltip = generate_calendar()
    
    # Create JSON output
    output = {
        "text": time_format,
        "tooltip": tooltip,
        "class": "custom-clock"
    }
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()
