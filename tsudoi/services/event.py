from models.event import find_event_by_id, get_owner_by_event_id, get_fee_rules_by_event_id

def get_event_detail(event_id):
    event = find_event_by_id(event_id)
    if event is None:
        return None
    owner = get_owner_by_event_id(event_id)
    fee_rules = get_fee_rules_by_event_id(event_id)
    return {"event": event, "owner": owner, "fee_rules": fee_rules}

# 料金区分の年齢入力をチェックする
def validate_fee_rule_ages(tier_names, min_ages, max_ages):
    for tier_name, min_age, max_age in zip(
        tier_names, min_ages, max_ages
    ):
        # 区分名が空欄の場合は登録対象外
        if not tier_name:
            continue

        # 最小年齢・最大年齢の未入力チェック
        if not min_age or not max_age:
            return "料金区分の最小年齢と最大年齢を入力してください"

        # 整数チェック
        try:
            min_age = int(min_age)
            max_age = int(max_age)
        except (TypeError, ValueError):
            return "料金区分の年齢は0以上の整数で入力してください"

        # マイナスチェック
        if min_age < 0 or max_age < 0:
            return "料金区分の年齢は0以上で入力してください"

        # 最小年齢と最大年齢の前後関係チェック
        if min_age > max_age:
            return "最小年齢は最大年齢以下で入力してください"

    return None

# 料金区分の年齢・性別の重複をチェックする
def has_overlapping_fee_rules(tier_names, min_ages, max_ages, genders):
    rules = []

    for tier_name, min_age, max_age, gender in zip(tier_names, min_ages, max_ages, genders):
        # 区分名が空欄の場合は登録対象外
        if not tier_name:
            continue

        rules.append({
            "min_age": int(min_age),
            "max_age": int(max_age),
            "gender": gender or None,
        })

    # 料金区分同士を比較
    for i in range(len(rules)):
        for j in range(i + 1, len(rules)):
            rule1 = rules[i]
            rule2 = rules[j]

            # 年齢範囲が重なっているか
            age_overlaps = (
                rule1["min_age"] <= rule2["max_age"]
                and rule2["min_age"] <= rule1["max_age"]
            )

            # 性別の対象が重なっているか
            gender_overlaps = (
                rule1["gender"] is None
                or rule2["gender"] is None
                or rule1["gender"] == rule2["gender"]
            )

            if age_overlaps and gender_overlaps:
                return True
    return False