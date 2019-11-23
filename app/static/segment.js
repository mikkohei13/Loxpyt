
var segmentNumberGlobal;

window.onload = function() {
  console.log("Calling init...")
  init()
}

let saveElement = document.getElementById("save");
if (saveElement) {
  saveElement.addEventListener('click', function() { sendAnnotation("save"); }, false);
}

let carryElement = document.getElementById("carry");
if (carryElement) {
  carryElement.addEventListener('click', function() { sendAnnotation("carry"); }, false);
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
  console.log("INIT FUNCTION");
  clearAlert();

  let hash = window.location.hash;
  segmentNumberGlobal = parseInt(hash.replace("#", ""), 10);

  getSegmentData(file_idGlobal, segmentNumberGlobal);

  // Todo: set spectro & audio
  // Todo: get segment data from API & db
  // Todo: if spectro & audio not found, return to main
//  console.log("segmentNumberGlobal: " + segmentNumberGlobal);
}

function getSegmentData(file_id, segmentNumber) {
  console.log("GETSEGMENTDATA FUNCTION");

  var url = "/api/segment?file_id=" + file_id + "&segmentNumber=" + segmentNumber;
  $.getJSON( url, {
    format: "json"
  })
  .done(function(data) {
    console.log("FROM API");
    console.log(data.spectroFilename); // ok

    let basePath = "http://localhost:8080/";
    let spectrogramPath = basePath + data.fileDirectory + "/" + data.spectroFilename;
    $("#spectrogram").attr("src", spectrogramPath);
    let audioPath = basePath + data.fileDirectory + "/" + data.finalAudioFilename;
    $("#audio").attr("src", audioPath);
    let titleText = "Segment: " + data._id + ", number " + data.segmentNumber + " - Start: " + data.segmentStartUTC;
    $("#title").text(titleText);
    

  });
}

function sendAnnotation(mode) {
  console.log("SENDANNOTATION FUNCTION");

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
    warning("Must set at least one tag or keyword!")
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

      if ("save" == mode) {
        clearAlert();
        clearForm(); // This is the difference between save and carry
        clearContent();
        moveToNextSegment();
      }
      else if ("carry" == mode) {
        clearAlert();
        clearContent();
        moveToNextSegment();
      }

    })
    .fail(function() {
      error("API responded with failure!")
    })
    .always(function(response) {
      console.log("annotation after send: ")
      console.log(annotation);
  
      console.log("API response: "); console.log(response);
    });
  }

}

function warning(message) {
  console.log("WARNING: " + message)
  $("#alert").text(message);
  $("#alert").addClass("warning");
}

function error(message) {
  console.log("ERROR: " + message)
  $("#alert").text(message);
  $("#alert").addClass("error");
}

function clearAlert() {
  console.log("CLEARALERT FUNCTION");

  $("#alert").text("");
  $("#alert").removeClass("warning");
  $("#alert").removeClass("error"); // Todo: remove all classes?
}

function clearContent() {
  console.log("CLEARCONTENT FUNCTION");

  $("#title").text("");
  $("#spectrogram").attr("src", "");
  $("#audio").attr("src", "");
}

function clearForm() {
  console.log("CLEARFORM FUNCTION");

  $('#form').find('input:text, input:password, input:file, select, textarea').val('');
  $('#form').find('input:radio').prop('selected', false);
  $('#form').find('input:checkbox').prop('checked', false);
}

function moveToNextSegment() {
  console.log("MOVETONEXTSEGMENT FUNCTION");

  let nextSegmentNumber = segmentNumberGlobal + 1;
  window.location.hash = "#" + nextSegmentNumber;

  init();
}

