from typing import Any

from transformers import pipeline
from openai import OpenAI

from src.models.basemodel import BaseServiceModel
from src.models.registry import register_service
from src.utils.logger import logger
from src.config import service_settings


@register_service("translator")
class TranslationServiceModel(BaseServiceModel):
    def init_model(self):
        self.model = pipeline(
            task="translation",
            model="facebook/nllb-200-distilled-600M",
            src_lang=self.language[0],
            tgt_lang=self.language[1],
            max_length=512
        )

    def process(self, segments: list[dict[str, Any]]):
        for segment in segments:
            logger.info(segment["text"])
            segment["text"] = self.model(
                segment["text"],
                max_length=512
            )[0]["translation_text"]
            logger.info(segment["text"])


@register_service("translator-gpt")
class GptTranslationServiceModel(BaseServiceModel):
    def init_model(self):
        self.client = OpenAI(api_key=service_settings.GPT_API_KEY)

    def process(self, segments: list[dict[str, Any]]):
        sentences = [sub["text"] for sub in segments]
        combined_text = '\n'.join(f"- {sentence}" for sentence in sentences)
        prompt = (
            f"You are a professional translator. Consider the overall context of the following sentences, "
            f"silently correct any awkward or unnatural expressions based on that context, "
            f"then translate the corrected sentences directly from {self.language[0]} to {self.language[1]}. "
            f"Respond only with the final translated sentences as a list, preserving the original order, and no additional explanation:\n\n"
            f"{combined_text}\n\nTranslations:"
        )
        response = self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        translations = response.choices[0].message.content.strip().split('\n')
        translations = [line.lstrip('- ').strip() for line in translations if line.startswith('-')]
        
        for i, segment in enumerate(segments):
            segment["text"] = translations[i]
        print(segments)
