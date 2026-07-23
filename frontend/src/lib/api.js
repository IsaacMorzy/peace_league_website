const API_BASE_URL = import.meta.env.PUBLIC_API_URL || '';

async function apiCall(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const config = { ...defaultOptions, ...options };

  if (config.body instanceof FormData) {
    // Let the browser set multipart/form-data Content-Type with boundary
    delete config.headers['Content-Type'];
  } else if (config.body && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body);
  }

  try {
    const response = await fetch(url, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || `HTTP ${response.status}`);
    }
    
    // Frappe wraps API responses in {"message": {...}}, unwrap it
    if (data.message && typeof data.message === 'object' && data.message.status) {
      return data.message;
    }
    
    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export async function getCauses() {
  return apiCall('/api/method/peace_league_website.api.get_causes');
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

export async function donationStatus(checkoutRequestId) {
  return apiCall(`/api/method/peace_league_website.api.donation_status?checkout_request_id=${encodeURIComponent(checkoutRequestId)}`);
}

// ── Awards API ──

export async function getAwardCategories() {
  return apiCall('/api/method/peace_league_website.api_awards.get_categories');
}

export async function getAwardCategory(slug) {
  return apiCall(`/api/method/peace_league_website.api_awards.get_category?slug=${encodeURIComponent(slug)}`);
}

export async function getAwardResults() {
  return apiCall('/api/method/peace_league_website.api_awards.get_results');
}

export async function castVote(nomineeId, categorySlug, email) {
  const body = { nominee_id: nomineeId, category_slug: categorySlug };
  if (email) body.email = email;
  return apiCall('/api/method/peace_league_website.api_awards.cast_vote', {
    method: 'POST',
    body,
  });
}

export async function submitNomination(formData) {
  return apiCall('/api/method/peace_league_website.api_awards.create_nomination', {
    method: 'POST',
    body: formData,
  });
}

export async function purchaseTicket(data) {
  return apiCall('/api/method/peace_league_website.api_awards.purchase_ticket', {
    method: 'POST',
    body: data,
  });
}

export async function ticketPaymentStatus(checkoutRequestId) {
  return apiCall(`/api/method/peace_league_website.api_awards.ticket_payment_status?checkout_request_id=${encodeURIComponent(checkoutRequestId)}`);
}

// ── Admin API ──

export async function adminGetNominations(filters = {}) {
  const params = new URLSearchParams();
  if (Object.keys(filters).length) {
    params.set('filters', JSON.stringify(filters));
  }
  return apiCall(`/api/method/peace_league_website.api_awards.admin_get_nominations?${params.toString()}`);
}

export async function adminGetVoteStats() {
  return apiCall('/api/method/peace_league_website.api_awards.admin_get_vote_stats');
}

export async function adminDeleteNomination(nomineeName) {
  return apiCall('/api/method/peace_league_website.api_awards.admin_delete_nomination', {
    method: 'POST',
    body: { nominee_name: nomineeName },
  });
}

export async function adminUpdateNomination(nomineeName, updates) {
  return apiCall('/api/method/peace_league_website.api_awards.admin_update_nomination', {
    method: 'POST',
    body: { nominee_name: nomineeName, ...updates },
  });
}
