from services.config.workout_config import PROMPT


class LLMCoach:
    def __init__(self, groq_client):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT

    def give_feedback(self, event, issue):
        prompt = f"Event: {event}"

        if issue:
            prompt += f" Form Issue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:],
            {"role": "user", "content": prompt}
        ]

        models_to_try = [
            "openai/gpt-oss-20b",
            "llama-3.3-70b-versatile",
            "llama3-8b-8192",
            "qwen/qwen3.8-27b"
        ]

        for m in models_to_try:
            try:
                response = self.client.chat.completions.create(
                    model=m,
                    messages=messages,
                    temperature=0.4,
                )
                text = response.choices[0].message.content.strip()
                if text:
                    self.history.append({"role": "assistant", "content": text})
                    return text
            except Exception as e:
                continue

        return None