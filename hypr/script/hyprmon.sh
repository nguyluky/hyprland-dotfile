#!/bin/bash

# Thư mục chứa các bản sao lưu cấu hình màn hình
SAVE_DIR="$HOME/.config/hypr/monitors"
MAIN_CONF="$HOME/.config/hypr/monitors.conf"

# Đảm bảo thư mục tồn tại
mkdir -p "$SAVE_DIR"

function usage() {
    echo "Usage:"
    echo "  hyprmon save <name>    - Lưu cấu hình hiện tại với tên <name>"
    echo "  hyprmon load <name>    - Tải cấu hình <name> vào monitors.conf"
    echo "  hyprmon remove <name>  - Xoá cấu hình <name>"
    echo "  hyprmon list           - Liệt kê các cấu hình đã lưu"
    exit 1
}

case "$1" in
    save)
        [[ -z "$2" ]] && usage
        cp "$MAIN_CONF" "$SAVE_DIR/$2.conf"
        echo "✅ Đã lưu cấu hình hiện tại thành '$2.conf'"
        ;;
    load)
        [[ -z "$2" ]] && usage
        if [[ -f "$SAVE_DIR/$2.conf" ]]; then
            cp "$SAVE_DIR/$2.conf" "$MAIN_CONF"
            echo "✅ Đã tải cấu hình '$2.conf' vào monitors.conf"
        else
            echo "❌ Không tìm thấy cấu hình '$2.conf'"
            exit 2
        fi
        ;;
    remove)
        [[ -z "$2" ]] && usage
        if [[ -f "$SAVE_DIR/$2.conf" ]]; then
            rm "$SAVE_DIR/$2.conf"
            echo "🗑️ Đã xoá cấu hình '$2.conf'"
        else
            echo "❌ Không tìm thấy cấu hình '$2.conf'"
            exit 2
        fi
        ;;
    list)
        echo "📂 Danh sách các cấu hình đã lưu:"
        ls "$SAVE_DIR" | sed 's/\.conf$//'
        ;;
    *)
        usage
        ;;
esac

