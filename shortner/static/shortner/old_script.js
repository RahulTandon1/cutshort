// checker comment

function isAvailable() {
  fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    credentials: "same-origin",
    body: JSON.stringify({
      toCheck: true,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// following function has been copy pasted from https://www.w3schools.com/js/js_cookies.asp. This is not original content
function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

document
  .getElementById("formSubmit")
  .addEventListener("click", function (event) {
    event.preventDefault(); // not reloading
  });
document.getElementById("formSubmit").onclick = isAvailable;

let checkShortLink = () => {
  console.log("Shortlink keydown being run");

  fetch("/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      toCheck: true,
      shortLink: document.getElementById("shortLink").value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error("Error during fetch", error);
    });
};
