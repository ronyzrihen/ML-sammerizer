from pydantic import BaseModel, Field
from . import Language


class TranslateRequest(BaseModel):
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
