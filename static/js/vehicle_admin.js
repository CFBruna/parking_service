document.addEventListener('DOMContentLoaded', function () {
    const licensePlateInput = document.getElementById('id_license_plate');
    const vehicleTypeSelect = document.getElementById('id_vehicle_type');
    const ownerSelect = document.getElementById('id_owner');

    if (licensePlateInput) {
        licensePlateInput.addEventListener('blur', function () {
            const licensePlate = this.value.trim();

            if (licensePlate) {
                const payload = {
                    license_plate: licensePlate,
                    vehicle_type: vehicleTypeSelect ? parseInt(vehicleTypeSelect.value) || null : null,
                    owner: ownerSelect ? parseInt(ownerSelect.value) || null : null
                };

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
                const csrftoken = getCookie('csrftoken');

                fetch('/api/v1/vehicles/get-by-plate/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(payload)
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data && data.admin_url) {
                            window.location.href = data.admin_url;
                        }
                    })
                    .catch(error => console.error('Erro ao processar veículo:', error));
            }
        });
    }
});
