// Dashboard route group layout with navigation and sign out
// Implements T041, T042, T043, T045 from tasks.md

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { Button } from '@/components/ui/Button';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { user, signOut, isLoading: authLoading } = useAuth();
  const [isSigningOut, setIsSigningOut] = useState(false);

  /**
   * T043: Implement signout handler that calls Better Auth signout
   * T045: Implement redirect to /signin after signout
   */
  const handleSignOut = async () => {
    setIsSigningOut(true);
    try {
      // T043: Call Better Auth signout
      await signOut();

      // T045: Redirect to /signin after signout
      router.push('/signin');
    } catch (error) {
      console.error('Signout error:', error);
      // Still redirect even if API call fails
      router.push('/signin');
    } finally {
      setIsSigningOut(false);
    }
  };

  // Show loading state while auth is initializing
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <LoadingSpinner size="lg" text="Loading..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* T041: Navigation header */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo and title */}
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
            </div>

            {/* User info and sign out button */}
            <div className="flex items-center gap-4">
              {user && (
                <span className="text-sm text-gray-700 hidden sm:block">
                  {user.email}
                </span>
              )}

              {/* T042: Sign out button */}
              <Button
                variant="ghost"
                size="sm"
                onClick={handleSignOut}
                isLoading={isSigningOut}
                disabled={isSigningOut}
              >
                {isSigningOut ? 'Signing out...' : 'Sign out'}
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
