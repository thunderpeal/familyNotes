'use strict'
var zs_saved = JSON.parse(localStorage.zs || "{}");
$(function () {
    var d = $("[id=draggable]").attr("id", function (i) {
        return "draggable_" + i
    })
    $.each(zs_saved, function (id, zats) {
        $("#" + id).css(zats);
        let elem = document.getElementById(id)
        elem.firstElementChild.firstElementChild.children[1].innerText = zats['z-index'];
    })
});



let zUps = document.getElementsByClassName('zUp');
for (let z of zUps){
    z.addEventListener('click', function (){
        let prevZ = Number(z.parentElement.parentElement.parentElement.style.zIndex);
        let maxZ = zUps.length;
        if ((prevZ + Number(1)) < maxZ){
            z.parentElement.parentElement.parentElement.style.zIndex = prevZ + Number(1);
        }
        z.nextElementSibling.innerText = z.parentElement.parentElement.parentElement.style.zIndex;

        zs_saved[z.parentElement.parentElement.parentElement.id] = {'z-index':z.parentElement.parentElement.parentElement.style.zIndex};
        localStorage.zs = JSON.stringify(zs_saved)
    });
}

let zDowns = document.getElementsByClassName('zDown');
for (let z of zDowns){
    z.addEventListener('click', function (){
        let prevZ = Number(z.parentElement.parentElement.parentElement.style.zIndex);
        if (prevZ){
            z.parentElement.parentElement.parentElement.style.zIndex = prevZ - Number(1);
        }else{
            z.parentElement.parentElement.parentElement.style.zIndex = 0;
        }
        z.previousElementSibling.innerText = z.parentElement.parentElement.parentElement.style.zIndex;
    });
}

