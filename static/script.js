function updateSort() {
    var option = document.getElementById('sort-select-box').value;
    window.location.href = '/?sort=' + option;
}