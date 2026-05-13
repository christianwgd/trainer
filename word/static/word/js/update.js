const myModal = new bootstrap.Modal(document.getElementById('word-modal-form'));
let editButtons = document.getElementsByClassName("btn-edit");
for (let index=0; index < editButtons.length; index++) {
editButtons[index].addEventListener('click', (e) => {
    let word_id = editButtons[index].dataset.id;
    let url = `/word/get_word/${word_id}/`;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('id_source').value = data.word;
            document.getElementById('id_translation').value = data.translation;
            document.getElementById('id_word').value = word_id;
        })
        .catch(error => console.error(error));
    myModal.show();
});
}

let submitButton = document.getElementById('btn-submit');
submitButton.addEventListener('click', (e) => {
let word_id = document.getElementById('id_word').value;
let url = `/word/set_word/${word_id}/`;
fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": csrf_token
    },
    body: JSON.stringify({
        'word': document.getElementById('id_source').value,
        'translation': document.getElementById('id_translation').value,
    })
})
    .then(data => {
            myModal.hide();
            let selector = '.source-' + word_id;
            let source_elements = document.querySelectorAll(selector);
            let source = document.getElementById('id_source').value;
            for (let index=0; index < source_elements.length; index++) {
                source_elements[index].textContent = source;
            }
            let selector2 = '.translation-' + word_id;
            let translation_elements = document.querySelectorAll(selector2);
            let translation = document.getElementById('id_translation').value;
            for (let index=0; index < translation_elements.length; index++) {
                translation_elements[index].textContent = translation;
            }
        })
})