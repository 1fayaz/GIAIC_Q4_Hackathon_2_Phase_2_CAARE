import { Button } from '@/components/ui/button';
import { Task } from '@/types/task';
import { Edit, Trash2, CheckCircle, Circle } from 'lucide-react';

interface TaskActionsProps {
  task: Task;
  onTaskUpdate: (updatedTask: Task) => void;
  onTaskDelete: (taskId: string) => void;
}

const TaskActions: React.FC<TaskActionsProps> = ({ task, onTaskUpdate, onTaskDelete }) => {
  const handleToggleComplete = () => {
    onTaskUpdate({ ...task, completed: !task.completed });
  };

  const handleEdit = () => {
    // Edit action will be handled by parent component
    console.log('Edit task:', task.id);
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      onTaskDelete(task.id);
    }
  };

  return (
    <div className="flex space-x-2">
      <Button
        variant="ghost"
        size="sm"
        onClick={handleToggleComplete}
        className="glow-button"
      >
        {task.completed ? (
          <CheckCircle className="h-4 w-4 text-green-500" />
        ) : (
          <Circle className="h-4 w-4 text-gray-400" />
        )}
      </Button>
      <Button
        variant="ghost"
        size="sm"
        onClick={handleEdit}
        className="glow-button"
      >
        <Edit className="h-4 w-4" />
      </Button>
      <Button
        variant="ghost"
        size="sm"
        onClick={handleDelete}
        className="glow-button"
      >
        <Trash2 className="h-4 w-4 text-red-500" />
      </Button>
    </div>
  );
};

export default TaskActions;