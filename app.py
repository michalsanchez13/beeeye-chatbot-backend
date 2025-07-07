from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])  # <- zmenené z /search na /chat
def chat():
    data = request.get_json()
    question = data.get("question", "") or data.get("message", "")  # ak frontend posiela "message"

    if not question:
        return jsonify({"answer": "Zadaj otázku, prosím."})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            max_tokens=200
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"Chyba: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
