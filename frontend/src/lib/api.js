const API_BASE_URL = import.meta.env.PUBLIC_API_URL || '';

async function apiCall(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const config = { ...defaultOptions, ...options };

  if (config.body && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body);
  }

  try {
    const response = await fetch(url, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || `HTTP ${response.status}`);
    }
    
    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export async function getPrograms() {
  return apiCall('/api/method/peace_league_website.api.get_programs');
}

export async function getHomepageData() {
  return apiCall('/api/method/peace_league_website.api.get_homepage_data');
}

export async function getVolunteers() {
  return apiCall('/api/method/peace_league_website.api.get_volunteers');
}

export async function getChapters() {
  return apiCall('/api/method/peace_league_website.api.get_chapters');
}

export async function submitVolunteer(data) {
  return apiCall('/api/method/peace_league_website.api.create_volunteer', {
    method: 'POST',
    body: data,
  });
}

export async function submitDonation(data) {
  return apiCall('/api/method/peace_league_website.api.create_donation', {
    method: 'POST',
    body: data,
  });
}

export async function submitContact(data) {
  return apiCall('/api/method/peace_league_website.api.submit_contact_form', {
    method: 'POST',
    body: data,
  });
}

export async function getProgramDetails(name) {
  return apiCall(`/api/method/peace_league_website.api.get_program_details?name=${encodeURIComponent(name)}`);
}
