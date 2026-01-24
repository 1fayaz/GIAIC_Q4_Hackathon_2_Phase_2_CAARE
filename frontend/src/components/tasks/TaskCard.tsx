import React, { useState, useRef } from 'react';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Task } from '@/types/task';
import TaskActions from './TaskActions';
import useTouchDevice from '@/hooks/useTouchDevice';

interface TaskCardProps {
  task: Task;
  onTaskUpdate: (updatedTask: Task) => void;
  onTaskDelete: (taskId: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onTaskUpdate, onTaskDelete }) => {
  const [isHovered, setIsHovered] = useState(false);
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

  return (
    <Card
      ref={cardRef}
      className={`glow-card relative overflow-hidden ${task.completed ? 'opacity-75' : ''} ${glowEnabled ? 'hover:enabled' : ''}`}
      onMouseMove={glowEnabled ? handleMouseMove : undefined}
      onMouseEnter={glowEnabled ? () => setIsHovered(true) : undefined}
      onMouseLeave={glowEnabled ? () => setIsHovered(false) : undefined}
      style={{
        '--mouse-x': `${mousePosition.x}%`,
        '--mouse-y': `${mousePosition.y}%`,
      } as React.CSSProperties}
    >
      <CardContent className="pt-6">
        <div className="flex flex-col sm:flex-row sm:items-start space-y-3 sm:space-y-0 sm:space-x-3">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={(e) => onTaskUpdate({ ...task, completed: e.target.checked })}
            className="mt-1 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 self-start"
          />
          <div className="flex-1 min-w-0">
            <h3 className={`text-base sm:text-lg font-medium break-words ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-1 text-sm break-words ${task.completed ? 'text-gray-400' : 'text-gray-500'}`}>
                {task.description}
              </p>
            )}
            <div className="mt-2 text-xs text-gray-400">
              {new Date(task.created_at).toLocaleDateString()}
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter className="justify-end sm:justify-end">
        <TaskActions
          task={task}
          onTaskUpdate={onTaskUpdate}
          onTaskDelete={onTaskDelete}
        />
      </CardFooter>
    </Card>
  );
};

export default TaskCard;