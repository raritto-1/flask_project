from flask import Flask, render_template, request

app = Flask(__name__,template_folder="template")

@app.route("/", methods=["GET", "POST"])
def prime_checker():
    result = None
    if request.method == "POST":
        number = request.form["number"]
        if number.isdigit():
            num = int(number)
            if num > 1 and all(num % i != 0 for i in range(2, int(num**0.5) + 1)):
                result = f"{num} is a prime number."
            else:
                result = f"{num} is not a prime number."
        else:
            result = "Please enter a valid number."
    return render_template("prime_number.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
