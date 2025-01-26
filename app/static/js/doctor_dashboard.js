document.addEventListener('DOMContentLoaded', () => {
    // Handling the  Approve or Decline actions
    document.querySelectorAll('.approve, .decline').forEach(button => {
        button.addEventListener('click', async (event) => {
            const appointmentId = event.target.dataset.appointmentId;
            const action = event.target.classList.contains('approve') ? 'approve' : 'decline';

            try {
                const response = await fetch(`/updateAppointment`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 'approved':action,
                        'id':appointmentId
                     }),
                });
                console.log(response)

                if (response.ok) {
                    window.location.reload();
                } else {
                    alert('Action failed. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    });
});

