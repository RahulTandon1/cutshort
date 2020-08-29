async function isAvailable() {
  shortlink = getShortlink();
  try {
    res = await fetch(`/api/check/${shortlink}`, {
      method: "GET",
      credentials: "same-origin",
    });
    res = await res.json();
    let availableStatus = res.available;
    return availableStatus;
  } catch (ex) {
    console.log(ex);
  }
}

function create() {
  fetch("/api/create/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    credentials: "same-origin",
    body: JSON.stringify({
      longlink: getLonglink(),
      shortlink: getShortlink(),
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      showResult(data.shortlink);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
// following function has been copy pasted from https://www.w3schools.com/js/js_cookies.asp.
// This is not original content
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

function getLonglink() {
  let longlink = document.getElementById("longlink-input").value;
  return longlink;
}

function getShortlink() {
  let shortlink = document.getElementById("shortlink-input").value;

  return shortlink;
}

function showResult(shortlink) {
  // make result div visible
  document.getElementById("result").style.display = "block";

  let resultAnchor = document.getElementById("result-link");
  let hostURL = window.location.hostname;
  url = `${hostURL}/${shortlink}`;
  resultAnchor.href = url;
  resultAnchor.innerText = url;
}

function verifyLongLink() {
  let t = String(getLonglink());
  let btn = document.getElementById("submitBtn");
  if (t.startsWith("http://") || t.startsWith("https://")) {
    btn.disabled = false;
  } else if (btn.disabled == false) {
    btn.disabled = true;
  }
}

function verifyShortLink() {
  let t = getShortlink();
  let btn = document.getElementById("submitBtn");
  if (t != "") {
    isAvailable()
      .then((res) => {
        // if avaiable
        if (res == true) {
          document.getElementById("shortlink-status").color = "blue";
          document.getElementById("shortlink-status").innerText = "available";
        } else {
          document.getElementById("shortlink-status").color = "red";
          document.getElementById("shortlink-status").innerText =
            "NOT available";
        }
      })
      .catch((ex) => console.error(ex));
  }
}

// this function was sourced from https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
function copyShortlink() {
  // get link href
  let copyText = document.getElementById("result-link").href;
  console.log(copyText);

  /* do the cool copy stuff */
  navigator.clipboard
    .writeText(copyText)
    .then(() => {
      let statusP = document.getElementById("result-copy-status");
      statusP.innerText = `Copied!`;

      setTimeout(
        (statusP) => {
          statusP.innerText = "";
        },
        2000,
        statusP
      );
    })
    .catch((err) => console.error("error while copying to clipboard", err));
}
