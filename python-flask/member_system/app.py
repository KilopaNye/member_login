from flask import*
import pymongo
client=pymongo.MongoClient("mongodb+srv://root:root@mycluster.sofjul9.mongodb.net/?retryWrites=true&w=majority")
db=client.member_system
app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key="keycard123"

@app.route("/")
def index():
    return render_template("index.html")

#防止非會員進入此頁面
@app.route("/member")
def member():
    #判斷暱稱是否存在密鑰中
    if "nickname" in session:
        return render_template("member.html")
    else:
        return redirect("/")

@app.route("/error")
def error():
    message=request.args.get("msg","發生錯誤,請聯繫客服")
    return render_template("error.html",message=message)

#註冊
@app.route("/signup", methods=["POST"])
def signup():
    nickname=request.form.get("nickname")
    email=request.form.get("email")
    password=request.form.get("password")
    collection=db.user
#尋找資料庫中Email是否已存在
    result=collection.find_one({
        "email":email
    })
#如果mail已存在則跳往error頁面
    if result != None:
        return redirect("/error?msg=信箱已被註冊")
    collection.insert_one({
        "nickname":nickname,
        "email":email,
        "password":password
    })
    return redirect("/")

#登入
@app.route("/signin",methods=["POST"])
def signin():
    email=request.form.get("email")
    password=request.form.get("password")
    #選擇要操作的資料庫
    collection=db.user
    #尋找是否有相應資料，使用$and
    result=collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })
    #如果找不到資料就導向到錯誤頁面
    if result!=None:
    #在session中記錄會員資料 並導向到會員頁面
        session["nickname"]=result["nickname"]

        return redirect("/member")
    else: 
        return redirect("/error?msg=帳號或密碼錯誤")

#登出
@app.route("/signout")
def signout():
    #移除密鑰
    del session["nickname"]
    #導回首頁
    return redirect("/")

@app.route("/back")
def back():
    return redirect("/")

app.run(port=3000, debug=True)