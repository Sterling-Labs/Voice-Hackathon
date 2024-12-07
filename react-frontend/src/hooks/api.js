/**
 * API wrapper functions for Twilio and call management
 */

export class APIError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'APIError';
    this.status = status;
  }
}

/**
 * Fetches a Twilio token for the hackathon demo
 */
export async function getHackathonTwilioToken(id, baseUrl) {
  try {
    const response = await fetch(`${baseUrl}/api/hackathon-twilio-token?id=${id}`);
    
    if (!response.ok) {
      throw new APIError('Failed to fetch Twilio token', response.status);
    }

    const data = await response.json();
    return data.token;
  } catch (error) {
    console.error('Error fetching Twilio token:', error);
    throw error;
  }
}

/**
 * Starts a call for the hackathon demo
 */
export async function startHackathonCall(
  device_id, 
  prompt, 
  responseHandlerUrl,
  baseUrl
) {
  try {
    const response = await fetch(`${baseUrl}/api/hackathon-start-call`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        device_id,
        prompt,
        response_handler_url: responseHandlerUrl,
      }),
    });

    if (!response.ok) {
      throw new APIError('Failed to start call', response.status);
    }

    return await response.json();
  } catch (error) {
    console.error('Error starting call:', error);
    throw error;
  }
} 