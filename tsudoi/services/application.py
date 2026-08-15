from models.application import summarize_applications_by_event
from models.event import find_event_by_id

def summarize_applications(event_id):
    summary_rows = summarize_applications_by_event(event_id)
    # イベント全体の参加人数を計算
    total_participants = len(summary_rows)
    # イベント全体の合計金額を計算
    total_amount = sum(row["amount"] for row in summary_rows)

    # 申込時の料金区分名をキーにして、料金区分毎の人数・金額を計算
    fee_summary = {}
    for row in summary_rows:
        fee_name = row["fee_rule_name_snapshot"]
        # 初めて登場した料金区分の場合、集計用のdictを作成
        if fee_name not in fee_summary:
            fee_summary[fee_name] = {
                "count": 0,
                "amount": 0
            }
        # 料金区分毎の参加人数と合計金額を加算
        fee_summary[fee_name]["count"] += 1
        fee_summary[fee_name]["amount"] += row["amount"]

    # 性別をキーにして、性別毎の合計人数を計算
    gender_summary = {}
    for row in summary_rows:
        gender = row["gender"]
        # 初めて登場した性別の場合、集計用のdictを作成
        if gender not in gender_summary:
            gender_summary[gender] = 0
        gender_summary[gender] +=  1

    # 世帯IDをキーにして、世帯ごとの人数・金額・参加者情報をまとめる
    household_summary = {}
    for row in summary_rows:
        household_id = row["household_id"]
        # 初めて登場した世帯の場合、集計用のdictを作成
        if household_id not in household_summary:
            household_summary[household_id] = {
                "count": 0,
                "amount": 0,
                "members": []
            }
        # 世帯の参加人数と合計金額を加算
        household_summary[household_id]["count"] +=1
        household_summary[household_id]["amount"] += row["amount"]
        # 世帯に所属する参加者情報をmembersへ追加
        household_summary[household_id]["members"].append({
            "name": row["member_name_snapshot"],
            "age": row["age_at_application"],
            "gender": row["gender"],
            "fee_rule_name": row["fee_rule_name_snapshot"],
            "amount": row["amount"]
        })
    # 世帯数を取得する
    household_count = len(household_summary)

    # イベント名を表示するためにmodels/event.pyのfind_event_by_id()からイベント情報を取得する
    event = find_event_by_id(event_id)

    # 集計した結果を返す
    return {
        "total_participants": total_participants,
        "total_amount": total_amount,
        "fee_summary": fee_summary,
        "gender_summary": gender_summary,
        "household_summary": household_summary,
        "household_count" : household_count,
        "event": event
    }
