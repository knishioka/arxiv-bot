import os

import deepl


def translate(text: str, lang="ja"):
    """Translate text by Deepl.

    Args:
        text (str): Original text.
        lang (str): Target Language.

    Returns:
        str: Translated text.

    """
    api_key = os.environ["DEEPL_API_KEY"]
    translator = deepl.Translator(api_key)
    result = translator.translate_text(text, target_lang=lang)
    return result.text
