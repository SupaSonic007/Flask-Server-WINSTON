document.addEventListener('DOMContentLoaded', function () {
    // The hamburger button will toggle the navbar in a smaller screen
    document.getElementById("hamburger").addEventListener('click', () => {
        var navbar = document.getElementById("navbar");
        if (navbar.classList.contains('hidden')) navbar.classList.remove('hidden');
        else navbar.classList.add('hidden');
        console.log("clicked")
    });
});
