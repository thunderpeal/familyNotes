'use strict'
$(function () {
    let user1 = document.getElementById('user1').innerText;
    let positions = JSON.parse(localStorage[user1] || "{}");

    let d = $("[id=draggable]").attr("id", function (i) {
        return "draggable_" + i
    })
    $.each(positions, function (id, pos) {
        $("#" + id).css(pos)
    })

    d.draggable({
        containment: ".main-container",
        scroll: false,
        handle: 'div.header-bar',
        stop: function (event, ui) {
            positions[this.id] = ui.position
            localStorage[user1] = JSON.stringify(positions)
        }
    });
});