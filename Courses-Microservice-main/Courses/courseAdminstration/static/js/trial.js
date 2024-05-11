// Ensuring the DOM is fully loaded before executing the script

$(document).ready(function () {
  // Sets up global AJAX request settings, particularly for CSRF token handling

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      // Check if the method needs CSRF protection and if it's not a cross-domain request

      if (
        !/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) &&
        !this.crossDomain
      ) {
        // Set CSRF token header for the request from hidden form field

        xhr.setRequestHeader(
          "X-CSRFToken",
          $('input[name="csrfmiddlewaretoken"]').val()
        );
      }
    },
  });

  // Toggle sidebar visibility when button with class `btn` is clicked
  $(".btn").click(function () {
    $(".sidebar").toggleClass("collapsed");
  });

  // Toggle visibility of features under `.feat-btn` using event delegation
  $(document).on("click", ".feat-btn", function () {
    // Since the `.feat-show` is no longer the direct next sibling, adjust the selector
    $(this).closest("li").find(".feat-show").slideToggle();
    $(this).find(".fa-caret-down").toggleClass("rotate");
});

  // Similar toggle functionality for `.serv-btn` elements
  $(document).on("click", ".serv-btn", function () {
    $(this).next(".serv-show").slideToggle();
    $(this).find(".fa-caret-down").toggleClass("rotate");
  });

  // Opens modal and stores section ID when `.addLessonBtn` is clicked
  $(document).on("click", ".addLessonBtn", function () {
    var sectionId = $(this).closest("li.list-sidenev").data("section-id"); // Retrieve the section ID
    $("#createLessonModal")
      .data("sectionId", sectionId)
      .css("display", "block"); // Store it in the modal for later use
  });

  // Display the create section modal
  $("#createSectionBtn").click(function () {
    $("#createSectionModal").css("display", "block");
  });

  // Close modal windows
  $(".close").click(function () {
    $(this).closest(".modal").css("display", "none");
  });
  // Close modals by clicking outside of them

  window.onclick = function (event) {
    if (event.target == document.getElementById("createSectionModal")) {
      document.getElementById("createSectionModal").style.display = "none";
    }
    if (event.target == document.getElementById("createLessonModal")) {
      document.getElementById("createLessonModal").style.display = "none";
    }
  };

  // Form submission handler for sections, preventing default form behavior
  $("#sectionForm").submit(function (event) {
    event.preventDefault();
    const courseId = getCourseIdFromURL();
    var sectionTitle = $("#sectionTitle").val();
    var sectionDesc = $("#sectionDesc").val();
    var postData = {
      title: sectionTitle,
      description: sectionDesc,
    };

    // AJAX POST request to add a new section
    $.ajax({
      url: `/addSection/api/${courseId}/`, // Adjust this URL to your API endpoint
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(postData),
      success: function (section) {
        console.log("Section created successfully:", section);
        appendNewSectionToUI(section);
        $("#createSectionModal").css("display", "none"); // Close the modal on success
      },
      error: function (xhr, status, error) {
        console.error("Failed to create section:", xhr.responseText);
        alert("Failed to create section. Please try again.");
      },
    });
  });

  // Function to append a new section to the UI dynamically

  function appendNewSectionToUI(section) {
    var $sectionList = $(".sidebar > ul");
    var $section = $("<li>")
      .addClass("list-sidenev")
      .data("section-id", section.id);
    var $sectionLink = $("<a>")
      .addClass("sectionTitle a-sidenev feat-btn")
      .attr("href", "#")
      .text(section.title);
    var $caret = $("<span>").addClass("fas fa-caret-down first");
    $sectionLink.append($caret);

    var $lessonsList = $("<ul>").addClass("feat-show").css("display", "none");
    $lessonsList.append(
      $("<li>").append(
        $("<a>")
          .addClass("addLessonBtn")
          .attr("href", "#")
          .text("Add New Lesson")
      )
    );

    $section.append($sectionLink).append($lessonsList);
    $sectionList.append($section);
  }

  // Function to extract course ID from the URL
  function getCourseIdFromURL() {
    var pathname = window.location.pathname;
    var segments = pathname.split("/");
    return segments[segments.length - 2]; // Adjust if necessary based on your URL structure
  }

  // Form submission handler for lessons, preventing default behavior

  $("#lessonForm").submit(function (event) {
    event.preventDefault();
    var sectionId = $("#createLessonModal").data("sectionId"); // Retrieve the stored section ID
    var lessonTitle = $("#lessonTitle").val();

    // AJAX POST request to add a new lesson

    $.ajax({
      url: `/addLesson/api/${sectionId}/`,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ title: lessonTitle }),
      success: function (lesson) {
        $("#createLessonModal").css("display", "none");
        appendNewLessonToUI(lesson, sectionId);
        alert("Lesson added successfully!");
      },
      error: function (xhr) {
        alert("Failed to add lesson. Please try again.");
        console.error("Error:", xhr.responseText);
      },
    });
  });

  // Function to append a new lesson to the UI dynamically

  function appendNewLessonToUI(lesson, sectionId) {
    var $lessonsList = $(
      'li.list-sidenev[data-section-id="' + sectionId + '"]'
    ).find(".feat-show");
    // Create the new lesson element with lesson ID
    var $lessonItem = $("<li>").data("lesson-id", lesson.id);
    var $lessonLink = $("<a>")
      .addClass("lessonTitle")
      .attr("href", "#")
      .text(lesson.title)
      .data("content", lesson.contents || []);
    $lessonItem.append($lessonLink);
    $lessonsList.append($lessonItem);
  }

  // Function to fetch course details and update UI dynamically
  function fetchCourseDetails() {
    const courseId = getCourseIdFromURL(); // Ensure this ID is fetched correctly
    $.ajax({
      url: `/courseInner/api/${courseId}/`,
      type: "GET",
      dataType: "json",
      success: function (course) {
        updateCourseDetails(course);
      },
      error: function (error) {
        console.error("Failed to fetch course details:", error);
      },
    });
  }

  // Function to update course details in the UI based on fetched data

  function updateCourseDetails(course) {
    $(".courseTitle").text(course.title);
    $(".Course-Title").text(course.title);
    $(".Course-topic").text(course.category);
    $(".Course-deficality").text(course.difficultyLevel);
    $(".Course-description").text(course.description);
    $(".coures-inner-img").attr(
      "src",
      course.coursePic || "/path/to/default/image.jpg"
    );

    $(".sidebar > ul").empty(); // Clear previous content

    course.sections.forEach(function (section) {
      var sectionEl = $("<li>")
        .addClass("list-sidenev")
        .data("section-id", section.id);
    
      // Create a container for the section title and icons
      var sectionContainer = $("<div>").addClass("section-container");
    
      var editIcon = $("<span>")
        .addClass("fas fa-edit edit-section")
        .attr("title", "Edit Section")
        .data("section-id", section.id); // Ensure the icon carries the section ID for functionality
    
      var deleteIcon = $("<span>")
        .addClass("fas fa-trash delete-section")
        .attr("title", "Delete Section")
        .data("section-id", section.id); // Ensure the icon carries the section ID for functionality
    
      var sectionLink = $("<a>")
        .addClass("sectionTitle a-sidenev feat-btn")
        .attr("href", "#")
        .text(section.title); // Append the text directly
        sectionLink.append($("<span>").addClass("fas fa-caret-down first")); // Caret icon
    
      // Append the icons and title to the section container
      sectionContainer.append(editIcon, deleteIcon,sectionLink);
    
      var lessonsList = $("<ul>").addClass("feat-show").css("display", "none");
    
      lessonsList.append(
        $("<li>").append(
          $("<a>")
            .addClass("addLessonBtn")
            .attr("href", "#")
            .text("Add New Lesson")
        )
      );
    
      section.lessons.forEach(function (lesson) {
        var $lessonItem = $("<li>").data("lesson-id", lesson.id);
        var $lessonContainer = $("<div>").addClass("lesson-container");
    
        var editIcon = $("<span>")
          .addClass("fas fa-edit edit-lesson")
          .attr("title", "Edit Lesson")
          .data("lesson-id", lesson.id);
    
        var deleteIcon = $("<span>")
          .addClass("fas fa-trash delete-lesson")
          .attr("title", "Delete Lesson")
          .data("lesson-id", lesson.id);
    
        var $lessonLink = $("<a>")
          .addClass("lessonTitle")
          .attr("href", "#")
          .data("content", lesson.contents)
          .data("lesson-id", lesson.id)
          .text(lesson.title);
    
        $lessonContainer.append(editIcon, deleteIcon, $lessonLink);
        $lessonItem.append($lessonContainer);
        lessonsList.append($lessonItem);
      });
    
      // Append the section container and lessons list to the section element
      sectionEl.append(sectionContainer).append(lessonsList);
      $(".sidebar > ul").append(sectionEl);
    });
    
  }

  // Initial fetch of course details to populate UI

  fetchCourseDetails();

  // Initially hide course content and form sections
  $(".course-content").hide();
  $(".form1").hide();

  // Toggle visibility of course content on clicking the course title
  $("#courseTitle").click(function () {
    $(".course-content").slideToggle(); // Toggle visibility of course content
    $(".form1").hide(); // Ensure the editor is hidden
  });

  // Load content into the editor when a lesson title is clicked
  $(document).on("click", ".lessonTitle", function () {
    $(".course-content").hide(); // Hide course content
    $(".form1").show(); // Make sure the editor is shown
    var contents = $(this).data("content"); // This is an array of objects
    var contentString = contents.map((content) => content.reference).join(" "); // Join all references with a space
    if (quill) {
      quill.root.innerHTML = contentString; // Load the concatenated string into Quill
    } else {
      console.error("Quill not initialized");
    }
  });


  $(document).on("click", ".edit-lesson", function() {
    var lessonId = $(this).data('lesson-id'); // Retrieve the lesson ID stored in the icon's data attribute
    var currentTitle = $(this).siblings('.lessonTitle').text(); // Assuming the title is in an element with class 'lessonTitle' near the icon

    // Fill in the modal inputs
    $('#editLessonModal #lessonTitle').val(currentTitle);
    $('#editLessonModal').data('lessonId', lessonId); // Store the lesson ID in the modal for later use

    // Show the modal
    $('#editLessonModal').css("display", "block");
});





