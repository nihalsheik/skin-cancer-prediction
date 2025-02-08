function previewImage() {
  var file = document.getElementById("imagefile").files;
  if (file.length > 0) {
    var fileReader = new FileReader();

    fileReader.onload = function (event) {
      var previewImage = document.getElementById("preview");
      previewImage.style.display = "block";
      previewImage.setAttribute("src", event.target.result);
    };

    fileReader.readAsDataURL(file[0]);
  }
}
