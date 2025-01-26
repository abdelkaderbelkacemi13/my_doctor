let inputPwd = '';


const cancelBtn = document.getElementById("cancelButton");
const pwd = document.getElementById('password');
const confirmPwd = document.getElementById('confirmPassword');
const pwdCheck = document.getElementById('pwdCheck');
const lenCheck = document.getElementById('len');
const numCheck = document.getElementById('num');
const caseCheck = document.getElementById('case');
const specCharCheck = document.getElementById('specialChar');
const errorMsg = document.getElementById('error');
const patientForm = document.getElementById('patient-registration');
const doctorForm = document.getElementById('doctor-registration');

// Manage the cancel button
if (cancelBtn) {
    cancelBtn.addEventListener('click', function () {
        if (patientForm) {
            patientForm.reset();
        }
        if (doctorForm) {
            doctorForm.reset();
        }
        if (errorMsg) {
            errorMsg.textContent = '';
        }
        if (pwdCheck) {
            pwdCheck.style.display = 'none';
        }
        if (lenCheck) {
            lenCheck.style.color = '';
        }
        if (numCheck) {
            numCheck.style.color = '';
        }
        if (caseCheck) {
            caseCheck.style.color = '';
        }
        if (specCharCheck) {
            specCharCheck.style.color = '';
        }
        if (confirmPwd) {
            confirmPwd.style.border = '';
        }
    });
}

// Password validation
if (pwd) {
    pwd.addEventListener('input', (ev) => {
        inputPwd = ev.target.value;
        if (inputPwd) {
            pwdCheck.style.display = 'block';
        }

        // Regular expressions
        const lenpt = /^.{8,16}$/; // Length between 8 and 16
        const nums = /(?=.*\d)/; // At least one number
        const cases = /(?=.*[A-Z])/; // At least one uppercase letter
        const spec = /(?=.*[!@#$%^&*()_+{}\[\]:;"'<>,.?/\\|`~-])/; // At least one special character

        lenpt.test(inputPwd) ? lenCheck.style.color = 'green' : lenCheck.style.color = 'red';
        nums.test(inputPwd) ? numCheck.style.color = 'green' : numCheck.style.color = 'red';
        cases.test(inputPwd) ? caseCheck.style.color = 'green' : caseCheck.style.color = 'red';
        spec.test(inputPwd) ? specCharCheck.style.color = 'green' : specCharCheck.style.color = 'red';
    });
}


//handle form submission
function FormSubmit(event, endpoint) {
    event.preventDefault();

    const password = document.getElementById("password").value;
    const confpwd = document.getElementById("confirmPassword").value;

    // Check if the password and the confirm password  matchs
    if (password !== confpwd) {
        errorMsg.textContent = "Passwords do not match.";
        return;
    }

    // Collect the data
    let usersdata = new FormData(event.target);

    fetch(endpoint, {
        method: 'POST',
        body: usersdata
    })
    .then(response => {
        if (response.ok) {
            // if the registration was success
            return response.json().then(data => {
                alert(data.message || "Registration successful!");
                window.location.href = "/login";
            });
            // if the email is already  used
        } else if (response.status === 409) {
            return response.json().then(data => {
                errorMsg.textContent = data.error || "Email already registered.";
            });
        } else {
            // if the registrasion failed
            return response.json().then(data => {
                errorMsg.textContent = data.error || "Registration failed.";
            }).catch(() => {
                errorMsg.textContent = "Registration failed.";
            });
        }
    })
    .catch(error => {
        console.error('Error during registration:', error);
        errorMsg.textContent = "Registration failed. Please try again.";
    });
}
[
    { form: doctorForm, endpoint: '/registerDoctor' },
    { form: patientForm, endpoint: '/registerPatient' },
].forEach(({ form, endpoint }) => {
    form?.addEventListener('submit', (event) => FormSubmit(event, endpoint));
});



