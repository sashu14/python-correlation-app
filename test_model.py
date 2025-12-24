"""
Quick test script to demonstrate how to use the Gemma3:1b model.
"""
import ollama
from agents.text_agent import analyze_text
from agents.image_agent import analyze_image

# Example 1: Direct Ollama usage
print("=" * 60)
print("Example 1: Direct Ollama Chat")
print("=" * 60)

response = ollama.chat(
    model="gemma3:1b",
    messages=[
        {
            "role": "user",
            "content": "Analyze this text: 'Looking for some 🔥 stuff, DM me 💊'"
        }
    ]
)
print(response["message"]["content"])
print("\n")

# Example 2: Using the text agent (with emoji and slang detection)
print("=" * 60)
print("Example 2: Using Text Agent (Enhanced)")
print("=" * 60)

test_text = "Looking for some 🔥 stuff, DM me 💊💰"
result = analyze_text(test_text)
print(result)
print("\n")

# Example 3: Test with different types of content
print("=" * 60)
print("Example 3: Testing Various Content Types")
print("=" * 60)

test_cases = [
    "Selling premium quality 💊 contact me",
    "Need help with prescription meds",
    "🔥🔥🔥 Best prices DM for menu 💰",
    "Just sharing my recovery journey"
]

for i, text in enumerate(test_cases, 1):
    print(f"\nTest Case {i}: {text}")
    print("-" * 40)
    result = analyze_text(text)
    print(result[:200] + "..." if len(result) > 200 else result)

