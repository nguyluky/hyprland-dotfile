#!/usr/bin/env python3
import argparse
import sys
import json
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--player')
    return parser.parse_args()

def get_players():
    output = subprocess.getoutput('playerctl --list-all 2>/dev/null')
    if not output:
        return []
    return output.split('\n')

def get_status(player):
    return subprocess.getoutput(f'playerctl --player={player} status 2>/dev/null')

def get_metadata(player, key):
    output = subprocess.getoutput(f'playerctl --player={player} metadata {key} 2>/dev/null')
    return output if output else "Unknown"

def main():
    args = parse_arguments()
    
    if args.player:
        players = [args.player]
    else:
        players = get_players()
        
    if not players:
        print(json.dumps({"text": "", "class": "custom-media"}))
        sys.exit(0)
    
    for player in players:
        status = get_status(player)
        if status == 'Playing':
            artist = get_metadata(player, 'artist')
            title = get_metadata(player, 'title')
            if artist == "Unknown" and title == "Unknown":
                text = "Playing"
            else:
                text = f"{artist} - {title}"
                if len(text) > 30:
                    text = text[:27] + "..."
            
            result = {
                "text": text,
                "class": "custom-media",
                "alt": player,
                "tooltip": f"{artist} - {title}",
            }
            print(json.dumps(result))
            sys.exit(0)
    
    print(json.dumps({"text": "", "class": "custom-media"}))

if __name__ == "__main__":
    main()
