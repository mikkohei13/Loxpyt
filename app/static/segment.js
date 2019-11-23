
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

// Todo: Something wrong with session number handling durng save. hash and vr mismatch, hash skips numbers. 

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

  // Base data
  var annotation = {}
  annotation['segment'] = segmentNumberGlobal; // or segment_id?

//  annotation['_id'] = ;

  // Get data from form
  let formData = $("#form").serializeArray();

  // Format keywords as array
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

  // Validate tags
  if (0 == allTags.length) {
    warn("Must set at least one tag or keyword!")
  }
  else {
    // Combine all data
    annotation['tags'] = allTags;
//    console.log("annotation: ")
//    console.log(annotation);

    // Send to API
    $.ajax("/api/annotation", {
      type: "POST",
      data: JSON.stringify(annotation),
      contentType: "application/json; charset=utf-8"
    })
    .done(function() {
      console.log("SUCCESS: API responded with success!");
      moveToNextSegment();
    })
    .fail(function() {
      warn("API responded with failure!")
    })
    .always(function(response) {
      console.log("annotation after send: ")
      console.log(annotation);
  
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

