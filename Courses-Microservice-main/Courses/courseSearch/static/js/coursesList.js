
$(document).ready(function() {
    function fetchCourses(searchQuery) {
        $.ajax({
            url: '/search/',
            type: 'GET',
            data: { q: searchQuery },  // Pass the search query as data
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
                    <div class="students"><span class="emoji">&#128100;</span> ${course.enrolled_students || '0'}</div>
                    <div class="lessons"><span class="emoji">&#128214;</span> 10</div>
                    <div class="instructor"><span class="emoji">&#128188;</span> ${course.instructor}</div>
                    <div class="reviews">⭐⭐⭐⭐⭐

<p>${course.rating}</p></div>
                </div>
            </div>`;
            courseSection.append(courseHTML);
        });

        if (courses.length === 0) {
            courseSection.html('<p>No courses available at this time.</p>');
        }
    }

    function toggleDropdown() {
        document.getElementById("categoryDropdown").classList.toggle("show");
    }

    function searchCategory() {
        var input, filter, ul, li, a, i;
        input = document.getElementById("categorySearchInput");
        filter = input.value.toUpperCase();
        div = document.getElementById("categoryDropdown");
        a = div.getElementsByTagName("a");
        for (i = 0; i < a.length; i++) {
            txtValue = a[i].textContent || a[i].innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                a[i].style.display = "";
            } else {
                a[i].style.display = "none";
            }
        }
    }

    fetchCourses('');

    $('#course-section').on('click', '.course-info', function() {
        const courseId = $(this).data('course-id');
        console.log("Clicked Course ID:", courseId);  // Check if the course ID is fetched correctly
        window.location.href = `/courseInfo/${courseId}/`;  // Ensure your Django URL pattern matches this
    });

    // Event listeners for dropdown and search
    $('#categoryDropdown').on('click', toggleDropdown);
    $('#categorySearchInput').on('keyup', searchCategory);
});
