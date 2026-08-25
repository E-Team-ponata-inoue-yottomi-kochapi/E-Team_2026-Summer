from models.household import get_family_members,get_family_member_by_id
from datetime import date

LIMITED_RELATIONS = ['本人', '夫', '妻']


# 指定した続柄が、すでに登録済みかどうかを確認する
def is_relation_duplicated(household_id, relation):
    if relation not in LIMITED_RELATIONS:
        return False

    members = get_family_members(household_id)
    return any(m['relation'] == relation for m in members)

#指定した続柄がすでに登録済みかを確認する
def is_relation_duplicated_on_edit(household_id, relation, member_id):
    if relation not in LIMITED_RELATIONS:
        return False

    members = get_family_members(household_id)
    return any(m['relation'] == relation and m['id'] != member_id for m in members)

# 指定したメンバーが「本人」かどうかを確認する
def is_self_member(member_id):
    member = get_family_member_by_id(member_id)
    if member is None:
        return False
    return member['relation'] == '本人'

#フォームの入力エラーの作成
def validate_member_input(relation, birth_date):
    errors=[]
    if relation:
        relation = relation.strip()
    if birth_date:
        birth_date = birth_date.strip()
    if not relation:
        errors.append("続柄を選択してください")
    if not birth_date:
        errors.append("生年月日を入力してください")
    else:
        try:
            parsed_date = date.fromisoformat(birth_date)
            if parsed_date > date.today():
                errors.append("生年月日は今日より前の日付を入力してください")
        except ValueError:
            errors.append("生年月日の形式が正しくありません")
    
    return errors
        
# 本人の続柄を、他の続柄に変更しようとしていないか確認する
def is_changing_self_relation(member_id, new_relation):
    member = get_family_member_by_id(member_id)
    if member is None:
        return False
    return member['relation'] == '本人' and new_relation != '本人'
    