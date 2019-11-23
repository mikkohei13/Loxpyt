
var segmentNumberGlobal;
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

// Todo: shortcut keys
/*
enter / arrow-right = save
s = silence
r = rain
w = wind
*/

//----------------------------------------------------

function init() {
  let hash = window.location.hash;
  segmentNumberGlobal = parseInt(hash.replace("#", ""), 10);

  // Todo: set spectro & audio
  // Todo: get segment data from API & db
  // Todo: if spectro & audio not found, return to main
//  console.log("segmentNumberGlobal: " + segmentNumberGlobal);
}

function save() {

  // Get data from form, format as array
  let formData = $("#form").serializeArray();
//  console.log(formData);

    var tags = [];
    var keywords = [];

    for (let i = 0; i < formData.length; i++) {
//    console.log(formData[i])
    if ("tags" == formData[i]['name']) {
      tags[i] = formData[i]['value'];
    }
    else if ("keywords" == formData[i]['name']) {
      keywords = formData[i]['value'].split(",");

      // Trim array items
      keywords = keywords.map(string => string.trim())
      // Remove empty items
      var keywords = keywords.filter(function (el) {
        return el != "" && el != null;
      });

    }
  }
  let allTags = tags.concat(keywords);
  console.log(allTags);

  // Validate array and send to API
  if (0 == allTags.length) {
    warn("Must set at least one tag or keyword!")
  }
  else {
    $.ajax("/api/annotation", {
      type: "POST",
      data: JSON.stringify(allTags),
      contentType: "application/json"
    })
    .done(function() {
      console.log("SUCCESS: API responded with success!");
      moveToNextSegment();
    })
    .fail(function() {
      warn("API responded with failure!")
    })
    .always(function(response) {
      console.log("API response: "); console.log(response);
    });
  }

}

function warn(warning) {
  console.log("WARNING: " + warning)
  $("#warn").html(warning);
  $("#warn").addClass("alert");
}

function clearWarning() {
  $("#warn").html();
  $("#warn").removeClass("alert");
}

function clearForm() {
  // Todo
}

function moveToNextSegment() {
  clearWarning();
  clearForm();

  let nextSegmentNumber = segmentNumberGlobal + 1;
  window.location.hash = "#" + nextSegmentNumber;

  init();
}

