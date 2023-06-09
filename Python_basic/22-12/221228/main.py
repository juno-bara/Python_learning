from flask import Flask, request
import mod_sql as ms 
import json

app = Flask(__name__)
db = ms.Database("172.16.12.149", "ubion", "1234")

@app.route("/corona") # localhost : 8080 / corona 접속 시 아래의 함수를 실행

def corona():
    _id = request.args.get("id")
    _pass= request.args.get("pass")
    print(_id,_pass)
    login_sql = """ 
        select * from user_list where "id"=%s and "password" = %s
    """
    check = db.execute(login_sql,[_id,_pass])
    # 로그인 성공시 check > [{id:xxx, password:xxx}] t실패시 >> ()

    if check:

        sql = """
            select
            *
            from
            corona 
        """

        result = db.execute(sql)
        # print(result)
        return json.dumps(result)
    else :
        return "login fail"

app.run(port=8080)