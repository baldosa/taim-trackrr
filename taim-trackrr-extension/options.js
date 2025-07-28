// Saves the settings in input values to Chrome storage
async function saveSettings(formData) {

  const username = document.getElementById('username');
  const password = document.getElementById('password');
  const serverUrlInput = document.getElementById('serverUrlInput');

  if (!username.value || !password.value || !serverUrlInput.value) {
    showPopup('Please fill in all fields.');
    return;
  }

  const response = await fetch(`${serverUrlInput.value}/api/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: `grant_type=password&username=${username.value}&password=${password.value}`
  });

  if (!response.ok) {
    showPopup('Login failed.');
    return;
  }

  const data = await response.json();
  if (data) {
    // Save the token and server URL in Chrome storage
    const settings = {
      token: data.access_token,
      serverUrl: serverUrlInput.value
    };

    chrome.storage.sync.set({ settings }, () => {
      showPopup('Settings saved!');
      hideLoginForm(settings.serverUrl);
    });

  } else {
    showPopup('Failed to retrieve token.');
  }


}

// Display a temporary popup message
function showPopup(message) {
  const popup = document.createElement('div');
  popup.textContent = message;
  popup.className = 'popup';
  document.body.appendChild(popup);

  setTimeout(() => {
    popup.classList.add('fade-out');
    setTimeout(() => {
      document.body.removeChild(popup);
    }, 500); // match with fade-out transition duration
  }, 2000);
}

function hideLoginForm(serverUrl) {
  const form = document.querySelector('form');
  const container = document.querySelector('.container');

  form.hidden = true; // Hide the form if settings are already saved

  const statusDiv = document.createElement('p');
  statusDiv.textContent = `Connected to: ${serverUrl}`;
  statusDiv.className = 'status';
  container.appendChild(statusDiv);

  const logoutButton = document.createElement('button');
  logoutButton.classList.add('btn');
  logoutButton.textContent = 'Logout';
  logoutButton.addEventListener('click', () => {
    chrome.storage.sync.remove('settings', () => {
      showPopup('Logged out successfully.');
      location.reload(); // Reload the page to reset the form
    });
  });
  container.appendChild(logoutButton);
}

// Initializes the options page by setting up event listeners
document.addEventListener('DOMContentLoaded', () => {
  // Prevent default form submission
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      saveSettings();
    });
  }

  // Load the saved settings from Chrome storage
  chrome.storage.sync.get('settings', data => {
    if (data.settings) {
      hideLoginForm(data.settings.serverUrl);
    }
  });
});