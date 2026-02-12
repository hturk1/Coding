// Save selected role
const roleButtons = document.querySelectorAll('.role-btn');
if (roleButtons) {
  roleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const role = btn.getAttribute('data-role');
      localStorage.setItem('selectedRole', role);
      window.location.href = 'login.html';
    });
  });
}

// Display selected role on login page
const roleTitle = document.getElementById('role-title');
if (roleTitle) {
  const role = localStorage.getItem('selectedRole');
  if (role) {
    roleTitle.textContent = `Sign in as ${role.charAt(0).toUpperCase() + role.slice(1)}`;
  }
}

// Login form submission
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const role = localStorage.getItem('selectedRole');

    if (!role) {
      alert('Please select your role first.');
      window.location.href = 'index.html';
      return;
    }

    // TODO: replace with backend call
    console.log(`Attempting login for ${role} with ${email}`);
    alert(`Logged in as ${role}!`);
  });
}

// Password reset form
const resetForm = document.getElementById('resetForm');
if (resetForm) {
  resetForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('resetEmail').value.trim();
    const role = localStorage.getItem('selectedRole');
    alert(`If an account exists for ${email}, a password reset link will be sent.`);
    window.location.href = 'login.html'; // Redirect back after reset
  });
}
