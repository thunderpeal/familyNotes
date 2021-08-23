var sizes = JSON.parse(localStorage.sizes || "{}");
$(function (){
    var d = $("[id=draggable]").attr("id", function (i) {
        return "draggable" + i
    });
    $.each(sizes, function (id, pos) {
        $("#" + id).css(pos)
    })
    d.resizable({
        containment: ".main-container",
        stop: function (event, ui) {
            sizes[this.id] = ui.size
            localStorage.sizes = JSON.stringify(sizes)
        }
    })
});