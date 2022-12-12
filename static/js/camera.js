//here we need RPi IP address in MIR LAN
var path = "http://192.168.12.30:5500/picture";

const image_input = document.querySelector("#image-input");
let httpPost = new XMLHttpRequest();
httpPost.open("PUT", path);
httpPost.setRequestHeader("Accept", "application/json");
httpPost.setRequestHeader("Content-Type", "application/json");

image_input.addEventListener("change", function() {
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    document.querySelector("#display-image").style.backgroundImage = `url(${uploaded_image})`;

    var block = uploaded_image.split(";");
    // Get the content type of the image
    var contentType = block[0].split(":")[1];// In this case "image/gif"
    // get the real base64 content of the file
    var realData = block[1].split(",")[1];// In this case "R0lGODlhPQBEAPeoAJosM...."


    httpPost.onreadystatechange = function() {
        if (httpPost.readyState == 4 && httpPost.status == 200){
            console.log(httpPost.status);
            console.log(httpPost.responseText);
        };
    };
    httpPost.send(realData);
  });
  reader.readAsDataURL(this.files[0]);
});
