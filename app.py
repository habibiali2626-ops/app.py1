from flask import Flask, request
import json, os

app = Flask(__name__)

ORDERS_FILE = "orders.json"

def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)

orders = load_orders()

@app.route("/", methods=["GET", "POST"])
def home():
    global orders

    if request.method == "POST":
        orders.append({
            "product": request.form.get("product",""),
            "name": request.form.get("name",""),
            "family": request.form.get("family",""),
            "phone": request.form.get("phone",""),
            "postal": request.form.get("postal",""),
            "address": request.form.get("address","")
        })
        save_orders(orders)

    return """
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<title>نیلی گالری</title>
<style>
body{font-family:tahoma;background:#ff8c42;text-align:center;margin:0;padding:0}
.products{display:flex;justify-content:center;flex-wrap:wrap;gap:20px}
.card{background:white;width:250px;padding:20px;border-radius:15px;box-shadow:0 0 15px rgba(0,0,0,.25)}
button{padding:10px 15px;border:none;border-radius:8px;background:#2e7d32;color:white;cursor:pointer}
#orderForm{display:none;background:white;padding:20px;margin:20px auto;max-width:400px;border-radius:10px}
input{width:90%;padding:8px;margin:5px}
</style>
</head>
<body>

<div style="background:#e76f00;color:white;padding:25px;margin-bottom:20px;"><h1>🍊 NILI GALLERY 🍊</h1><h2>نیلی گالری</h2><p>خلق یادگاری‌های خاص</p></div>

<div class="products">
<div class="card">
<h2>بوک مارک MDF طرح گل</h2>
<h3>89,000 تومان</h3>
<button onclick="buyProduct('بوک مارک MDF طرح گل')">خرید</button>
</div>

<div class="card">
<h2>بوک مارک اسم اختصاصی</h2>
<h3>119,000 تومان</h3>
<button onclick="buyProduct('بوک مارک اسم اختصاصی')">خرید</button>
</div>

<div class="card">
<h2>جاکلیدی اسم سفارشی</h2>
<h3>129,000 تومان</h3>
<button onclick="buyProduct('جاکلیدی اسم سفارشی')">خرید</button>
</div>
</div>

<div id="orderForm">
<h2>ثبت سفارش</h2>
<form method="POST">
<input type="hidden" id="product" name="product">
<input name="name" placeholder="نام">
<input name="family" placeholder="نام خانوادگی">
<input name="phone" placeholder="شماره همراه">
<input name="postal" placeholder="کد پستی">
<input name="address" placeholder="آدرس">
<br><br>
<button type="submit">ثبت سفارش</button>
</form>
</div>

<script>
function buyProduct(name){
document.getElementById("orderForm").style.display="block";
document.getElementById("product").value=name;
}
</script>

</body>
</html>
"""

@app.route("/admin")
def admin():
    html = """
    <html dir="rtl"><meta charset="UTF-8">
    <h1>سفارش ها</h1>
    <table border="1" style="border-collapse:collapse">
    <tr><th>محصول</th><th>نام</th><th>نام خانوادگی</th><th>شماره</th></tr>
    """
    for o in orders:
        html += f"<tr><td>{o['product']}</td><td>{o['name']}</td><td>{o['family']}</td><td>{o['phone']}</td></tr>"
    html += "</table></html>"
    return html

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
