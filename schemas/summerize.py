from . import Language
from pydantic import BaseModel, Field


class SummerizeRequest(BaseModel):
    text: str = Field(
        ...,
        description="The text content you want to summarize.",
        example="האסטרונאוטים במשימת אפולו 11 היו ניל ארמסטרונג, באז אולדרין ומייקל קולינס. מטרתם הייתה לנחות על הירח ולהחזיר דגימות לכדור הארץ."
    )
    src_lang: Language = Field(
        default=Language.HEBREW,
        description="The source language of the text."
    )
    tgt_lang: Language = Field(
        default=Language.HEBREW,
        description="The desired target language for the summary."
    )
    temperature: float = Field(
        default=0.6,
        ge=0.2,
        le=1.0,
        description="Controls randomness. Lower values are more deterministic.",
        example=0.7
    )
    top_p: float = Field(
        default=0.9,
        ge=0.7,
        le=1.0,
        description="Controls nucleus sampling. Considers tokens with top_p probability mass.",
        example=0.9
    )
    max_tokens: int = Field(
        default=512,
        gt=0,
        description="The maximum number of tokens to generate in the summary.",
        example=256
    )
