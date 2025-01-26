document.addEventListener('DOMContentLoaded', function () {
    const specialitySelect = document.getElementById('speciality-select');
    const doctorsList = document.getElementById('doctors-list');
    const appointmentDateInput = document.getElementById('appointment-date');
    const submitRequestButton = document.getElementById('submit-request');

    let doctorsData = [];
    let selectedDoctor = null;

    // Fetch doctors data from the backend (replace with your actual API endpoint)
    fetch('/doctors')
        .then(response => response.json())
        .then(data => {
            doctorsData = data;
            console.log(data)
        })
        .catch(error => {
            console.error('Error fetching doctors data:', error);
        });

    // Event listener for specialty selection
    specialitySelect.addEventListener('change', function () {
        const selectedSpeciality = specialitySelect.value;
        doctorsList.innerHTML = ''; // Clear the list
        selectedDoctor = null; // Reset selected doctor

        if (selectedSpeciality) {
            const filteredDoctors = doctorsData.filter(doctor => doctor.specialization === selectedSpeciality);
            displayDoctors(filteredDoctors);
        }
    });

    // Function to display doctors in the list
    function displayDoctors(doctors) {
        doctors.forEach(doctor => {
            const listItem = document.createElement('li');
            listItem.textContent = `${doctor.first_name} ${doctor.last_name} - ${doctor.specialization}`;

            // Restore selection if this doctor was previously selected
            if (selectedDoctor && selectedDoctor.id === doctor.id) {
                listItem.classList.add('selected');
            }

            // Add click event listener to select the doctor
            listItem.addEventListener('click', function () {
                // Remove 'selected' class from all list items
                const allDoctorItems = doctorsList.querySelectorAll('li');
                allDoctorItems.forEach(item => item.classList.remove('selected'));

                // Add 'selected' class to the clicked list item
                listItem.classList.add('selected');

                // Update selectedDoctor variable
                selectedDoctor = doctor;
                console.log('Selected doctor:', selectedDoctor);
            });

            doctorsList.appendChild(listItem);
        });
    }

    // Event listener for submit request button
    submitRequestButton.addEventListener('click', function () {
        const selectedDate = appointmentDateInput.value;

        // Validate selected date and doctor
        if (!selectedDate || !selectedDoctor) {
            alert('Please select a date and a doctor.');
            return;
        }

        // Send appointment request to the backend (replace with your actual API endpoint)
        fetch('/bookAppointments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                doctor_email: selectedDoctor.email,
                doctors_specialization: selectedDoctor.specialization,
                date: selectedDate
            })
        })
            .then(response => response.json())
            .then(data => {
                // Handle response (e.g., show success message)
                alert(data.msg);
                window.location.href = '/patient/appointments'
            })
            .catch(error => {
                console.error('Error submitting appointment request:', error);
                alert(data.msg);
            });
    });
});
