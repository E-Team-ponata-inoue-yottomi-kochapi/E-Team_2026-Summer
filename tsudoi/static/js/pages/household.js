//家族一覧のフォームの開閉処理
function toggleAddForm() {
    const form = document.getElementById('add-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function toggleEditForm(id) {
    const li = document.getElementById('member-' + id);
    const viewMode = li.querySelector('.household-member__view');
    const editMode = li.querySelector('.household-member__edit');
    const isEditing = editMode.style.display !== 'none';
    viewMode.style.display = isEditing ? 'flex': 'none';
    editMode.style.display = isEditing ? 'none': 'block';
    li.classList.toggle('household-member--editing', !isEditing);
}