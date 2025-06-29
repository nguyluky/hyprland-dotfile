import os

MONITOR_FILE = "/home/luky/.config/hypr/monitors.conf"
MONITOR_FOLDER = '/home/luky/.config/hypr/monitors_save'
HYPRLAND_MONITOR_CONFIG_KEYWORDS = [
    "name",
    "resolution",
    "position",
    "scale",
    "mirror",
    "bitdepth",
    "cm",
    "transform"
]


class MonitorConfig:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', args[0] if len(args) > 0 else "Wtf")
        self.resolution = kwargs.get('resolution', args[1] if len(args) > 1 else None)
        self.position = kwargs.get('position', args[2] if len(args) > 2 else None)
        self.scale = kwargs.get('scale', args[3] if len(args) > 3 else "1.0")
        self.mirror = kwargs.get('mirror', None)
        self.bitdepth = kwargs.get('bitdepth', None)
        self.cm = kwargs.get('cm', 'auto')
        self.transform = kwargs.get('transform', None)

    def __repr__(self):
        return f"MonitorConfig(name={self.name}, resolution={self.resolution}, position={self.position}, scale={self.scale}, mirror={self.mirror}, bitdepth={self.bitdepth}, cm={self.cm}, transform={self.transform})"

    def merge(self, other):
        if isinstance(other, MonitorConfig):
            self.name = other.name or self.name
            self.resolution = other.resolution or self.resolution
            self.position = other.position or self.position
            self.scale = other.scale or self.scale
            self.mirror = other.mirror or self.mirror
            self.bitdepth = other.bitdepth or self.bitdepth
            self.cm = other.cm or self.cm
            self.transform = other.transform or self.transform

        return self

def read_monitor_config(file_path):
    try:
        with open(os.path.expanduser(file_path), 'r') as file:
            lines = file.readlines()
            config: dict[str, MonitorConfig] = {}
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                key, value= line.split('=', 1)
                values = value.strip().split(',')

                args = []
                kwargs = {}
                keyword  = ''
                for value in values:
                    value = value.strip()
                    if value in HYPRLAND_MONITOR_CONFIG_KEYWORDS:
                        keyword = value
                        continue
                    if keyword:
                        kwargs[keyword] = value
                        keyword = ''
                    else:
                        args.append(value)
                
                monitor_config = MonitorConfig(*args, **kwargs)
                if monitor_config.name in config:
                    config[monitor_config.name].merge(monitor_config)
                else:
                    config[monitor_config.name] = monitor_config

            return list(config.values())
    except FileNotFoundError:
        # print(f"Error: The file {file_path} does not exist.")
        return None
    pass



def config_to_monitor_review_widget_eww(configs, title):
    # get max range of positions and resolutions
    # and scale all monitors to fit in a box 150x150
    # and move them to the center of box

    # 1. Calculate the max/min width and height of all monitors
    min_x = min_y = float('inf')
    max_x = max_y = 0
    for config in configs:
        res_x, res_y = map(int, config.resolution.split("@")[0].split('x'))
        pos_x, pos_y = map(int, config.position.split('x'))
        min_x = min(min_x, pos_x)
        min_y = min(min_y, pos_y)
        max_x = max(max_x, pos_x + res_x)
        max_y = max(max_y, pos_y + res_y)
    
    box_width = max_x - min_x
    box_height = max_y - min_y

    scale_factor = min(100 / box_width, 100 / box_height)
    
    new_configs = []
    min_x = min_y = 150 
    max_x = max_y = 0 
    for config in configs:
        res_x, res_y = map(int, config.resolution.split("@")[0].split('x'))
        pos_x, pos_y = map(int, config.position.split('x'))
        new_res_x = int(res_x * scale_factor)
        new_res_y = int(res_y * scale_factor)
        new_pos_x = int(pos_x * scale_factor)  # Centering in a 150x150 box
        new_pos_y = int(pos_y * scale_factor)  # Centering in a 150x150 box
        
        new_configs.append({
            "name": config.name,
            "resolution": [new_res_x, new_res_y],
            "position": [new_pos_x, new_pos_y],
        })
        
        # find min and max positions
        min_x = min(min_x, new_pos_x)
        min_y = min(min_y, new_pos_y)
        max_x = max(max_x, new_pos_x + new_res_x)
        max_y = max(max_y, new_pos_y + new_res_y)
    
    box_width = max_x - min_x
    box_height = max_y - min_y

    center_x = (150 - box_width ) // 2 - min_x
    center_y = (150 - box_height) // 2 - min_y

    eww_monitor = ''
    for config in new_configs:
        
        name = config['name']
        res_x, res_y = config['resolution']
        pos_x, pos_y = config['position']
        # print(f"Monitor: {name}, Resolution: {res_x}x{res_y}, Position: {pos_x + center_x}x{pos_y + center_y}")
        # print(f"          (monitor-widget :x 63 :y 75 :width 112 :height 63) ")
        # print(f"(monitor-widget :name \"{name}\" :x {pos_x + center_x} :y {pos_y + center_y} :width {res_x} :height {res_y})")
        eww_monitor += f"(monitor-widget :name \"{name}\" :x {pos_x + center_x} :y {pos_y + center_y} :width {res_x} :height {res_y})"
    
    eww = f"""
        (button :class "monitor-review-wrapper"
            :hexpand false
            :vexpand false
            :valign "start"
          (box :class "monitor-review-widget"
            :orientation "h"
            :spacing -80
            (box :class "monitor-review"
              :space-evenly false
              :halign "start"
              (overlay
                :vexpand true
                :hexpand true
                {eww_monitor}
              )
            )
            (box :class "monitor-info"
              (box :class "test-box"
                (label :class "monitor-label"
                  :text "{title}"
                  :halign "start"
                  :wrap true
                )
              )
            )
          )
        )
    """
    return eww

def minify_eww(eww):
    # Remove unnecessary whitespace and newlines
    t1 = ' '.join(eww.split())
    t3 = t1.strip()

    return t3

def escape_eww_string(s):
    # Escape double quotes and backslashes
    return s.replace('\\', '\\\\').replace('"', '\\"')

def test():
    eww = ''
    for file in os.listdir(MONITOR_FOLDER):
        if file.endswith('.conf'):
            # print(f"Reading monitor config from {file}")
            configs = read_monitor_config(os.path.join(MONITOR_FOLDER, file))
            eww += config_to_monitor_review_widget_eww(configs, file.replace('.conf', ''))
        
    eww = f"""
      (box :class "quick-monitor-settings"
    (scroll
      :width "400"
      :vscroll true
      :halign "start"
      (box
        :class "monitor-review-container"
        :orientation "v"
        :spacing 5
        
        {eww}
      )
    )
  )

    """
    eww = minify_eww(eww)
    eww = escape_eww_string(eww)
    
    print(eww)
    
if __name__ == "__main__":
    test()