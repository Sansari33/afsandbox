import os

ROOT_DIR = os.getcwd()

for subdir, _, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(subdir, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            changes = []
            if "import openai" in content:
                changes.append("Replace 'import openai' with tracked_chat_completion import")
            if "openai.ChatCompletion.create" in content:
                changes.append("Replace 'openai.ChatCompletion.create' with 'tracked_chat_completion'")

            if changes:
                print(f"--- {file_path} ---")
                for change in changes:
                    print(f"   • {change}")

print("✅ Test mode complete — review above changes before running the live update script.")
