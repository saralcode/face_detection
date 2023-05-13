console.log("hello dear");

function dataURLtoFile(dataurl, filename) {
  var arr = dataurl.split(","),
    mime = arr[0].match(/:(.*?);/)[1],
    bstr = atob(arr[1]),
    n = bstr.length,
    u8arr = new Uint8Array(n);

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  return new File([u8arr], filename, { type: mime });
}
const videoObject = document.getElementById("video-element");
const canvas = document.getElementById("img-element");

const captureButton = document.getElementById("capture-btn");
captureButton.addEventListener("click", async () => {
  canvas.width = videoObject.videoWidth;
  canvas.height = videoObject.videoHeight;
  canvas
    .getContext("2d")
    .drawImage(videoObject, 0, 0, canvas.width, canvas.height);
  const image_data_url = canvas.toDataURL("image/jpeg");
  const data = new FormData();
  const csrf = document.getElementById("csrf").firstChild.nextSibling.value;
  const image = dataURLtoFile(image_data_url, "image.jpeg");
  console.log(image);
  data.append("file", image);
  const isLogin = window.location.pathname == "/login/";
  const url = isLogin ? "/login/" : "/update-user";
  fetch(url, {
    method: "POST",
    body: data,
    headers: { "x-CSRFToken": csrf },
  })
    .then(async (response) => {
      const resData = await response.json();
      console.log(resData["success"]);
      if (resData["success"]) {
        if (!isLogin) {
          alert("Updated");
        }
        window.location.reload();
      } else {
        alert("Opps Not Matched🙃");
      }
    })
    .catch((er) => {
      console.log("error ", er);
    });
  // console.log(image_data_url);
});
var hdConstraints = {
  video: {
    mandatory: {
      minWidth: 1280,
      minHeight: 720,
      /*Added by Chad*/
      maxWidth: 1280,
      maxHeight: 720,
    },
  },
};
if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices
    .getUserMedia(hdConstraints)
    .then((stream) => {
      videoObject.srcObject = stream;
    })
    .catch((err) => console.log(err));
}
