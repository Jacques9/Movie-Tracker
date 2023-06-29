// Firebase Config
import { app } from '../firebase/config';

// Firebase functions
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  sendPasswordResetEmail,
  updateProfile,
  onAuthStateChanged,
} from 'firebase/auth';

// React Hooks
import { useState } from 'react';

export const useAuth = () => {
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(null);

  // Get auth from firebase
  const auth = getAuth(app);
  // Change firebase messages language to brazilian portuguese
  auth.languageCode = 'pt-BR';

  // Set redirect URL to localhost
  const actionCodeSettings = {
    url: 'https://moviereviews-yago.vercel.app/',
  };

  // Function to login users
  const signInUser = async (email, password) => {
    setLoading(true);

    try {
      await signInWithEmailAndPassword(auth, email, password);
      setLoading(false);
    } catch (e) {
      setError(e.message);
      setLoading(false);
    }
  };

  // Function to logout users
  const signOutUser = () => {
    signOut(auth);
  };

  return {
    signInUser,
    signOutUser,
    onAuthStateChanged,
  };
};
