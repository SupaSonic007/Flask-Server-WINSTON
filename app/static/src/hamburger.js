$(document).ready(function () {
    // The hamburger button will toggle the navbar in a smaller screen
    $("#hamburger").click(function () {
        $("#navbar").toggleClass("hidden");
        console.log("clicked")
    });
});
