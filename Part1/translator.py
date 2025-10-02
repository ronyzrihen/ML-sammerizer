from transformers import pipeline

class Translator:
    def __init__(self):
        self.pipe = pipeline("translation", model="facebook/nllb-200-distilled-600M")

    def translate(self, text, src_lang ="heb_Hebr", tgt_lang="eng_Latn"):
        res = self.pipe(
            text,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
        )
        return res
    
if __name__ == "__main__":
    translator = Translator()
    text = "אניגמה היא משפחה של מכונות להצפנה ולפענוח של מסרים טקסטואליים, ששימשו את הכוחות הגרמנים והאיטלקים במלחמת העולם השנייה. בזכות התקשורת המוצפנת שאפשרה האניגמה, הצליח הקריגסמרינה (הצי הגרמני), ובמיוחד צי הצוללות, במהלך המערכה באוקיינוס האטלנטי (1939–1945), להטיל מצור אפקטיבי על בריטניה, מצור שמנע אספקת מזון ואמצעי לחימה לאי הבריטי, בדרך הים."
    translation = translator.translate(text)
    print(translation)