$('#editLessonForm').submit(function(event) {
  event.preventDefault();
  var lessonId = $('#editLessonModal').data('lessonId'); // Retrieve the stored lesson ID
  var newTitle = $('#editLessonModal #lessonTitle').val();

  // AJAX POST request to update the lesson
  $.ajax({
      url: `/editLesson/api/${lessonId}/`, // API endpoint for updating lesson
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ title: newTitle }),
      success: function(response) {
          // Update the lesson title in the UI
          $('li[data-lesson-id="' + lessonId + '"] .lessonTitle').text(newTitle);
          $('#editLessonModal').css("display", "none");
          alert("Lesson updated successfully!");
      },
      error: function(xhr) {
          alert("Failed to update the lesson. Please try again.");
          console.error("Error:", xhr.responseText);
      }
  });
});

});

// Quill.js editor initialization for rich text editing
var quill = new Quill("#editor-container", {
  theme: "snow", // Specify theme, 'snow' is one of the built-in themes
});

// Handling form submission with rich text data
document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("form").addEventListener("submit", function (event) {
    var descriptionHtml = document.querySelector(".ql-editor").innerHTML;
    var descriptionTextArea = document.querySelector(
      'textarea[name="description"]'
    );
    descriptionTextArea.value = descriptionHtml;
  });
});

