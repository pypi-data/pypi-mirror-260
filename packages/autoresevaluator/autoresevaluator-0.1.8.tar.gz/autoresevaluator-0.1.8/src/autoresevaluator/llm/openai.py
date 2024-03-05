from openai import OpenAI

client = OpenAI()

def _openai_model(prompt):
    response = client.chat.completions.create(
            model='gpt-4-turbo-preview',
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            seed=3655
            )

    return response.choices[0].message.content
