import os
import json

def get_game_data(root_dir, base_url):
    games = []
    
    # Iterate through immediate subdirectories of the root directory
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        
        # Ignore files, hidden directories, and the pagesort directory
        if not os.path.isdir(item_path) or item.startswith('.') or item == 'pagesort':
            continue
            
        index_path = os.path.join(item_path, 'index.html')
        
        if os.path.exists(index_path):
            # Case 1: Folder contains index.html
            games.append({
                "name": item,
                "desc": "",
                "link": f"{base_url.rstrip('/')}/{item}/index.html",
                "img": "",
                "type": "online"
            })
        else:
            # Case 2: Folder does not contain index.html, scan for other .html files
            for file in os.listdir(item_path):
                if file.endswith('.html') and not file.startswith('.'):
                    game_name = os.path.splitext(file)[0]
                    games.append({
                        "name": game_name,
                        "desc": "",
                        "link": f"{base_url.rstrip('/')}/{item}/{file}",
                        "img": "",
                        "type": "online"
                    })
    return games

def main():
    root_dir = input("Enter the path to the root directory (Leave blank for current dir): ").strip()
    if not root_dir:
        root_dir = "."
        
    root_base_url = input("Enter the base URL for root/game.json: ").strip()
    netlify_base_url = input("Enter the base URL for root/netlify/game.json: ").strip()
    
    # Generate identical structures with unique base URLs
    root_games = get_game_data(root_dir, root_base_url)
    netlify_games = get_game_data(root_dir, netlify_base_url)
    
    # Ensure netlify target folder exists
    netlify_dir = os.path.join(root_dir, 'netlify')
    os.makedirs(netlify_dir, exist_ok=True)
    
    # Write files
    with open(os.path.join(root_dir, 'game.json'), 'w', encoding='utf-8') as f:
        json.dump(root_games, f, indent=4)
        
    with open(os.path.join(netlify_dir, 'game.json'), 'w', encoding='utf-8') as f:
        json.dump(netlify_games, f, indent=4)
        
    print("\nFiles successfully created!")

if __name__ == '__main__':
    main()
