function updateProfile() {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (xml.readyState == 4 && xml.status == 200) {
            document.getElementById("alert-profile-update").style.display = "block"
        }
    };

    xml.open("POST", "profile_update.php", true);
    xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xml.send("firstName=" + document.getElementById("firstName").value + "&lastName=" + document.getElementById("lastName").value + "&email=" + document.getElementById("email").value + "&company=" + document.getElementById("company").value);
}
