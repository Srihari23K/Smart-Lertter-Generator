# fix_templates.py
import re

# Path to your template_engine.py
file_path = "engine/template_engine.py"

# Read the file
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Replace {{variable}} with {variable}
# This regex matches {{any_text}} and replaces with {any_text}
fixed_content = re.sub(r'\{\{(.*?)\}\}', r'{\1}', content)

# Write back
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(fixed_content)

print("✅ Templates updated from {{variable}} to {variable}")