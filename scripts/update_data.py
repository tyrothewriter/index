import json, time, sys, datetime as dt, pathlib
import yfinance as yf

GROUPS = [
    ("asia", "เอเชีย-แปซิฟิก", [
        ("^N225", "ญี่ปุ่น Nikkei 225"), ("^HSI", "ฮ่องกง Hang Seng"),
        ("^STI", "สิงคโปร์ STI"), ("^BSESN", "อินเดีย Sensex"), ("^NSEI", "อินเดีย Nifty 50"),
        ("^JKSE", "อินโดนีเซีย JCI"), ("^KLSE", "มาเลเซีย KLCI"),
        ("^AXJO", "ออสเตรเลีย ASX 200")]),
    ("europe", "ยุโรป", [
        ("^FTSE", "อังกฤษ FTSE 100"), ("^FCHI", "ฝรั่งเศส CAC 40"),
        ("^GDAXI", "เยอรมนี DAX"), ("FTSEMIB.MI", "อิตาลี FTSE MIB")]),
    ("america", "อเมริกา", [
        ("^DJI", "Dow Jones"), ("^GSPC", "S&P 500"), ("^IXIC", "Nasdaq Composite")]),
    ("futures", "ดัชนีล่วงหน้า (Futures)", [
        ("YM=F", "Dow Jones Futures"), ("ES=F", "S&P 500 Futures"), ("NQ=F", "Nasdaq 100 Futures")]),
    ("commodities", "ทองโลก น้ำมัน ค่าระวางเรือ", [
        ("GC=F", "ทองคำตลาดโลก (USD/oz)"), ("CL=F", "น้ำมัน WTI (USD/bbl)"),
        ("BZ=F", "น้ำมัน Brent (USD/bbl)"), ("^BDI", "Baltic Dry Index (ค่าระวางเรือ)")]),
    ("fx", "คริปโตและค่าเงิน", [
        ("BTC-USD", "Bitcoin (BTC/USD)"), ("THB=X", "ดอลลาร์สหรัฐ/บาท (USD/THB)")]),
]

def quote(sym, tries=3):
    for i in range(tries):
        try:
            c = yf.Ticker(sym).history(period="1mo", interval="1d", auto_adjust=False)["Close"].dropna()
            if len(c) >= 2:
                last, prev = float(c.iloc[-1]), float(c.iloc[-2])
                return {"price": last, "change": last - prev, "pct": (last - prev) / prev * 100,
                        "asof": c.index[-1].strftime("%Y-%m-%d"),
                        "spark": [round(float(x), 2) for x in c.tail(30)]}
        except Exception as e:
            print("ERR", sym, e)
        time.sleep(2)
    print("NO DATA", sym)
    return None

def main():
    data = {"updated": dt.datetime.now(dt.timezone.utc).isoformat(), "groups": []}
    ok = 0
    for gid, title, items in GROUPS:
        rows = []
        for sym, name in items:
            q = quote(sym)
            ok += q is not None
            rows.append({"symbol": sym, "name": name, **(q or {})})
        data["groups"].append({"id": gid, "title": title, "rows": rows})
    pathlib.Path("data").mkdir(exist_ok=True)
    pathlib.Path("data/data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ดึงสำเร็จ {ok} รายการ")
    if ok == 0:
        sys.exit(1)

if __name__ == "__main__":
    main()

