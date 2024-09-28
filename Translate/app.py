from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)

SUPPORTED_LANGUAGES = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu',
}


@app.route('/', methods=['GET', 'POST'])
def translate():
    text = ''
    translation = ''
    from_language = 'en'
    to_language = 'es'
    
    if request.method == 'POST':
        text = request.form['text']
        from_language = request.form['from_language']
        to_language = request.form['to_language']

        if text.strip() == '':
            return render_template('meme.html', error="Please enter some text to translate."), 400

        if from_language not in SUPPORTED_LANGUAGES or to_language not in SUPPORTED_LANGUAGES:
            return render_template('meme.html', error="Invalid language selection."), 400

        try:
            translator = Translator()
            translation = translator.translate(text, src=from_language, dest=to_language)

            
            if isinstance(translation, str):
                return render_template('meme.html', error="Translation error: " + translation), 500
        except Exception as e:
            return render_template('meme.html', error="Translation error: " + str(e)), 500

    lang_options = list(SUPPORTED_LANGUAGES.items())
    
    return render_template('meme.html', text=text, translation=translation.text if hasattr(translation, 'text') else translation, lang_options=lang_options)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
