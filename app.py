from app import *

app = create_app()

@app.route('/test')
def test_app():
    return "You are chicken🐣"

if __name__ == "__main__":
    app.run(debug = True)

