import { useState, useEffect } from 'react';

const useTouchDevice = (): boolean => {
  const [isTouchDevice, setIsTouchDevice] = useState<boolean>(false);

  useEffect(() => {
    // Check for touch capabilities
    const checkTouchDevice = () => {
      // Method 1: Check for touch events
      if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
        return true;
      }

      // Method 2: Check for TouchEvent constructor
      if (typeof TouchEvent !== 'undefined') {
        return true;
      }

      // Method 3: Check screen characteristics
      // This is a fallback method
      if (window.matchMedia('(pointer: coarse)').matches) {
        return true;
      }

      return false;
    };

    setIsTouchDevice(checkTouchDevice());

    // Listen for orientation changes to re-check
    const handleOrientationChange = () => {
      setIsTouchDevice(checkTouchDevice());
    };

    window.addEventListener('orientationchange', handleOrientationChange);

    return () => {
      window.removeEventListener('orientationchange', handleOrientationChange);
    };
  }, []);

  return isTouchDevice;
};

export default useTouchDevice;