document.addEventListener("DOMContentLoaded", function () {
  const addButton = document.getElementById("add-fee-rule");
  const container = document.getElementById("fee-rules-container");
  if (!addButton || !container) return;
  const isEditMode = container.dataset.isEdit === "true";

  const template = document.getElementById("fee-rule-template");
  const errorBox = document.getElementById("fee-rule-errors");
  const errorList = document.getElementById("fee-rule-errors-list");
  const form = container.closest("form");

  //区分を追加する処理
  addButton.addEventListener("click", function () {
    const clone = template.content.cloneNode(true);
    container.appendChild(clone);
    validateFeeRules();
  });

  //区分を削除する処理（編集画面の時だけ確認を入れる）
  container.addEventListener("click", function (event) {
    const deleteButton = event.target.closest(".fee-rule-delete");
    if (!deleteButton) return;
    const card = deleteButton.closest(".fee-rule-card");
    if (!card) return;
    if (isEditMode && !confirm("この区分を削除します。よろしいですか？")) {
      return;
    }
    card.remove();
    validateFeeRules();
  });

  //年齢や金額の編集のタイミングでチェック（リアルタイム）
  container.addEventListener("input", validateFeeRules);

  //作成ボタンを推した時に年齢幅の重複がある場合は、送信しない
  if (form) {
    form.addEventListener("submit", function (event) {
      if (!validateFeeRules()) {
        event.preventDefault();
        errorBox.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });
  }

  //空欄の区分カードは無視されるようにする。
  function readFeeRuleCards() {
    return Array.from(container.querySelectorAll(".fee-rule-card"))
      .map(function (card) {
        const name = card.querySelector('input[name="tier_name"]').value.trim();
        const minAge = Number(
          card.querySelector('input[name="min_age"]').value,
        );
        const maxAge = Number(
          card.querySelector('input[name="max_age"]').value,
        );
        const gender = card.querySelector('select[name="gender"]').value;
        return {
          card: card,
          name: name,
          minAge: minAge,
          maxAge: maxAge,
          gender: gender,
        };
      })
      .filter(function (rule) {
        return (
          rule.name !== "" &&
          !Number.isNaN(rule.minAge) &&
          !Number.isNaN(rule.maxAge)
        );
      });
  }

  // 2つの区分が年齢でも性別でも同じ人ではないかを確認する
  function conflicts(a, b) {
    const ageOverlaps = a.minAge <= b.maxAge && b.minAge <= a.maxAge;
    if (!ageOverlaps) return false;
    const genderOverlaps =
      a.gender === "" || b.gender === "" || a.gender === b.gender;
    return genderOverlaps;
  }

  // 全ての区分を確認して、矛盾があればエラーを表示して、エラーがなければ表示を消す
  function validateFeeRules() {
    const rules = readFeeRuleCards();
    const messages = [];

    container.querySelectorAll(".fee-rule-card").forEach(function (card) {
      card.classList.remove("has-conflict");
    });

    for (let i = 0; i < rules.length; i++) {
      for (let j = i + 1; j < rules.length; j++) {
        if (conflicts(rules[i], rules[j])) {
          rules[i].card.classList.add("has-conflict");
          rules[j].card.classList.add("has-conflict");
          messages.push(
            "「" +
              rules[i].name +
              "」と「" +
              rules[j].name +
              "」の年齢が重なっています（" +
              rules[i].minAge +
              "〜" +
              rules[i].maxAge +
              "歳 / " +
              rules[j].minAge +
              "〜" +
              rules[j].maxAge +
              "歳）",
          );
        }
      }
    }

    if (messages.length > 0) {
      errorList.innerHTML = "";
      messages.forEach(function (message) {
        const li = document.createElement("li");
        li.textContent = message;
        errorList.appendChild(li);
      });
      errorBox.classList.add("is-visible");
      return false;
    }

    errorBox.classList.remove("is-visible");
    return true;
  }

  //画面表示した時に重複がないかの確認
  validateFeeRules();
});
