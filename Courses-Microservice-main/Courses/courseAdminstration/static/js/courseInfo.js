// This function extracts the courseId from a URL path of the form "/courses/<courseId>/"
function getCourseIdFromQuery() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('courseId');
}

const courseId = getCourseIdFromQuery();
const apiUrl = `/courses/courses/api/${courseId}/`; // Adjust based on your actual API endpoint

fetch(apiUrl)
  .then(response => response.json())
  .then(course => {

    updateCourseDetails(course);
    // Update course title
    document.querySelector('.courseinfo-CourseTitle').textContent = course.title;

    // Update instructor, you'll need to adjust this based on how your instructor data is structured
    // For this example, it's assumed to be just an ID or name
    document.querySelector('.courseinfo-infoSection .info div').textContent = `Course Instructor: ${course.instructor}`;

    // Update course description
    document.querySelector('.courseInfo-About p').textContent = course.description;

    // Assuming 'category' is a simple field, but you might need to adjust this
    // If categories are an array or a more complex structure, you'll need a loop to display them
    document.querySelector('.courseInfo-About .Category').textContent = course.category;

    document.getElementById('courseID').textContent = course.id;
    document.getElementById('difficultyLevel').textContent = course.difficultyLevel;
    document.getElementById('duration').textContent = course.duration;

    // Update more fields as necessary...

    // Update sections
    if (course.sections && course.sections.length > 0) {
        const sectionsContainer = document.getElementById('sectionsContainer');
        // Clear existing content
        sectionsContainer.innerHTML = '';
      
        course.sections.forEach(section => {
          // Create a new div for the section
          const sectionDiv = document.createElement('div');
          sectionDiv.classList.add('Sections-box'); // Assuming you have CSS styles for this class
      
          // Set the title and description
          const title = document.createElement('h3');
          title.textContent = section.title;
          title.id = 'Sections-title'; // IDs should be unique, consider not setting or using a class instead
      
          const description = document.createElement('p');
          description.textContent = section.description;
          description.id = 'Sections-description'; // Same note on uniqueness as above
      
          // Append title and description to the section div
          sectionDiv.appendChild(title);
          sectionDiv.appendChild(description);
      
          // Append the section div to the container
          sectionsContainer.appendChild(sectionDiv);
        });
      } else {
        // Handle case where there are no sections or course.sections is undefined
        document.getElementById('sectionsContainer').innerHTML = '<p>No sections available.</p>';
      }

  })
  .catch(error => console.error('Error fetching course data:', error));


  function updateCourseDetails(course) {
    // Other updates here (title, description, etc.)
    
    // Update the course image
    if(course.coursePic) {
        document.querySelector('.courseInfoRight img').src = course.coursePic;
    } else {
        // Handle cases where the coursePic might be null or undefined
        document.querySelector('.courseInfoRight img').src = '{% static "images/default.png" %}'; // A default image in case there's no coursePic
    }
}