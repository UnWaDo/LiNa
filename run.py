from web import app


app.debug = False
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=33507)
