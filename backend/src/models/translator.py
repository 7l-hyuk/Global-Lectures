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
        logger.info("translation")
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

    def process(self, segments: list[dict[str, Any]], model: str = 'gpt-3.5-turbo'):
        sentences = [sub["text"] for sub in segments]
        logger.info(f"TRANSLATION: {self.language[0]} -> {self.language[1]}")
        combined_text = '\n'.join(f"- {sentence}" for sentence in sentences)
        prompt = (
            f"You are a professional translator. Carefully consider the meaning and natural usage of the following sentences in full context. "
            f"Silently correct any unnatural or awkward expressions if necessary, "
            f"and translate them naturally and idiomatically from {self.language[0]} to {self.language[1]}. "
            f"Respond only with the translated sentences in list form, preserving order, and give no additional explanation.\n\n"
            f"{combined_text}\n\nTranslations:"
        )
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        translations = response.choices[0].message.content.strip().split('\n')
        translations = [line.lstrip('- ').strip() for line in translations if line.startswith('-')]
        print(translations)

        for i, segment in enumerate(segments):
            print(segment["text"])
            print(translations[i])
            segment["text"] = translations[i]
        print(segments)
