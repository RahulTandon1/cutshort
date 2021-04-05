function calcMonths() {
  var d1 = new Date();
  var d2 = new Date();
  
  // Cutshort was built in Aug 2020
  d1.setMonth(8);
  d1.setYear(2020);
  
  /*
  1000 milliseconds per sec * 60 seconds per min * 60 mins per hour 
  * 24 hours per day * 30 days a month
  */ 

  millisecondsInAMonth = 1000 * 60 * 60 * 25 * 30
  
  // difference between when user is seeing and when cutshort was built, in months
  text = Math.round( (d2-d1)/millisecondsInAMonth );

}

function getStats() {
  let statsBar = document.getElementById("stats")
  let statHolders = document.querySelectorAll(".stat-num")
  let months = calcMonths()
  statHolders[2].innerText = calcMonths


  
  fetch(`/api/getStats`, {
      method: "GET",
      credentials: "same-origin",
    })
    .then(res => res.json())
    .then( res => {
      
      statHolders[0].innerText = res.totalClicks
      statHolders[1].innerText = res.totalLinks
      statsBar.style.visibility = "visible"
    } )
    .catch(err => console.log(err))

}

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
  // !!!!!!!
  // note! Right now I've have hardcoded the HTTP bit.
  // !!!!!!!
  // make result div visible
  document.getElementById("result").style.display = "block";

  let resultAnchor = document.getElementById("result-link");
  // let hostURL = window.location.hostname;
  let hostURL = "cutshort.in"; // hardcoding cutshort.in
  url1 = `${hostURL}/${shortlink}`;
  url2 = 'https://' + url1

  console.log("url", url);
  resultAnchor.innerText = url1
  resultAnchor.href = url2;
  
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
// and this StackOverflow post ans:
// https://stackoverflow.com/questions/50795042/create-a-copy-button-without-an-input-text-box#:~:text=2%20Answers&text=You%20can%20use%20this%20kind,your%20onclick%20in%20the%20HTML.)&text=%3Cbutton%20id%3D%22Copy%22,here%2C%20to%20try!%22%3E
function copyShortlink() {
  let copyText = document.getElementById("result-link").href;

  // temp input obj
  let tempInput = document.createElement("input");
  tempInput.value = copyText;
  document.body.appendChild(tempInput);
  tempInput.select();
  document.execCommand("copy");
  // removing temp input obj
  document.body.removeChild(tempInput);
  alertCopyStatus();
}

function alertCopyStatus() {
  let statusP = document.getElementById("result-copy-status");
  statusP.innerText = `Copied!`;
  setTimeout(
    (statusP) => {
      statusP.innerText = "";
    },
    2000,
    statusP
  );
}
