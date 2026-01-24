'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/providers/AuthProvider';
import AuthGuard from '@/components/AuthGuard';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import TaskList from '@/components/tasks/TaskList';
import TaskForm from '@/components/tasks/TaskForm';
import { Task } from '@/types/task';
import { taskService } from '@/services/taskService';
import { Plus } from 'lucide-react';

export default function TasksPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    if (user?.id) {
      fetchTasks();
    }
  }, [user]);

  const fetchTasks = async () => {
    if (!user?.id) return;

    setLoading(true);
    try {
      const response = await taskService.getAllTasks(user.id);
      if (response.success) {
        setTasks(response.data || []);
      } else {
        console.error('Failed to fetch tasks:', response.error);
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData: any) => {
    if (!user?.id) return;

    try {
      const response = await taskService.createTask({
        ...taskData,
        user_id: user.id
      });

      if (response.success) {
        setTasks([...tasks, response.data!]);
        setShowForm(false);
      } else {
        console.error('Failed to create task:', response.error);
      }
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const handleUpdateTask = async (taskId: string, taskData: any) => {
    if (!user?.id) return;

    try {
      const response = await taskService.updateTask(user.id, taskId, taskData);

      if (response.success) {
        setTasks(tasks.map(t => t.id === taskId ? response.data! : t));
        setEditingTask(null);
      } else {
        console.error('Failed to update task:', response.error);
      }
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!user?.id) return;

    try {
      const response = await taskService.deleteTask(user.id, taskId);

      if (response.success) {
        setTasks(tasks.filter(t => t.id !== taskId));
      } else {
        console.error('Failed to delete task:', response.error);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleTaskUpdate = (updatedTask: Task) => {
    setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
  };

  if (!user) {
    return <AuthGuard>{null}</AuthGuard>;
  }

  return (
    <AuthGuard>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Tasks</h1>
          <Button
            onClick={() => {
              setEditingTask(null);
              setShowForm(true);
            }}
            className="glow-button"
          >
            <Plus className="mr-2 h-4 w-4" /> New Task
          </Button>
        </div>

        {showForm ? (
          <Card className="glow-card">
            <CardHeader>
              <CardTitle>{editingTask ? 'Edit Task' : 'Create New Task'}</CardTitle>
            </CardHeader>
            <CardContent>
              <TaskForm
                task={editingTask || undefined}
                onSubmit={editingTask ? (data) => handleUpdateTask(editingTask.id, data) : handleCreateTask}
                onCancel={() => {
                  setShowForm(false);
                  setEditingTask(null);
                }}
              />
            </CardContent>
          </Card>
        ) : (
          <Button
            onClick={() => setShowForm(true)}
            variant="outline"
            className="w-full glow-button"
          >
            <Plus className="mr-2 h-4 w-4" /> Add New Task
          </Button>
        )}

        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
          </div>
        ) : (
          <TaskList
            tasks={tasks}
            onTaskUpdate={handleTaskUpdate}
            onTaskDelete={handleDeleteTask}
          />
        )}
      </div>
    </AuthGuard>
  );
}