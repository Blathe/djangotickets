const urlParams = new URLSearchParams(window.location.search);

document.getElementById('hide-closed-filter').checked = localStorage.getItem('hideClosedChecked')
document.getElementById('sort-select-box').value = localStorage.getItem('sortSelection')

function updateSort() {
    var sortSelection = document.getElementById('sort-select-box').value;
    urlParams.set('sort', sortSelection);
    localStorage.setItem('sortSelection', sortSelection)
    window.location.search = urlParams;
}

function handleHideClosedTickets(checkbox) {
    if (checkbox.checked){
        localStorage.setItem('hideClosedChecked', true);
        urlParams.set('filters', 'hideClosed')
        window.location.search = urlParams;
    } else {
        urlParams.delete('filters')
        localStorage.removeItem('hideClosedChecked')
        window.location.search = urlParams;
    }
}