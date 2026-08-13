import os
from flask import Flask, render_template, request, make_response
from engine.template_engine import TemplateEngine
from pdf_generator import generate_letter_pdf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=DOTENV_PATH)
except ImportError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get(
    "FLASK_SECRET_KEY", "dev-only-insecure-key-change-me"
)

engine = TemplateEngine()


@app.route("/")
def index():
    templates = engine.list_templates()
    return render_template("index.html", templates=templates)


@app.route("/editor/<template_key>", methods=["GET", "POST"])
def editor(template_key):
    template = engine.get_template(template_key)
    if not template:
        return "Template not found", 404
    placeholders = engine.get_placeholders(template_key)
    error = None
    if request.method == "POST":
        data = {field: request.form.get(field, "") for field in placeholders}

        if error:
            return render_template(
                "editor.html",
                template=template,
                placeholders=placeholders,
                error=error,
                form_data=data,
            )

        letter = engine.generate_letter(template_key, data)
        return render_template(
            "result.html",
            letter=letter,
            template_title=template.title,
        )

    return render_template("editor.html", template=template, placeholders=placeholders, error=None, form_data={})


@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    letter_text = request.form.get("letter_text", "")
    template_title = request.form.get("template_title", "")
    pdf_bytes = generate_letter_pdf(letter_text, title=template_title)
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=letter.pdf"
    return response


if __name__ == "__main__":
    app.run(debug=True)