document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission

            const formData = new FormData(form);
            const params = new URLSearchParams(formData);

            fetch('/ip_addr/?' + params.toString(), {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Mark as AJAX request
                }
            })
            .then(response => response.json())
            .then(data => {
                // Clear all result areas
                document.getElementById('netmask_result_display').innerHTML = '';
                document.getElementById('cidr_result_display').innerHTML = '';
                document.getElementById('netmask_v6_result_display').innerHTML = '';
                document.getElementById('host_list_display').innerHTML = '';
                document.getElementById('host_list_error_display').innerHTML = '';

                // Update the appropriate result area
                if (data.netmask_result) {
                    document.getElementById('netmask_result_display').innerHTML = data.netmask_result;
                } else if (data.cidr_result) {
                    document.getElementById('cidr_result_display').innerHTML = data.cidr_result;
                } else if (data.netmask_v6_result) {
                    document.getElementById('netmask_v6_result_display').innerHTML = data.netmask_v6_result;
                } else if (data.host_list) {
                    let hostListHTML = '<ul>';
                    data.host_list.forEach(host => {
                        hostListHTML += `<li>${host}</li>`;
                    });
                    hostListHTML += '</ul>';
                    document.getElementById('host_list_display').innerHTML = hostListHTML;
                } else if (data.host_list_error) {
                    document.getElementById('host_list_error_display').innerHTML = data.host_list_error;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
