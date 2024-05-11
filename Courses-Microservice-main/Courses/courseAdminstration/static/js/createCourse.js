function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('createCourseForm');
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);
        // Assuming 'CourseInstructor' is the correct field name expected by your API,
        // but ensure this matches your Django model and serializer fields.
        formData.append('instructor', document.getElementById('CourseInstructor').value); 
        formData.append('category', document.getElementById('courseCategory').value);
        formData.append('title', document.getElementById('courseTitle').value);
        formData.append('description', document.getElementById('courseDescription').value);
        formData.append('difficultyLevel', document.getElementById('difficultyLevel').value);
        formData.append('duration', document.getElementById('duration').value);
        // The file field is directly appended through the form data construction.

        fetch('api/', { // Ensure this URL is correct
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: formData, // FormData will correctly handle the file upload
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            alert("Course created successfully!");
            // Optionally, reset the form or redirect the user
            // form.reset();
            // window.location.href = 'some-success-page';
        })
        .catch((error) => {
            console.error('Error:', error);
            alert("Error creating course. Please try again.");
        });
    });
});
