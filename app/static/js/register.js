let inputPwd = '';
let confPwd = '';

// Get DOM elements
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

// Manage the cancel button to reset the form
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

        // Regular expressions for password validation
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

// Confirm password validation
if (confirmPwd) {
    confirmPwd.addEventListener('input', (ev) => {
        confPwd = ev.target.value;
        if (confPwd !== inputPwd) {
            confirmPwd.style.border = 'solid 1px red';
            errorMsg.textContent = "Passwords do not match.";
        } else {
            confirmPwd.style.border = 'transparent';
            errorMsg.textContent = '';
        }
    });
}




