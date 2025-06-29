#!/bin/bash

# Thư mục chứa các cấu hình màn hình đã lưu
SAVE_DIR="$HOME/.config/hypr/monitors"
MAIN_CONF="$HOME/.config/hypr/monitors.conf"

# Kiểm tra xem rofi có được cài chưa
if ! command -v rofi &> /dev/null; then
    echo "❌ Rofi chưa được cài đặt."
    exit 1
fi

# Kiểm tra thư mục lưu config
if [ ! -d "$SAVE_DIR" ]; then
    echo "❌ Không tìm thấy thư mục lưu cấu hình: $SAVE_DIR"
    exit 1
fi

# Danh sách file cấu hình đã lưu (bỏ đuôi .conf)
configs=($(ls "$SAVE_DIR" 2>/dev/null | grep '\.conf$' | sed 's/\.conf$//'))

if [ ${#configs[@]} -eq 0 ]; then
    echo "⚠️ Không có cấu hình nào được lưu trong $SAVE_DIR"
    exit 0
fi

# Dùng rofi để chọn
chosen=$(printf "%s\n" "${configs[@]}" | rofi -dmenu -p "Conf:")

# Nếu người dùng không chọn gì thì thoát
[[ -z "$chosen" ]] && exit 0

# Kiểm tra file tồn tại
config_file="$SAVE_DIR/$chosen.conf"
if [ -f "$config_file" ]; then
    cp "$config_file" "$MAIN_CONF"
    echo "✅ Đã áp dụng cấu hình '$chosen.conf'"
    # Reload Hyprland nếu cần
    hyprctl reload
else
    echo "❌ Không tìm thấy file: $config_file"
    exit 1
fi

