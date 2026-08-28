from datetime import date, datetime
from models.household import get_family_members
from models.application import (
    get_fee_rules, 
    insert_application, 
    insert_application_participant, 
    update_application_total, 
    delete_application_participants, 
    summarize_applications_by_event,
    find_application_by_event_id_and_household_id,
    count_participants_by_event,
    count_participants_by_event_excluding_application
)
from models.event import find_event_by_id

#すでに同じイベントに同じ世帯の申し込みが存在するか確認する
def is_already_applied(event_id, household_id):
    existing_application = find_application_by_event_id_and_household_id(event_id,household_id)
    return existing_application is not None

#イベントの申込期限を過ぎていないか確認
def is_deadline_passed(event):
    if event.get('deadline') is None:
        return False
    return datetime.now() > event['deadline']

#member_idが自分の世帯のメンバーか確認する
def validate_member_ids(household_id, member_ids):
    members = get_family_members(household_id)
    valid_ids = {str(m['id']) for m in members}
    return all (member_id in valid_ids for member_id in member_ids)

# イベントの定員数を超えていないか確認する(新規申し込み)
def is_capacity_exceeded(event, new_participant_count):
    if event.get('capacity') is None:
        return False
    current_count = count_participants_by_event(event['id'])
    return (current_count + new_participant_count) > event['capacity']

#編集時の定員数確認
def is_capacity_exceeded_on_edit(event, application_id, new_participant_count):
    if event.get('capacity') is None:
        return False
    current_count = count_participants_by_event_excluding_application(event['id'], application_id)
    return (current_count + new_participant_count) > event['capacity']

def is_empty_selection(member_ids):
    return len(member_ids) == 0

# 生年月日から、現在の年齢を計算する
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


# 年齢に合う料金区分を、fee_rulesの中から探す
def find_fee_rule(fee_rules, age, gender):
    for rule in fee_rules:
        if rule['min_age'] <= age <= rule['max_age']:
            if rule['gender'] is None or rule['gender'] == gender:
                return rule
    return None


# 選択されたmember_idの一覧から、参加者ごとの金額情報を計算する(保存はしない)
def build_participants_preview(event_id, household_id, member_ids):
    members = get_family_members(household_id)
    fee_rules = get_fee_rules(event_id)

    # member_idからメンバー情報をすぐ引けるように、辞書に変換
    members_by_id = {str(m['id']): m for m in members}

    participants = []
    for member_id in member_ids:
        member = members_by_id[member_id]
        age = calculate_age(member['birth_date'])
        fee_rule = find_fee_rule(fee_rules, age, member['gender'])

        if fee_rule is None:
            continue

        participants.append({
            'member_id': member['id'],
            'member_name_snapshot': member['name'],
            'relation_snapshot': member['relation'],
            'age_at_application': age,
            'fee_rule_id': fee_rule['id'],
            'fee_rule_name_snapshot': fee_rule['tier_name'],
            'amount': fee_rule['fee'],
        })

    return participants


# 参加者情報一覧から、申し込みを確定してDBに保存する
def create_application(event_id, household_id, member_ids):
    participants = build_participants_preview(event_id, household_id, member_ids)
    total_amount = sum(p['amount'] for p in participants)

    application_id = insert_application(event_id, household_id, total_amount)

    for p in participants:
        insert_application_participant(
            application_id=application_id,
            member_id=p['member_id'],
            fee_rule_id=p['fee_rule_id'],
            member_name_snapshot=p['member_name_snapshot'],
            relation_snapshot=p['relation_snapshot'],
            age_at_application=p['age_at_application'],
            fee_rule_name_snapshot=p['fee_rule_name_snapshot'],
            amount=p['amount'],
        )
    return application_id

# 既存の申し込みを、新しい参加者内容で更新する
def update_application(application_id, event_id, household_id, member_ids):
    participants = build_participants_preview(event_id, household_id, member_ids)
    total_amount = sum(p['amount'] for p in participants)

    delete_application_participants(application_id)

    for p in participants:
        insert_application_participant(
            application_id=application_id,
            member_id=p['member_id'],
            fee_rule_id=p['fee_rule_id'],
            member_name_snapshot=p['member_name_snapshot'],
            relation_snapshot=p['relation_snapshot'],
            age_at_application=p['age_at_application'],
            fee_rule_name_snapshot=p['fee_rule_name_snapshot'],
            amount=p['amount'],
        )
    update_application_total(application_id, total_amount)


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
