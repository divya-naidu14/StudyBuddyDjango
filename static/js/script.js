/* ******************************* subjects.html page functions ******************************* */
/* To set properties for add-subject button in subjects.html page */
document.addEventListener("DOMContentLoaded", function () {
  const addSubjectButton = document.getElementById("add-subject-button");
  const addSubjectFormContainer = document.getElementById(
    "add-subject-form-container"
  );

  addSubjectButton.addEventListener("click", function () {
    // Toggle images
    const images = addSubjectButton.querySelectorAll(".form-button-image");
    images.forEach(
      (image) =>
        (image.style.display =
          image.style.display === "none" ? "inline" : "none")
    );

    // Toggle form container with slide transition
    if (addSubjectFormContainer.style.maxHeight) {
      addSubjectFormContainer.style.maxHeight = null;
    } else {
      addSubjectFormContainer.style.maxHeight =
        addSubjectFormContainer.scrollHeight + "px";
    }
  });
});


/* To trigger the delete subject method / To delete the selected subject */
function deleteSubject(subjectId) {
  if (confirm("Are you sure you want to delete this subject?")) {
    $.ajax({
      url: "/delete-subject/" + subjectId + "/",
      type: "POST",
      beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function (data) {
        // Handle success, such as removing the subject from the DOM
        console.log("Subject deleted successfully");
        window.location.reload();
      },
      error: function (xhr, textStatus, errorThrown) {
        // Handle error
        console.error("Error deleting subject:", textStatus);
      },
    });
  }
}

/* ******************************* topicsAndTasks.html page functions ******************************* */
/* To set properties for add-topic button in topicsAndTasks.html page */
document.addEventListener("DOMContentLoaded", function () {
  const addTopicButton = document.getElementById("add-topic-button");
  const addTopicFormContainer = document.getElementById(
    "add-topic-form-container"
  );

  addTopicButton.addEventListener("click", function () {
    // Toggle images
    const images = addTopicButton.querySelectorAll(".form-button-image");
    images.forEach(
      (image) =>
        (image.style.display =
          image.style.display === "none" ? "inline" : "none")
    );

    // Toggle form container with slide transition
    if (addTopicFormContainer.style.maxHeight) {
      addTopicFormContainer.style.maxHeight = null;
    } else {
      addTopicFormContainer.style.maxHeight =
        addTopicFormContainer.scrollHeight + "px";
    }
  });
});


/* To trigger the delete-topic button in topicsAndTasks.html page */
function deleteTopic(topicId) {
  if (confirm("Are you sure you want to delete this topic?")) {
    $.ajax({
      url: "/delete-topic/" + topicId + "/",
      type: "POST",
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function(data) {
        // Handle success, such as removing the topic from the DOM
        console.log("Topic deleted successfully");
        window.location.reload(); // Reload the page
      },
      error: function(xhr, textStatus, errorThrown) {
        // Handle error
        console.error("Error deleting topic:", textStatus);
      },
    });
  }
}


/* To set properties for add-task button in topicsAndTasks.html page */
document.addEventListener("DOMContentLoaded", function () {
  const addTaskButton = document.getElementById("add-task-button");
  const addTaskFormContainer = document.getElementById("add-task-form-container");

  addTaskButton.addEventListener("click", function () {
    // Toggle images
    const images = addTaskButton.querySelectorAll(".form-button-image");
    images.forEach(
      (image) =>
        (image.style.display =
          image.style.display === "none" ? "inline" : "none")
    );

    // Toggle form container with slide transition
    if (addTaskFormContainer.style.maxHeight) {
      addTaskFormContainer.style.maxHeight = null;
    } else {
      addTaskFormContainer.style.maxHeight = addTaskFormContainer.scrollHeight + "px";
    }
  });
});

/* To verify that the deadline date entered by the user for add task is greater than or equal to today's date in the
   topicsAndTasks.html page */
document.getElementById('add-task-form').addEventListener('submit', function(event) {
    var deadlineInput = document.getElementById('deadline').value;
    var today = new Date().toISOString().slice(0, 10);

    if (deadlineInput < today) {
        document.getElementById('deadline-error').innerText = 'Deadline date must be greater than or equal to today';
        event.preventDefault();
    } else {
        document.getElementById('deadline-error').innerText = '';
    }
});


/* ******************************* templates.html page functions ******************************* */
/* To set the selected day from dropdown in templates page */
function setSelectedDay(day) {
  document.getElementById("daySelectorDropdownMenuButton").innerText = day;
}


/* ******************************* general utility functions ******************************* */
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
