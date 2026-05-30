from flask import Flask, render_template, render_template_string, request, send_from_directory, send_file, jsonify
from jinja2 import TemplateNotFound
from parser import parse
import io
import subprocess
import os

from codegen import generate_cpp
from java_generator import generate_java
from js_generator import generate_js

app = Flask(__name__, template_folder='.', static_folder='.')


@app.route("/", methods=["GET", "POST"])
def index():
    output_code = ""
    python_code = ""
    language = "cpp"

    if request.method == "POST":

        language = request.form.get("language", "cpp")

        if "code" in request.form and request.form["code"].strip():
            python_code = request.form["code"]

        elif "file" in request.files:
            file = request.files["file"]
            if file and file.filename.endswith(".py"):
                python_code = file.read().decode("utf-8")

        if python_code:
            ast = parse(python_code.split("\n"))

            if language == "cpp":
                output_code = generate_cpp(ast)

            elif language == "java":
                output_code = generate_java(ast)

            elif language == "js":
                output_code = generate_js(ast)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"output": output_code})

    try:
        return render_template("index.html", cpp_code=output_code, language=language)
    except TemplateNotFound:
        with open("index.html", "r", encoding="utf-8") as fh:
            return render_template_string(fh.read(), cpp_code=output_code, language=language)

@app.route("/run", methods=["POST"])
def run_code():
    code = request.form.get("code", "")
    language = request.form.get("language", "cpp")
    user_input = request.form.get("input", "")

    try:
        if language == "python":
            result = subprocess.run(
                ["python", "-c", code],
                input=user_input,
                text=True,
                capture_output=True
            )
            output = result.stdout if result.returncode == 0 else result.stderr
            return output if output else "(No output)"

        elif language == "cpp":
            with open("temp.cpp", "w") as f:
                f.write(code)

            compile_result = subprocess.run(
                ["g++", "temp.cpp", "-o", "temp.exe"], 
                capture_output=True, 
                text=True,
                shell=True
            )
            if compile_result.returncode != 0:
                return "Compilation Error:\n" + (compile_result.stderr or compile_result.stdout)

            result = subprocess.run(
                ["temp.exe"],
                input=user_input,
                text=True,
                capture_output=True,
                shell=True
            )
            
            if result.returncode != 0:
                return "Runtime Error:\n" + (result.stderr or result.stdout)
            
            output = result.stdout
            return output if output else "(No output)"

        elif language == "java":
            # Write Java code to file
            with open("Main.java", "w") as f:
                f.write(code)

            # Compile Java code
            compile_result = subprocess.run(
                ["javac", "Main.java"], 
                capture_output=True, 
                text=True,
                shell=True
            )
            if compile_result.returncode != 0:
                error_msg = compile_result.stderr or compile_result.stdout
                return "Compilation Error:\n" + error_msg if error_msg else "Compilation failed"

            # Run compiled Java code
            result = subprocess.run(
                ["java", "Main"],
                input=user_input,
                text=True,
                capture_output=True,
                shell=True
            )
            
            if result.returncode != 0:
                return "Runtime Error:\n" + (result.stderr or result.stdout)
            
            output = result.stdout
            return output if output else "(No output)"

        elif language == "js":
            # Add helper code for stdin input handling (not shown to user)
            helper_code = """const lines = require('fs').readFileSync(0, 'utf-8').trim().split('\\n');
let inputIndex = 0;
function input() { return lines[inputIndex++]; }
"""
            full_code = helper_code + code
            
            # Write JavaScript code to file
            with open("script.js", "w") as f:
                f.write(full_code)
            
            result = subprocess.run(
                ["node", "script.js"],
                input=user_input,
                text=True,
                capture_output=True,
                shell=True
            )
            
            if result.returncode != 0:
                return "Runtime Error:\n" + (result.stderr or result.stdout)
            
            output = result.stdout
            return output if output else "(No output)"

        return "Unsupported language"

    except Exception as e:
        return "Error: " + str(e)

@app.route("/download", methods=["POST"])
def download():
    code = request.form.get("cpp_code", "")
    language = request.form.get("language", "cpp")

    filename = {
        "cpp": "output.cpp",
        "java": "Main.java",
        "js": "script.js"
    }.get(language, "output.txt")

    file = io.BytesIO()
    file.write(code.encode("utf-8"))
    file.seek(0)

    return send_file(file, as_attachment=True, download_name=filename, mimetype="text/plain")


# -------------------------------
# STATIC CSS
# -------------------------------
@app.route('/style.css')
def serve_css():
    return send_from_directory('.', 'style.css')


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)