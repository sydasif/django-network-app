document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(form);
        const params = new URLSearchParams(formData);

        fetch('/ping/?' + params.toString(), {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // Mark as AJAX request
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('ping_result_display').innerHTML = data.test_result || '';
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
