
var segmentNumberGlobal;

window.onload = function() {
  init()
}

// Save buttons

let saveElement = document.getElementById("save");
if (saveElement) {
  saveElement.addEventListener('click', function() { 
    sendAnnotation("save"); 
  }, false);
}

let carryElement = document.getElementById("carry");
if (carryElement) {
  carryElement.addEventListener('click', function() { 
    sendAnnotation("carry"); 
  }, false);
}


// Checkbox styles
// Seems that this gets invoked only chen checkbox is checked/unchecked directly, not when done using jQuery prop
$(".tag").change(function() {
  if (this.checked) {
    $(this).parent().addClass("checkedlabel");
  }
  else {
    $(this).parent().removeClass("checkedlabel");
  }
});


// Keyboard shortcuts
// Todo: disable when cursor in keywords field. Remove comment also on /*else*/ below

// https://keycode.info/

document.onkeyup = function(e) {

  // If cursor in input field
  if (e.target.id == 'keywords') return;

  if (e.which == 49) { // 1
    moveToNextSegment();
  }
  if (e.which == 50) { // 2
    moveToNextSegment(10);
  }

  if (e.which == 77) {
    $("#migrant").prop("checked", true);
    $("#migrant").parent().addClass("checkedlabel");
  }
  else if (e.which == 87) {
    $("#wander").prop("checked", true);
    $("#wander").parent().addClass("checkedlabel");
  }
  else if (e.which == 76) {
    $("#local_individual").prop("checked", true);
    $("#local_individual").parent().addClass("checkedlabel");
  }
  else if (e.which == 192) {
    $("#local_choir").prop("checked", true);
    $("#local_choir").parent().addClass("checkedlabel");
  }
  else if (e.which == 70) {
    $("#faint").prop("checked", true);
    $("#faint").parent().addClass("checkedlabel");
  }
  else if (e.which == 71) {
    $("#strong").prop("checked", true);
    $("#strong").parent().addClass("checkedlabel");
  }
  else if (e.which == 73) {
    $("#silence").prop("checked", true);
    $("#silence").parent().addClass("checkedlabel");
  }
  else if (e.which == 78) {
    $("#single_noise").prop("checked", true);
    $("#single_noise").parent().addClass("checkedlabel");
  }
  else if (e.which == 82) {
    $("#rain").prop("checked", true);
    $("#rain").parent().addClass("checkedlabel");
  }
  else if (e.which == 89) {
    $("#wind").prop("checked", true);
    $("#wind").parent().addClass("checkedlabel");
  }

  // Clear all
  else if (e.which == 27) {
    $('#form').find('input:checkbox').prop('checked', false);
    $('#form').find('label').removeClass("checkedlabel");
  }

  // Save and carry on
  else if (e.which == 13) {
    console.log("save");
    sendAnnotation("save");
  }
  else if (e.which == 39) {
    console.log("carry");
    sendAnnotation("carry");
  }
};

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
  showAnnotationCount();

  // Todo: if spectro & audio not found, return to main
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
    let titleText = "File number: " + (data.segmentNumber - 1) + " - Segment: " + data._id + ", number " + data.segmentNumber + " - Start: " + data.segmentStartUTC;
    $("#titletext").text(titleText);
//    $("#prev").text(data.segmentNumber - 1);
//    $("#next").text(data.segmentNumber + 1);
    
  });
}

function sendAnnotation(mode) {
  console.log("SENDANNOTATION FUNCTION");

  // Base data
  var annotation = {}
  annotation['segmentNumber'] = segmentNumberGlobal;
  annotation['file_id'] = file_idGlobal;
  annotation['segment_id'] = file_idGlobal + "/" + segmentNumberGlobal;

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

function showAnnotationCount() {
  $.getJSON("http://localhost/api/annotation/count?file_id=" + file_idGlobal + "&segmentNumber=" + segmentNumberGlobal)
  .done(function(data) {
    console.log("HERE x1");
    console.log(data.count)
    if (data.count > 0) {
      $("#alert").text("Already " + data.count + " annotation(s) of this segment!");
      $("#alert").addClass("notice");
    }
  })
  .fail(function() {
    error("api/annotation/count responded with failure!")
  });
}

function clearAlert() {
  console.log("CLEARALERT FUNCTION");

  $("#alert").text("");
  $("#alert").removeClass("warning");
  $("#alert").removeClass("error"); // Todo: remove all classes?
}

function clearContent() {
  console.log("CLEARCONTENT FUNCTION");

  $("#titletext").text("");
  $("#spectrogram").attr("src", "");
  $("#audio").attr("src", "");
}

function clearForm() {
  console.log("CLEARFORM FUNCTION");

  $('#form').find('input:text, input:password, input:file, select, textarea').val('');
  $('#form').find('input:radio').prop('selected', false);
  $('#form').find('input:checkbox').prop('checked', false);

  $('#form').find('label').removeClass("checkedlabel");

}

function moveToNextSegment(skip = 1) {
  console.log("MOVETONEXTSEGMENT FUNCTION");

  let nextSegmentNumber = segmentNumberGlobal + skip;
  window.location.hash = ("#" + nextSegmentNumber);

  init();
}

