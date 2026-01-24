import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Menu, X, Home, SquarePen, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface NavMobileProps {
  onLogout: () => void;
}

const NavMobile: React.FC<NavMobileProps> = ({ onLogout }) => {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  const toggleMenu = () => setIsOpen(!isOpen);

  const navItems = [
    { href: '/dashboard', icon: Home, label: 'Dashboard' },
    { href: '/dashboard/tasks', icon: SquarePen, label: 'Tasks' },
  ];

  return (
    <div className="md:hidden">
      <Button variant="outline" onClick={toggleMenu} className="glow-button">
        {isOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
      </Button>

      {isOpen && (
        <div className="fixed inset-0 z-50 bg-white bg-opacity-95 backdrop-blur-sm">
          <div className="flex flex-col h-full">
            <div className="flex justify-between items-center p-4 border-b">
              <span className="text-xl font-semibold">Todo App</span>
              <Button variant="outline" onClick={toggleMenu} className="glow-button">
                <X className="h-5 w-5" />
              </Button>
            </div>

            <div className="flex-1 flex flex-col p-4 space-y-4">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center space-x-3 p-3 rounded-lg ${
                    pathname === item.href
                      ? 'bg-indigo-100 text-indigo-700'
                      : 'hover:bg-gray-100'
                  }`}
                  onClick={() => setIsOpen(false)}
                >
                  <item.icon className="h-5 w-5" />
                  <span>{item.label}</span>
                </Link>
              ))}

              <Button
                variant="outline"
                className="w-full mt-4 glow-button flex items-center justify-center space-x-2"
                onClick={() => {
                  onLogout();
                  setIsOpen(false);
                }}
              >
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NavMobile;