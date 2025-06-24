const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

function ignoreWord(word_id) {
    tooltipList.forEach(tooltip => {
        tooltip.hide();
    });
    let url = `/word/ignore/${word_id}/`;
    fetch(url, {
        method: "GET",
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("col-" + word_id).remove();
        });
}

let ignoreButtons = document.getElementsByClassName("btn-ignore");
for (let index = 0; index < ignoreButtons.length; index++) {
    ignoreButtons[index].addEventListener("click", (e) => {
        ignoreWord(ignoreButtons[index].dataset.id);
    });
}