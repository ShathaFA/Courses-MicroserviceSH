$(document).ready(function() {
    function fetchCourses() {
        $.ajax({
            url: 'api/', // Adjust to match your actual API endpoint
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                updateCourseSection(data);
            },
            error: function(error) {
                console.error('Error fetching courses:', error);
            }
        });
    }

    function updateCourseSection(courses) {
        let courseSection = $('#course-section');
        courseSection.empty(); // Clear existing content

        courses.forEach(function(course) {
            let courseHTML = `
            <div class="course-info" data-course-id="${course.id}">
                <img class="course-image" src="${course.coursePic}" alt="${course.title}" />
                <div class="course-title">${course.title}</div>
                <div class="course-details">
                    <div class="category">${course.category}</div>
                    <div class="hours"><span class="emoji">&#9200;</span> ${course.duration} hours</div>
                    <div class="students"><span class="emoji">&#128100;</span> 500</div>
                    <div class="lessons"><span class="emoji">&#128214;</span> 10</div>
                    <div class="instructor"><span class="emoji">&#128188;</span> ${course.instructor}</div>
                    <div class="reviews">⭐⭐⭐⭐⭐<p>1K</p></div>
                </div>
            </div>`;
            courseSection.append(courseHTML);
        });

        if(courses.length === 0) {
            courseSection.html('<p>No courses available at this time.</p>');
        }
    }

    fetchCourses();

    // Delegating the click event to the parent container
    $('#course-section').on('click', '.course-info', function() {
        const courseId = $(this).data('course-id');
        window.location.href = `/courses/courseinfo/?courseId=${courseId}`;
    });
});
