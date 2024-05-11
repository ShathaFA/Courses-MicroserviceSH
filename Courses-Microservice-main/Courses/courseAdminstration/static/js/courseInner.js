document.addEventListener('DOMContentLoaded', function() {
    // Assuming the course ID is passed as a query parameter named 'courseId'
    const courseId = new URLSearchParams(window.location.search).get('courseId');
    if (courseId) {
        fetchCourseDetails(courseId);
    } else {
        console.error('Course ID not provided.');
    }
});

function fetchCourseDetails(courseId) {
    fetch(`/courses/courses/api/${courseId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(course => {
            // Update course details in the page
            document.getElementById('courseTitle').textContent = course.title;
            document.getElementById('courseTitleHeader').textContent = course.title;
            document.getElementById('courseCategory').textContent = course.category;
            document.getElementById('courseLevel').textContent = course.difficultyLevel;
            document.getElementById('courseDescription').textContent = course.description;
            
            // Assuming 'coursePic' is the URL to the course image
            if(course.coursePic) {
                document.querySelector('.coures-inner-img').src = course.coursePic;
            }

            // Update sections and lessons
            updateSections(course.sections);
        })
        .catch(error => {
            console.error('Error fetching course details:', error);
        });
}

function updateSections(sections) {
    const sectionsList = document.getElementById('sectionsList');
    sectionsList.innerHTML = ''; // Clear existing sections

    sections.forEach(section => {
        const sectionItem = document.createElement('li');
        sectionItem.className = 'list-sidenev';
        
        const sectionLink = document.createElement('a');
        sectionLink.href = '#';
        sectionLink.className = 'a-sidenev feat-btn';
        sectionLink.innerHTML = `${section.title} <span class="fas fa-caret-down first"></span>`;
        
        const lessonsList = document.createElement('ul');
        lessonsList.className = 'feat-show';

        section.lessons.forEach(lesson => {
            const lessonItem = document.createElement('li');
            const lessonLink = document.createElement('a');
            lessonLink.href = '#';
            lessonLink.textContent = lesson.title;
            lessonItem.appendChild(lessonLink);
            lessonsList.appendChild(lessonItem);
        });

        sectionItem.appendChild(sectionLink);
        sectionItem.appendChild(lessonsList);
        sectionsList.appendChild(sectionItem);
    });
}
