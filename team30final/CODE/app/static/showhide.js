function showMore(id) {
    document.getElementById(id + '_ing_small').setAttribute('class', document.getElementById(id + '_ing_small').getAttribute('class').replace('show', 'hide'));
    document.getElementById(id + '_ing_large').setAttribute('class', document.getElementById(id + '_ing_large').getAttribute('class').replace('hide', 'show'));
}
function showLess(id) {
    document.getElementById(id + '_ing_large').setAttribute('class', document.getElementById(id + '_ing_large').getAttribute('class').replace('show', 'hide'));
    document.getElementById(id + '_ing_small').setAttribute('class', document.getElementById(id + '_ing_small').getAttribute('class').replace('hide', 'show'));
}
function showProductPopup(id) {
    document.getElementById(id + '_view').setAttribute('class', document.getElementById(id + '_view').getAttribute('class').replace('hide', 'show'));
}
function hideProductPopup(id) {
    document.getElementById(id + '_view').setAttribute('class', document.getElementById(id + '_view').getAttribute('class').replace('show', 'hide'));
}