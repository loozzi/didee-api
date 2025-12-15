# Firebase Authentication Setup Guide

This guide explains how to set up Firebase Authentication for the Didee API.

## Prerequisites

1. A Firebase project (create one at https://console.firebase.google.com/)
2. Python environment with firebase-admin installed

## Setup Steps

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or select an existing project
3. Follow the setup wizard

### 2. Enable Authentication Methods

1. In Firebase Console, go to **Authentication** → **Sign-in method**
2. Enable the authentication providers you want to use:
   - Email/Password
   - Google
   - Facebook
   - Apple
   - etc.

### 3. Generate Service Account Key

1. In Firebase Console, go to **Project Settings** (gear icon)
2. Go to **Service Accounts** tab
3. Click **Generate New Private Key**
4. Download the JSON file
5. Save it securely in your project (e.g., `firebase-credentials.json`)
6. **Important**: Add this file to `.gitignore` to keep it secure

### 4. Configure Environment Variables

Create a `.env` file in the project root with:

```env
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

Or use the full path:
```env
FIREBASE_CREDENTIALS_PATH=/path/to/your/firebase-credentials.json
```

### 5. Update .gitignore

Add these lines to `.gitignore`:
```
.env
firebase-credentials.json
*firebase-credentials*.json
```

## API Endpoints

### 1. Verify Token and Create User
**POST** `/api/v1/users/verify`

Verifies Firebase token and creates user if they don't exist.

**Request Body:**
```json
{
  "firebase_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
}
```

**Response (New User):**
```json
{
  "message": "User created successfully",
  "user": {
    "id": "uuid-here",
    "firebase_uid": "firebase-uid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "avatar_url": "https://...",
    "phone_number": null,
    "provider": "GOOGLE",
    "created_at": "2025-11-24T10:00:00",
    "updated_at": "2025-11-24T10:00:00"
  },
  "is_new_user": true
}
```

**Response (Existing User):**
```json
{
  "message": "User verified successfully",
  "user": { ... },
  "is_new_user": false
}
```

### 2. Get Current User
**GET** `/api/v1/users/me`

Returns the current authenticated user's information.

**Headers:**
```
Authorization: Bearer <firebase-token>
```

**Response:**
```json
{
  "id": "uuid-here",
  "firebase_uid": "firebase-uid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "avatar_url": "https://...",
  "phone_number": null,
  "provider": "GOOGLE",
  "created_at": "2025-11-24T10:00:00",
  "updated_at": "2025-11-24T10:00:00"
}
```

## Authentication Middleware

The API includes a global Firebase authentication middleware that protects all routes by default.

### Public Routes (No Authentication Required)

The following routes are public and don't require authentication:
- `/`
- `/health`
- `/api/v1/docs`
- `/api/v1/redoc`
- `/api/v1/openapi.json`
- `/api/v1/users/verify`

### Protected Routes (Authentication Required)

All other routes require a valid Firebase token in the Authorization header:
```
Authorization: Bearer <firebase-token>
```

### Adding Public Routes

To add more public routes, update `app/core/config.py`:

```python
PUBLIC_ROUTES: List[str] = [
    "/",
    "/health",
    "/api/v1/docs",
    "/api/v1/redoc",
    "/api/v1/openapi.json",
    "/api/v1/users/verify",
    "/api/v1/your-public-route",  # Add your route here
]
```

### Using Authentication in Endpoints

To get the current authenticated user in your endpoints:

```python
from fastapi import Depends
from app.core.dependencies import get_current_user
from app.models.user import User

@router.get("/my-protected-route")
async def my_route(current_user: User = Depends(get_current_user)):
    # current_user is automatically populated with authenticated user
    return {"user_id": current_user.id, "email": current_user.email}
```

## Client-Side Integration

### Web (JavaScript/TypeScript)

```javascript
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';

const auth = getAuth();

// Sign in user
const userCredential = await signInWithEmailAndPassword(auth, email, password);
const user = userCredential.user;

// Get ID token
const idToken = await user.getIdToken();

// Verify token with backend
const response = await fetch('http://localhost:8000/api/v1/users/verify', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ firebase_token: idToken }),
});

const data = await response.json();

// Make authenticated requests
const meResponse = await fetch('http://localhost:8000/api/v1/users/me', {
  headers: {
    'Authorization': `Bearer ${idToken}`,
  },
});
```

### Mobile (React Native)

```javascript
import auth from '@react-native-firebase/auth';

// Sign in user
const userCredential = await auth().signInWithEmailAndPassword(email, password);

// Get ID token
const idToken = await userCredential.user.getIdToken();

// Use token for API calls (same as web example above)
```

## Testing

### Using curl

```bash
# Get Firebase token from your client app, then:

# Verify token
curl -X POST http://localhost:8000/api/v1/users/verify \
  -H "Content-Type: application/json" \
  -d '{"firebase_token": "YOUR_FIREBASE_TOKEN"}'

# Get current user
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN"
```

### Using Postman

1. Set up a POST request to `/api/v1/users/verify`
2. Set header: `Content-Type: application/json`
3. Set body (raw JSON):
   ```json
   {
     "firebase_token": "your-token-here"
   }
   ```

## Troubleshooting

### Error: "Firebase authentication is not configured"

- Ensure `FIREBASE_CREDENTIALS_PATH` is set in your `.env` file
- Verify the credentials file exists at the specified path
- Check that the file is valid JSON

### Error: "Invalid authentication token"

- Token may be expired (Firebase tokens expire after 1 hour)
- Get a fresh token from your client
- Ensure you're using the ID token, not the refresh token

### Error: "User not found. Please verify your account first"

- User must call `/api/v1/users/verify` endpoint first
- This creates the user in the database

## Security Best Practices

1. **Never commit Firebase credentials** - Add to `.gitignore`
2. **Use environment variables** - Keep credentials path in `.env`
3. **Rotate keys regularly** - Generate new service account keys periodically
4. **Limit token scope** - Use Firebase security rules to limit what tokens can access
5. **Validate on server** - Always verify tokens server-side (which this API does)
6. **Use HTTPS** - In production, always use HTTPS to prevent token interception

## Production Deployment

1. Store Firebase credentials securely (e.g., AWS Secrets Manager, Azure Key Vault)
2. Set `FIREBASE_CREDENTIALS_PATH` environment variable in your deployment platform
3. Ensure credentials file has appropriate read permissions
4. Enable CORS for your frontend domains
5. Use HTTPS for all API requests
