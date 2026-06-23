from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def form():
    return """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>さくらさく予約システム</title>

<style>

body{
    font-family: "Yu Gothic", sans-serif;
    background-color:#f4f4f4;
    margin:0;
    padding:0;
}

.container{
    width:420px;
    margin:50px auto;
    background:white;
    padding:30px;
    border-radius:15px;
    box-shadow:0 0 15px rgba(0,0,0,0.1);
}

h1{
    text-align:center;
    color:#444;
}

.subtitle{
    text-align:center;
    color:#777;
    margin-bottom:25px;
}

label{
    display:block;
    margin-bottom:5px;
    font-weight:bold;
}

input{
    width:100%;
    padding:10px;
    margin-bottom:15px;
    border:1px solid #ccc;
    border-radius:5px;
    box-sizing:border-box;
}

button{
    width:100%;
    padding:12px;
    background:#4CAF50;
    color:white;
    border:none;
    border-radius:5px;
    font-size:16px;
    cursor:pointer;
}

button:hover{
    opacity:0.9;
}

.link{
    text-align:center;
    margin-top:20px;
}

</style>

</head>
<body>

<div class="container">

<h1>☕ さくらさく</h1>

<div class="subtitle">
ご予約フォーム
</div>

<form action="/reserve" method="post">

<label>お名前</label>
<input type="text" name="name" required>

<label>来店日</label>
<input type="date" name="date" required>

<label>時間</label>

<select name="time" required>
    <option value="11:00">11:00</option>
    <option value="11:30">11:30</option>
    <option value="12:00">12:00</option>
    <option value="12:30">12:30</option>
    <option value="13:00">13:00</option>
    <option value="13:30">13:30</option>
    <option value="14:00">14:00</option>
    <option value="14:30">14:30</option>
    <option value="15:00">15:00</option>
    <option value="15:30">15:30</option>
    <option value="16:00">16:00</option>
</select>

<label>人数</label>
<input type="number" name="people" min="1" max="20" required>

<button type="submit">予約する</button>

</form>

<div class="link">
<a href="/list">予約一覧を見る</a>
</div>

</div>

</body>
</html>
"""

@app.route("/reserve", methods=["POST"])
def reserve():
    name = request.form["name"]
    date = request.form["date"]
    time = request.form["time"]
    people = request.form["people"]

    with open("reservations.csv", "a", encoding="utf-8") as f:
        f.write(f"{date},{time},{name},{people}\n")

    return f"""
<!DOCTYPE html>
<html lang="ja">

<head>
<meta charset="utf-8">
<title>予約完了</title>

<style>

body {{
    font-family: "Yu Gothic", sans-serif;
    background:#f4f4f4;
    margin:0;
}}

.container {{
    width:500px;
    margin:60px auto;
    background:white;
    padding:30px;
    border-radius:15px;
    box-shadow:0 0 15px rgba(0,0,0,0.1);
    text-align:center;
}}

h1 {{
    color:#4CAF50;
}}

.info {{
    margin-top:20px;
    text-align:left;
    display:inline-block;
    line-height:2;
}}

.button {{
    display:inline-block;
    margin-top:25px;
    padding:10px 20px;
    background:#4CAF50;
    color:white;
    text-decoration:none;
    border-radius:5px;
}}

</style>

</head>

<body>

<div class="container">

<h1>☕ ご予約ありがとうございました！</h1>

<p>{name} 様</p>

<div class="info">
来店日：{date}<br>
時間：{time}<br>
人数：{people}名
</div>

<br>

<a class="button" href="/">トップへ戻る</a>

</div>

</body>

</html>
"""

@app.route("/list")
def reservation_list():

    rows = ""
    count = 0
    reservations = []

    try:
        with open("reservations.csv", "r", encoding="utf-8") as f:

            for line in f:
                date, time, name, people = line.strip().split(",")

                reservations.append(
                    (date, time, name, people)
                )

                count += 1

        # ここでソート
        reservations.sort()

        # ソート後にHTML作成
        for date, time, name, people in reservations:

            rows += f"""
            <tr>
                <td>{date}</td>
                <td>{time}</td>
                <td>{name}</td>
                <td>{people}名</td>
            </tr>
            """

    except:
        rows = """
        <tr>
            <td colspan="4">予約データがありません</td>
        </tr>
        """
    reservations.sort()

    return f"""
<!DOCTYPE html>
<html lang="ja">

<head>
<meta charset="utf-8">
<title>予約一覧</title>

<style>

body {{
    font-family: "Yu Gothic", sans-serif;
    background:#f4f4f4;
    margin:0;
}}

.container {{
    width:900px;
    margin:40px auto;
    background:white;
    padding:30px;
    border-radius:15px;
    box-shadow:0 0 15px rgba(0,0,0,0.1);
}}

h1 {{
    text-align:center;
}}

table {{
    width:100%;
    border-collapse:collapse;
}}

th {{
    background:#4CAF50;
    color:white;
    padding:12px;
}}

td {{
    border-bottom:1px solid #ddd;
    padding:10px;
}}

tr:hover {{
    background:#f8f8f8;
}}

.summary {{
    margin-bottom:20px;
    font-size:18px;
}}

.back {{
    margin-top:20px;
}}

a {{
    text-decoration:none;
}}

</style>

</head>

<body>

<div class="container">

<h1>☕ さくらさく予約一覧</h1>

<div class="summary">
予約件数：{count}件
</div>

<table>

<tr>
    <th>来店日</th>
    <th>時間</th>
    <th>お名前</th>
    <th>人数</th>
</tr>

{rows}

</table>

<div class="back">
    <a href="/">← 予約画面へ戻る</a>
</div>

</div>

</body>
</html>
"""

app.run(debug=True)