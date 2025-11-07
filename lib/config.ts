// API configuration
// In production (Vercel), NEXT_PUBLIC_API_URL should be set to: https://task-management-18oh.onrender.com
// In development, it defaults to localhost:8000
export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Log in development to help debugging
if (typeof window !== 'undefined' && process.env.NODE_ENV === 'development') {
  console.log('🔧 API URL:', API_URL);
  console.log('🔧 Environment:', process.env.NEXT_PUBLIC_API_URL ? 'Custom' : 'Default (localhost)');
}
