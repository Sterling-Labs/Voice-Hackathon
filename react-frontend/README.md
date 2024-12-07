# Voice Hackathon React Frontend

A React application for making voice calls using Twilio's Voice API. This frontend connects to a Flask backend to handle Twilio voice calls.

## Quick Start

### Prerequisites
- Node.js installed
- Backend server running (see backend README)
- Twilio account credentials configured in backend

### Installation

1. Install dependencies:
```
cd Voice-Hackathon/react-frontend
npm install
```


2. Start the development server:
```
npm start
```


The app will run at http://localhost:3000

### Making a Test Call

1. Ensure the backend server is running at http://localhost:5000
2. Open the app in Chrome (recommended browser)
3. Allow microphone permissions when prompted
4. Click "Start Call" button
5. Wait for "Connected" status
6. Speak into your microphone
7. Click "End Call" to disconnect

### Troubleshooting

If calls aren't connecting:
1. Check browser console (F12) for connection logs
2. Verify backend server is running
3. Ensure microphone permissions are granted
4. Refresh page and try again

### Key Files

- `src/components/CallControl.js` - Main UI component
- `src/hooks/useFBCall.js` - Twilio device management
- `src/hooks/api.js` - Backend API calls

### Browser Support

- Chrome (recommended)
- Firefox
- Safari (limited support)

For detailed implementation and API documentation, see the source code comments.