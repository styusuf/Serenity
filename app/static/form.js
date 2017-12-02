document.getElementById('final_form').addEventListener('submit', function() {
    // TODO be updated later with tuple
    var tuple = [];
    for (var i = 0; i < ings.length; i++) {
        var qty = document.getElementById(ings[i]).querySelector('#qty').value;
        var unit = document.getElementById(ings[i]).querySelector('#ingr_option').value;
        tuple.push(ings[i] + ":" + qty + ":" + unit);
    }
    document.getElementById('search_box').value = tuple.join(',');
}, false);
function form_list(units) {
    select = "<select name=\"units\" class=\"textbox ingr_unit\" id=\"ingr_option\">"
    if (units.length > 0) {
        units.forEach(function(element){
            select = select + "<option value='" + element + "'>" + element + "</option>"
        });
        select = select + "</select>"
        return select
    } else {
        return false
    }
}
function removeDiv(id) {
    var item = document.getElementById(id);
    document.getElementById('add_ingredient').removeChild(item);
    ings.pop();
    if (ings.length == 0) {
        document.getElementById('add_ingredient').style.display = "none";
        document.getElementById('search_button').style.display = "none";
    }
}
document.getElementById('add_button').addEventListener('click', function(){
    if (ings.length >= 1) {
        document.getElementById('add_ingredient').style.display = "inline-block";
        document.getElementById('search_button').style.display = "inline-block";
        var id = ings[ings.length-1];
        var ingr = document.getElementById('ingredients').value;
        document.getElementById('ingredients').value = "";
        var element = ""
        var select_list = form_list(units[id])
        if (select_list) {
            element = "<div id="+ id + "><input value=\"0\" min=\"0\" class=\"textbox ingr_quantity\" type='number' name='qty' id='qty' />" + select + "<input disabled=\"True\"class=\"textbox ingr_name\" type='text' value=\"" + ingr + "\"/><button class=\"button sub_button\" onclick=\"removeDiv(this.parentNode.id)\">-</button></div>";
        } else {
            element = "<div id="+ id + "><input value=\"0\" min=\"0\" class=\"textbox ingr_quantity\" type='number' name='qty' id='qty' disabled=\"True\"/><input class=\"textbox ingr_unit\" disabled=\"True\"/><input class=\"textbox ingr_name\" type='text' value=\"" + ingr + "\" disabled=\"True\"/><button class=\"button sub_button\" onclick=\"removeDiv(this.parentNode.id)\">-</button></div>"
        }
        document.getElementById('add_ingredient').innerHTML = document.getElementById('add_ingredient').innerHTML + element;
    }
}, false)