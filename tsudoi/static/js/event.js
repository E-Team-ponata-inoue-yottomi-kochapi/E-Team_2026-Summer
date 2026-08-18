document.addEventListener("DOMContentLoaded", function () {
  const addButton = document.getElementById("add-fee-rule");
  if (!addButton) return;

  const container = document.getElementById("fee-rules-container");
  const template = document.getElementById("fee-rule-template");

  addButton.addEventListener("click", function () {
    const clone = template.content.cloneNode(true);
    container.appendChild(clone);
  });
});
