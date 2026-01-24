'use client';

import { createAuthClient } from 'better-auth/client';
import { createContext, useContext, useEffect, useState } from 'react';

// Initialize the auth client
const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
});

interface AuthContextType {
  user: any | null;
  signIn: (email: string, password: string) => Promise<any>;
  signUp: (email: string, password: string) => Promise<any>;
  signOut: () => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already signed in
    const checkSession = async () => {
      try {
        const session = await authClient.getSession();
        if (session?.data?.session) {
          setUser(session.data.session.user);
        }
      } catch (error) {
        console.error('Error checking session:', error);
      } finally {
        setIsLoading(false);
      }
    };

    checkSession();
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const response = await authClient.signIn.email({
        email,
        password,
      });

      if (response?.data?.session) {
        setUser(response.data.session.user);
      }

      return response;
    } catch (error: any) {
      console.error('Sign in error:', error);
      // Re-throw with a more descriptive message
      throw new Error(error?.message || 'Failed to sign in. Please try again.');
    }
  };

  const signUp = async (email: string, password: string) => {
    try {
      const response = await authClient.signUp.email({
        email,
        password,
      });

      if (response?.data?.session) {
        setUser(response.data.session.user);
      }

      return response;
    } catch (error: any) {
      console.error('Sign up error:', error);
      // Re-throw with a more descriptive message
      throw new Error(error?.message || 'Failed to sign up. Please try again.');
    }
  };

  const signOut = async () => {
    try {
      await authClient.signOut();
      setUser(null);
    } catch (error: any) {
      console.error('Sign out error:', error);
      // Re-throw with a more descriptive message
      throw new Error(error?.message || 'Failed to sign out. Please try again.');
    }
  };

  const value = {
    user,
    signIn,
    signUp,
    signOut,
    isLoading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}