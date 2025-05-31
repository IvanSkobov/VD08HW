from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Опционально: ключ от api-ninjas
NINJAS_API_KEY = ""

QUOTE_APIS = [
    "https://zenquotes.io/api/random",
    "https://api.api-ninjas.com/v1/quotes"
]

def translate_text(text, target_lang="ru"):
    try:
        response = requests.post(
            "https://translate.googleapis.com/translate_a/single",
            params={
                "client": "gtx",
                "sl": "en",
                "tl": target_lang,
                "dt": "t",
                "q": text
            }
        )
        result = response.json()
        return result[0][0][0]
    except Exception as e:
        return text + " (перевод недоступен)"

def get_random_quote(lang):
    api_url = random.choice(QUOTE_APIS)
    headers = {}

    if "api-ninjas" in api_url and NINJAS_API_KEY:
        headers["X-Api-Key"] = NINJAS_API_KEY

    try:
        response = requests.get(api_url, headers=headers)
        data = response.json()

        if "zenquotes" in api_url:
            quote = data[0]["q"]
            author = data[0]["a"]
        elif "api-ninjas" in api_url:
            quote = data[0]["quote"]
            author = data[0]["author"]
        else:
            quote = "Не удалось получить цитату"
            author = "Сервер"

        if lang == "ru":
            quote = translate_text(quote)
            author = translate_text(author)

        return quote, author

    except Exception as e:
        return "Не удалось загрузить цитату", "Сервер"

@app.route("/", methods=["GET"])
def index():
    lang = request.args.get("lang", "en")
    theme = request.args.get("theme", "light")
    quote, author = get_random_quote(lang)
    return render_template("index.html", quote=quote, author=author, lang=lang, theme=theme)

if __name__ == "__main__":
    app.run(debug=True)
