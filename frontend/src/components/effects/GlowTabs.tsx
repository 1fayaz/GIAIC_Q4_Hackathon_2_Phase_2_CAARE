import React, { useState, useRef } from 'react';
import useTouchDevice from '@/hooks/useTouchDevice';

interface GlowTabItem {
  id: string;
  label: string;
  content: React.ReactNode;
}

interface GlowTabsProps {
  items: GlowTabItem[];
  defaultActiveId?: string;
  className?: string;
}

const GlowTabs: React.FC<GlowTabsProps> = ({
  items,
  defaultActiveId,
  className = ''
}) => {
  const [activeTab, setActiveTab] = useState(defaultActiveId || items[0]?.id);
  const [mousePosition, setMousePosition] = useState({ x: 50, y: 50 });
  const tabsContainerRef = useRef<HTMLDivElement>(null);
  const isTouch = useTouchDevice();

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (tabsContainerRef.current) {
      const rect = tabsContainerRef.current.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      setMousePosition({ x, y });
    }
  };

  const handleTabClick = (id: string) => {
    setActiveTab(id);
  };

  const activeItem = items.find(item => item.id === activeTab);

  // For touch devices, disable hover effects to prevent constant glow
  const glowEnabled = !isTouch;

  return (
    <div className={`flex flex-col ${className}`}>
      <div
        ref={tabsContainerRef}
        className="flex border-b mb-4"
        onMouseMove={glowEnabled ? handleMouseMove : undefined}
        style={{
          '--mouse-x': `${mousePosition.x}%`,
          '--mouse-y': `${mousePosition.y}%`,
        } as React.CSSProperties}
      >
        {items.map((item) => (
          <button
            key={item.id}
            className={`px-4 py-2 font-medium text-sm relative glow-nav-item ${
              activeTab === item.id
                ? 'text-indigo-600 border-b-2 border-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => handleTabClick(item.id)}
          >
            {item.label}
          </button>
        ))}
      </div>
      <div className="flex-1">
        {activeItem?.content}
      </div>
    </div>
  );
};

export default GlowTabs;