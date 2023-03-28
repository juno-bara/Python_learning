from flask import Flask

# Flask 라는 클라스 생성 (파일의 이름)
# __name__ : 파일의 리름
app = Flask(__name__)

@app.route("/")  # "/" 로 request가 왔을때 아래의 함수를 실행
def index():
    return "bagopa" # user 에게 response

app.run()