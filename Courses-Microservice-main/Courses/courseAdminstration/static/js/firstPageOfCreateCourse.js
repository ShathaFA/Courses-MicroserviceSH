// Get the button that opens the modal
var createCourseBtn = document.getElementById("createCourseBtn");

// Get the modal element
var createCourseModal = document.getElementById("createCourseModal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
createCourseBtn.onclick = function() {
  createCourseModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  createCourseModal.style.display = "none";
}

// When the user clicks outside of the modal, close it
window.onclick = function(event) {
  if (event.target == createCourseModal) {
    createCourseModal.style.display = "none";
  }
}
