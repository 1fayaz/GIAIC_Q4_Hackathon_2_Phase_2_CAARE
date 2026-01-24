import React, { useState, useRef } from 'react';
import useTouchDevice from '@/hooks/useTouchDevice';

interface GlowCardWrapperProps {
  children: React.ReactNode;
  className?: string;
  glowIntensity?: number; // 0-1 scale for glow intensity
}

const GlowCardWrapper: React.FC<GlowCardWrapperProps> = ({
  children,
  className = '',
  glowIntensity = 0.15
}) => {
  const [mousePosition, setMousePosition] = useState({ x: 50, y: 50 }); // Default to center
  const cardRef = useRef<HTMLDivElement>(null);
  const isTouch = useTouchDevice();

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (cardRef.current) {
      const rect = cardRef.current.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      setMousePosition({ x, y });
    }
  };

  // For touch devices, disable hover effects to prevent constant glow
  const glowEnabled = !isTouch;

  const glowStyle = {
    '--mouse-x': `${mousePosition.x}%`,
    '--mouse-y': `${mousePosition.y}%`,
    '--glow-intensity': glowIntensity,
  } as React.CSSProperties;

  return (
    <div
      ref={cardRef}
      className={`relative overflow-hidden ${className} ${glowEnabled ? 'glow-card' : ''}`}
      onMouseMove={glowEnabled ? handleMouseMove : undefined}
      style={glowStyle}
    >
      {children}
    </div>
  );
};

export default GlowCardWrapper;