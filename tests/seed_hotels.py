"""產生 data/hotels.json 的第一筆紀錄：2026-09-27 13:00 前後在瀏覽器實查じゃらん/Booking 的結果。"""
import json
from pathlib import Path

def j(cal, left, best, plans):
    mn = min(v["total"] for v in best.values()) if best else None
    return {"available": bool(best), "calendar": cal, "roomsLeft": left, "min": mn, "best": best, "plans": plans}

def b(total, room, plan, coupon=0, noBath=False, nonRefund=False):
    return {"total": total, "room": room, "plan": plan, "coupon": coupon, "noBath": noBath, "nonRefund": nonRefund}

seed = [{
  "checkedAt": "2026-09-27T13:10",
  "hotels": {
    "yosanoso": {"jalan": j("15 3 部屋", 3, {
        "none": b(14268, "和室（ユニットバス・トイレ付き）【OceanView】", "【じゃらんのお得な10日間】素泊まりプラン（１泊０食）", 4000, True),
        "dinner": b(24260, "和室（ユニットバス・トイレ付き）【OceanView】", "お手軽会席プラン（1泊夕食付き）", 4800, True),
        "both": b(28880, "和室（ユニットバス・トイレ付き）【OceanView】", "平日限定 お手軽会席プラン", 6600, True)}, 26)},
    "amanohashidate-hotel": {"jalan": j("15 2 部屋", 2, {
        "none": b(37400, "【禁煙】和洋室（オーシャンビュー）", "食事なしプラン"),
        "breakfast": b(44000, "【禁煙】和洋室（オーシャンビュー）", "朝食付きプラン"),
        "both": b(58520, "【禁煙】和洋室（オーシャンビュー）", "和食通常プラン")}, 0)},
    "atelier": {"jalan": j("16 ×", None, {}, 0),
                "booking": {"found": True, "title": "櫻花露台旅舍", "price": None, "soldOut": True}},
    "greenrich": {"jalan": j("16 ○", None, {
        "none": b(19280, "【喫煙】ダブルＡ", "★スタンダードシンプルステイ★素泊まり★"),
        "breakfast": b(22560, "【禁煙】ダブルＡ", "★朝食付プラン★")}, 0)},
    "ilverde": {"jalan": j("16 ▲", None, {
        "none": b(20400, "≪禁煙≫スタンダードダブルルーム", "【事前決済限定】返金不可プラン", 0, False, True),
        "breakfast": b(23120, "≪禁煙≫スタンダードダブルルーム", "【事前決済限定】朝食付き 返金不可プラン", 0, False, True)}, 0)},
    "zequu-annex": {"jalan": j("16 ○", None, {
        "none": b(23050, "ツインルーム【禁煙室】", "【返金不可】スタンダードプラン", 0, False, True)}, 0)}
  }
}]
Path(__file__).resolve().parent.parent.joinpath("data", "hotels.json").write_text(
    json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
print("seeded")
