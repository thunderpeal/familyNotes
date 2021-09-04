'use strict'
$(function () {
    let user1 = document.getElementById('user1').innerText;
    let us = JSON.parse(localStorage[user1] || "{}");
    let positions = {};
    let zs_saved = {};
    let sizes = {};
    if (us.positions){
        positions = us.positions;
    }
    if (us.sizes){
        sizes = us.sizes;
    }
    if (us.zs){
        zs_saved = us.zs;
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
    $.each(zs_saved, function (id, zats) {
        $("#" + id).css(zats);
        let elem = document.getElementById(id)
        elem.firstElementChild.children[1].children[1].innerText = zats['z-index'];
    })

    let zUps = document.getElementsByClassName('zUp');
for (let z of zUps){
    z.addEventListener('click', function (){
        let us = JSON.parse(localStorage[user1] || "{}");
        let zs_saved = {};
        if (us.zs){
        zs_saved = us.zs;
        }
        let prevZ = Number(z.parentElement.parentElement.parentElement.style.zIndex);
        let maxZ = zUps.length;
        if ((prevZ + Number(1)) < maxZ){
            z.parentElement.parentElement.parentElement.style.zIndex = prevZ + Number(1);
        }
        z.nextElementSibling.innerText = z.parentElement.parentElement.parentElement.style.zIndex;

        zs_saved[z.parentElement.parentElement.parentElement.id] = {'z-index':z.parentElement.parentElement.parentElement.style.zIndex};

        us.zs = zs_saved;
        localStorage[user1]= JSON.stringify(us)
    });
}

let zDowns = document.getElementsByClassName('zDown');
for (let z of zDowns){
    z.addEventListener('click', function (){
        let us = JSON.parse(localStorage[user1] || "{}");
        let zs_saved = {};
        if (us.zs){
        zs_saved = us.zs;
        }
        let prevZ = Number(z.parentElement.parentElement.parentElement.style.zIndex);
        if (prevZ){
            z.parentElement.parentElement.parentElement.style.zIndex = prevZ - Number(1);
        }else{
            z.parentElement.parentElement.parentElement.style.zIndex = 0;
        }
        z.previousElementSibling.innerText = z.parentElement.parentElement.parentElement.style.zIndex;
zs_saved[z.parentElement.parentElement.parentElement.id] = {'z-index':z.parentElement.parentElement.parentElement.style.zIndex};
        us.zs = zs_saved;
        localStorage[user1]= JSON.stringify(us)
    });
}
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