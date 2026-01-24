import React, { useState, useRef } from 'react';
import useTouchDevice from '@/hooks/useTouchDevice';

interface GlowEffectProps {
  children: React.ReactNode;
  className?: string;
  glowIntensity?: number; // 0-1 scale for glow intensity
  glowColor?: string; // CSS color value for the glow
  disabled?: boolean; // Whether to disable the glow effect entirely
}

const GlowEffect: React.FC<GlowEffectProps> = ({
  children,
  className = '',
  glowIntensity = 0.15,
  glowColor = 'rgba(99, 102, 241, 0.15)', // indigo-500 with low opacity
  disabled = false
}) => {
  const [mousePosition, setMousePosition] = useState({ x: 50, y: 50 }); // Default to center
  const elementRef = useRef<HTMLDivElement>(null);
  const isTouch = useTouchDevice();

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (elementRef.current) {
      const rect = elementRef.current.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      setMousePosition({ x, y });
    }
  };

  // Determine if glow should be enabled
  const glowEnabled = !disabled && !isTouch;

  // Calculate dynamic glow based on intensity
  const glowStyle = {
    '--mouse-x': `${mousePosition.x}%`,
    '--mouse-y': `${mousePosition.y}%`,
    '--glow-color': glowColor,
    '--glow-intensity': glowIntensity,
  } as React.CSSProperties;

  // Apply appropriate CSS classes based on glow availability
  const glowClass = glowEnabled ? 'glow-card' : '';
  const finalClassName = `${className} ${glowClass}`.trim();

  return (
    <div
      ref={elementRef}
      className={finalClassName}
      onMouseMove={glowEnabled ? handleMouseMove : undefined}
      style={glowStyle}
    >
      {children}
    </div>
  );
};

export default GlowEffect;