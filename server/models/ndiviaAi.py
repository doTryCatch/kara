api_key = "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"
from openai import OpenAI

client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)

completion = client.chat.completions.create(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    messages=[
        {
            "role": "user",
            "content": "Write a limerick about the wonders of GPU computing.",
        }
    ],
    temperature=0.5,
    top_p=1,
    max_tokens=1024,
    stream=True,
)

for chunk in completion:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
