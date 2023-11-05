from azure.ai.translation.text.models import InputTextItem
from flask import Flask, render_template, request
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

app = Flask(__name__)

# Azure Translator credentials
subscription_key = "acbd6dafbb0b4a16994227507a0e1b7b"
region = "northeurope"

# Create a translation client
translation_client = TextTranslationClient(credential=TranslatorCredential(subscription_key, region))

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""

    if request.method == 'POST':
        source_language = "zh-Hans"
        source_script = "Latn"
        input_text_elements = [InputTextItem(text="zhè shì gè cè shì。")]

        response = translation_client.find_sentence_boundaries(content=input_text_elements, language=source_language,
                                                            script=source_script)

        text_to_translate = [InputTextItem(text=request.form['text_to_translate'])]
        target_language = [request.form['target_language']]
        source_language = response[0].detected_language

        translated_text = translation_client.translate(content=text_to_translate, from_parameter=source_language,
                                                       to=target_language)[0].translations[0]["text"]

    return render_template('index.html', translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
