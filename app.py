from flask import Flask, render_template, request, redirect, flash
import subprocess
import os

app = Flask(__name__)
app.secret_key = "segredo"
PASTA_VIDEOS = os.path.join(os.getcwd(), "videos_youtube")
os.makedirs(PASTA_VIDEOS, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            flash("Cole um link válido do YouTube Shorts.", "danger")
            return redirect("/")
        
        comando = f'yt-dlp -f "bv*+ba/b" "{url}" -o "{PASTA_VIDEOS}/%(upload_date)s_%(title).50s.%(ext)s"'
        try:
            subprocess.run(comando, shell=True)
            flash("Download concluído com sucesso!", "success")
        except Exception as e:
            flash(f"Erro: {str(e)}", "danger")
        return redirect("/")
    
    return render_template("index.html")

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1", port=5000)
