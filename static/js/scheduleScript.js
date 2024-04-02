/* ******************************* schedule.html page functions ******************************* */
/* To set properties for add-session button in schedule page */
document.addEventListener("DOMContentLoaded", function () {
  const addSessionButton = document.getElementById("add-session-button");
  const addSessionFormContainer = document.getElementById("add-session-form-container");

  addSessionButton.addEventListener("click", function () {
    // Toggle images
    const images = addSessionButton.querySelectorAll(".form-button-image");
    images.forEach(
      (image) =>
        (image.style.display =
          image.style.display === "none" ? "inline" : "none")
    );

    // Toggle form with slide transition
    if (addSessionFormContainer.style.maxHeight) {
      addSessionFormContainer.style.maxHeight = null;
    } else {
      addSessionFormContainer.style.maxHeight = addSessionFormContainer.scrollHeight + 70 + "px";
    }
  });

  // Show/hide topic/task dropdown based on radio button selection
  const topicRadio = document.getElementById("topicRadio");
  const taskRadio = document.getElementById("taskRadio");
  const topicDropdown = document.getElementById("topicDropdown");
  const taskDropdown = document.getElementById("taskDropdown");

  topicRadio.addEventListener("change", function () {
    if (topicRadio.checked) {
      topicDropdown.style.display = "block";
      taskDropdown.style.display = "none";
      topicDropdown.setAttribute("required", "required");
      taskDropdown.removeAttribute("required");
    }
  });

  taskRadio.addEventListener("change", function () {
    if (taskRadio.checked) {
      topicDropdown.style.display = "none";
      taskDropdown.style.display = "block";
      taskDropdown.setAttribute("required", "required");
      topicDropdown.removeAttribute("required");
    }
  });
});


/* To dynamically populate the tasks and topics list */
$(document).ready(function() {
    // Populate subjects
    $.ajax({
        url: '/get-subjects/',
        dataType: 'json',
        success: function(data) {
            var subjectSelect = $('#subject');
            $.each(data.subjects, function(index, subject) {
                subjectSelect.append($('<option>', {
                    value: subject.id,
                    text: subject.name
                }));
            });
        }
    });

    // Handle subject selection
    $('#subject').change(function() {
        var selectedSubject = $(this).val();
        var date = $('#formattedDate').text();

        // Make AJAX request to get topics and tasks based on selected subject
        $.ajax({
            url: '/get-topics-and-tasks/',
            data: {
                subject_id: selectedSubject,
                date: date
            },
            dataType: 'json',
            success: function(data) {
                // Populate topics dropdown
                var topicSelect = $('#topic');
                topicSelect.empty();
                topicSelect.append($('<option>', {
                    value: '',
                    text: 'Select'
                }));
                $.each(data.topics, function(index, topic) {
                    topicSelect.append($('<option>', {
                        value: topic.id,
                        text: topic.name
                    }));
                });

                // Populate tasks dropdown
                var taskSelect = $('#task');
                taskSelect.empty();
                taskSelect.append($('<option>', {
                    value: '',
                    text: 'Select'
                }));
                $.each(data.tasks, function(index, task) {
                    taskSelect.append($('<option>', {
                        value: task.id,
                        text: task.name
                    }));
                });
            }
        });
    });

});

/* To perform form validations before sending the add-session request */
$('#add-session-form').submit(function(event) {
    event.preventDefault();

    // Get the values of start time and end time
    var startTime = $('#startTime').val();
    var endTime = $('#endTime').val();

    // Convert start time and end time to Date objects for comparison
    var startDate = new Date('1970-01-01T' + startTime);
    var endDate = new Date('1970-01-01T' + endTime);

    // Compare start time and end time
    if (endDate <= startDate) {
        // Show an error message or alert
        alert('End time must be greater than start time');
        // Prevent form submission
        return false;
    } else {
        // Check for intersections
        var intersectionCount = countIntersections(startTime, endTime);

        // If intersections found, prompt the user to confirm
        if (intersectionCount > 0) {
           var confirmMessage = "This session overwrites " + intersectionCount + " ";
            confirmMessage += (intersectionCount === 1) ? "session. Proceed anyway?" : "sessions. Proceed anyway?";
            var confirmResult = confirm(confirmMessage);

            // If user confirms, proceed with form submission
            if (!confirmResult) {
                return false;
            }
        }

        // Proceed with form submission
        var date = $('#formattedDate').text();
        var formData = $(this).serialize();
        formData += '&date=' + encodeURIComponent(date);
        $.ajax({
            url: '/add-session/',
            method: 'POST',
            data: formData,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            },
            success: function(response) {
                console.log("Session added successfully");
                window.location.reload(); // Reload the page
            },
            error: function(xhr, status, error) {
                console.log("Error adding session")
            }
        });
    }
});


/* To display user confirmation prompt before deleting the session */
$(document).ready(function() {
    $('.delete-session-btn').click(function(e) {
        e.preventDefault();
        var deleteUrl = $(this).attr('href');
        var confirmation = confirm("Are you sure you want to delete this session?");
        if (confirmation) {
            window.location.href = deleteUrl; // Proceed with the deletion
        }
    });
});



/* ******************************* Utility functions ******************************* */

// to get CSRF token from cookie to be able to send django server POST request
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i + 1) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/* To convert the date to the format of "%Y-%m-%d" to be able to pass to http request */
function formatDate(dateString) {
    var date = new Date(dateString);
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, '0'); // Month is zero-based
    var day = String(date.getDate()).padStart(2, '0');
    var formattedDate = year + '-' + month + '-' + day;
    return formattedDate;
}

/* find the number of session blocks the new block to be inserted overwrites */
function countIntersections(blockStart, blockEnd) {
    var timeParts1 = blockStart.split(':');
    var timeParts2 = blockEnd.split(':');
    var start1 = new Date(0, 0, 0, timeParts1[0], timeParts1[1]);
    var end1 = new Date(0, 0, 0, timeParts2[0], timeParts2[1]);
    var intersectionCount = 0;

    // Iterate over all children of the 'time-blocks' class
    $('.time-blocks').children().each(function() {
        // Check if the child is a session block by checking if it has a session class and if it doesn't have a button
        if (!$(this).hasClass('session') || $(this).find('button').length === 0) {
            return; // Continue to the next iteration if it doesn't have a 'session' class
        }

        // Get the start time and end time of the child
        var startTime = $(this).find('.top-overlap').text();
        var endTime = $(this).find('.bottom-overlap').text();
        var timeParts1 = startTime.split(':');
        var timeParts2 = endTime.split(':');
        var start2 = new Date(0, 0, 0, timeParts1[0], timeParts1[1]);
        var end2 = new Date(0, 0, 0, timeParts2[0], timeParts2[1]);

        // Check for intersection
        if (end2 <= start1 || end1 <= start2) {
            // Not intersecting
        } else {
            // Intersection found
            intersectionCount += 1;
        }
    });

    return intersectionCount;
};




