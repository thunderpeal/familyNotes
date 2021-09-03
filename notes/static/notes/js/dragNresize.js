'use strict'
$(function () {
    let user1 = document.getElementById('user1').innerText;
    let us = JSON.parse(localStorage[user1] || "{}");
    let positions = {};
    let sizes = {};
    if (us.positions){
        positions = us.positions;
    }
    if (us.sizes){
        sizes = us.sizes;
    }

    let d = $("[id=draggable]").attr("id", function (i) {
        return "draggable_" + i
    })
    $.each(positions, function (id, pos) {
        $("#" + id).css(pos)
    })
    $.each(sizes, function (id, s) {
        $("#" + id).css('height', s.height)
        $("#" + id).css('width', s.width)
    })

    d.draggable({
        containment: ".main-container",
        scroll: false,
        handle: 'div.header-bar',
        stop: function (event, ui) {
            positions[this.id] = ui.position
            us.positions = positions;
            localStorage[user1] = JSON.stringify(us)
        }
    });

    $("body").on('mouseout', ".note", function () {
        us = JSON.parse(localStorage[user1] || "{}");
        let newHeight = $(this).height();
        let newWidth = $(this).width();
        sizes[$(this)[0].id] = { height: newHeight, width: newWidth};
        us.sizes = sizes;
        localStorage[user1] = JSON.stringify(us)
    })
});