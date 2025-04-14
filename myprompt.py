from openai import OpenAI
import json
import os


rule_template = """
Generate a *single, coherent sentence* (between 50–100 characters) describing a video scene with a logical contradiction. Follow this structure:

1. Start with a normal, realistic setting (e.g., "A candle burns on a desk").
2. Introduce a logical action (e.g., "its flame flickers gently").
3. Add a clear contradiction (e.g., "yet the candle grows longer").
4. (Optional) End with a surprising or poetic twist (e.g., "brightening the room").

Example output:  
"A candle burns, its flame flickers, yet it grows longer, brightening the room."

- Keep it *vivid and concise* (50–100 characters).  
- Ensure the contradiction is *clear, unexpected, and abrupt*.  
- Use *simple, evocative language* for visual impact.  
"""



def generate_contradictions(n=5):
    responses = []

    for i in range(n):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are a creative writer who specializes in creating attention-grabbing scenes with logical contradictions."},
                {"role": "user",
                 "content": f"{rule_template}\n\nGenerate a new contradiction scene following these rules. Keep the total text under 50 characters."}
            ],
            temperature=1.2  # Slightly higher temperature for more creative outputs
        )

        scene = response.choices[0].message.content.strip()
        responses.append({
            "id": i + 1,
            "scene": scene,
            "length": len(scene)
        })

        print(f"Generated scene {i + 1}: {scene}")

    return responses


def append_to_json(new_data, filename="contradictions.json"):
    # 尝试读取现有文件
    existing_data = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)

    # 确定新条目的ID（从现有最大ID+1开始）
    start_id = max([item['id'] for item in existing_data], default=0) + 1

    # 更新新条目的ID
    for i, item in enumerate(new_data):
        item['id'] = start_id + i

    # 合并数据
    combined_data = existing_data + new_data

    # 保存回文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully appended {len(new_data)} contradictions to {filename}")


if __name__ == "__main__":
    # Generate 10 contradiction scenes (you can change this number)
    n = 3
    contradictions = generate_contradictions(n)

    # Append to JSON file
    append_to_json(contradictions)