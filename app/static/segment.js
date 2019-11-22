
init()

/*
window.onload = function() {
  console.log("Calling init...")
}
*/

let saveElement = document.getElementById("save");
if (saveElement) {
  saveElement.addEventListener('click', save, false);
}

/*
saveButton = document.querySelector("#save");
saveButton.onclick = function() {
  console.log("Saving document... FAKE");
  moveToAnotherSegment(segmentNumber + 1);
}
*/

//----------------------------------------------------

function init() {
  let hash = window.location.hash;
  let segmentNumber = hash.replace("#", "");
  console.log("segmentNumber: " + segmentNumber);
}

function save() {
  let formData = $("#form").serializeArray();
//  console.log(formData);

    var tags = [];
    for (let i = 0; i < formData.length; i++) {
    console.log(formData[i])
    if ("tags" == formData[i]['name']) {
      tags[i] = formData[i]['value'];
    }
    else if ("keywords" == formData[i]['name']) {
      keywords = formData[i]['value'].split(",");

      // trim array items
      keywords = keywords.map(string => string.trim())

    }
  }
  let allTags = tags.concat(keywords);
  console.log(allTags);

  $.ajax("/api", {
    type: "POST",
    data: JSON.stringify(allTags),
    contentType: "application/json"
  })
  .done(function() { console.log("DONE"); })
  .fail(function() { console.log("FAIL"); })
  .always(function(response) { console.log("response from API: "); console.log(response); })
  ;

}


/*
,
    statusCode: {
      200: function (response) {
        console.log("API responded 200");
      }
    }, success: function (response) {
       console.log("Data sent to API");
    },
*/

function moveToAnotherSegment(segmentNumber) {
  window.location.hash = "#" + segmentNumber;
  init();
}

