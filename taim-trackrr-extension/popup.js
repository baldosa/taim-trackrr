// Initialize button with users' preferred color
const startTracker = document.getElementById('startTracker');

// When the button is clicked, inject setPageBackgroundColor into current page
startTracker.addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: toggleTimer
  });
  // window.close();

});

// The body of this function will be executed as a content script inside the
// current page
async function toggleTimer() {
  settings = await chrome.storage.sync.get('settings');

  // Send a message to the server to start the timer
  const response = await fetch(`${settings.settings.serverUrl}/api/timer`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${settings.settings.token}`
    }
  })
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
}

async function stopTimer() {
  settings = await chrome.storage.sync.get('settings');

  // Send a message to the server to stop the timer
  const response = await fetch(`${settings.settings.serverUrl}/api/timer`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${settings.settings.token}`
    }
  })
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
}


async function checkTimer() {
  settings = await chrome.storage.sync.get('settings');

  // Send a message to the server to start the timer
  const response = await fetch(`${settings.settings.serverUrl}/api/timer`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${settings.settings.token}`
    }
  })
  if (response.status === 200) {
    jsonResponse = await response.json();
    chrome.storage.sync.set({ response: jsonResponse });

    // const timeStartDiv = document.getElementById('timeStart');
    // timeStartDiv.innerHTML = jsonResponse.start_time;
    startTracker.textContent = 'Stop';
    startTracker.style.backgroundColor = '#dc3545';

  } else if (response.status === 404) {
    startTracker.textContent = 'Start';
    startTracker.style.backgroundColor = '#28a745';
  }
}


// Initializes the options page by setting up event listeners
document.addEventListener('DOMContentLoaded', () => {
  checkTimer();

});