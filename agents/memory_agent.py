import os
from datetime import datetime

MEMORY_FOLDER = "memory"

def save_daily_memory(content):

    if not os.path.exists(MEMORY_FOLDER):
        os.makedirs(MEMORY_FOLDER)

    today = datetime.now().strftime("%Y-%m-%d")

    filename = f"{MEMORY_FOLDER}/{today}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"🧠 Memory saved: {filename}")

def load_recent_memories(days=3):

    if not os.path.exists(MEMORY_FOLDER):
        return ""

    files = sorted(os.listdir(MEMORY_FOLDER), reverse=True)

    recent_files = files[:days]

    memory_content = ""

    for file in recent_files:

        path = os.path.join(MEMORY_FOLDER, file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                memory_content += f"\n\n===== MEMORY: {file} =====\n\n"
                memory_content += f.read()

        except:
            continue

    return memory_content