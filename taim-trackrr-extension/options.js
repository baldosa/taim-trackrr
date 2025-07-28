// Saves the settings in input values to Chrome storage
function saveSettings() {
  console.log('Saving settings...');
  const tokenInput = document.getElementById('tokenInput');
  const refreshTokenInput = document.getElementById('refreshTokenInput');
  const serverUrlInput = document.getElementById('serverUrlInput');

  const settings = {
    token: tokenInput.value,
    refreshToken: refreshTokenInput.value,
    serverUrl: serverUrlInput.value
  };

  chrome.storage.sync.set({ settings }, () => {
    showPopup('Settings saved!');
  });
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
// Initializes the options page by setting up event listeners
document.addEventListener('DOMContentLoaded', () => {
  // Get all buttons and add click event listeners
  const buttons = document.querySelectorAll('.color-button');
  buttons.forEach(button => {
    button.addEventListener('click', handleButtonClick);
  });

  // Get the save button and add a click event listener
  const saveButton = document.getElementById('saveButton');
  saveButton.addEventListener('click', saveSettings);

  // Load the saved settings from Chrome storage
  chrome.storage.sync.get('settings', data => {
    if (data.settings) {
      document.getElementById('tokenInput').value = data.settings.token;
      document.getElementById('refreshTokenInput').value = data.settings.refreshToken;
      document.getElementById('serverUrlInput').value = data.settings.serverUrl;
    }
  });
});