// AJAX calls for deleting sections with confirmation
$(document).on("click", ".delete-section", function () {
  var sectionId = $(this).closest("li.list-sidenev").data("section-id");
  if (confirm("Are you sure you want to delete this section?")) {
    $.ajax({
      url: `/deleteSection/api/${sectionId}/`, // Updated to Users microservice URL
      type: "DELETE",
      success: function () {
        alert("Section deleted successfully!");
        window.location.reload(); // Reload the page or dynamically remove the section from UI
      },
      error: function (xhr) {
        alert("Failed to delete the section.");
        console.error("Error:", xhr.responseText);
      },
    });
  }
});

// AJAX calls for deleting lessons with lesson ID retrieval and confirmation
$(document).on("click", ".delete-lesson", function () {
  var lessonId = $(this).closest("li").data("lesson-id"); // Retrieve lesson ID correctly
  console.log(lessonId);

  if (lessonId && confirm("Are you sure you want to delete this lesson?")) {
    $.ajax({
      url: `/deleteLesson/api/${lessonId}/`, // Updated to Users microservice URL
      type: "DELETE",
      success: function () {
        alert("Lesson deleted successfully!");
        window.location.reload();
      },
      error: function (xhr) {
        alert("Failed to delete the lesson.");
        console.error("Error:", xhr.responseText);
      },
    });
  }
});

