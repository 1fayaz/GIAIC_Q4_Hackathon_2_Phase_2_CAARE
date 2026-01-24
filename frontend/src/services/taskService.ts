import { apiClient } from '@/lib/api';
import { handleApiError, ApiError } from '@/lib/errorHandler';
import { Task, TaskCreateRequest, TaskUpdateRequest } from '@/types/task';

class TaskService {
  async getAllTasks(userId: string): Promise<{ success: boolean; data?: Task[]; error?: string }> {
    try {
      const response = await apiClient.get<Task[]>(`/api/v1/${userId}/tasks`);
      return response;
    } catch (error: any) {
      const apiError = handleApiError(error, 'Failed to fetch tasks');
      return {
        success: false,
        error: apiError.message,
      };
    }
  }

  async getTaskById(userId: string, taskId: string): Promise<{ success: boolean; data?: Task; error?: string }> {
    try {
      const response = await apiClient.get<Task>(`/api/v1/${userId}/tasks/${taskId}`);
      return response;
    } catch (error: any) {
      const apiError = handleApiError(error, 'Failed to fetch task');
      return {
        success: false,
        error: apiError.message,
      };
    }
  }

  async createTask(taskData: TaskCreateRequest): Promise<{ success: boolean; data?: Task; error?: string }> {
    // Validate that the user ID in the task data matches the authenticated user
    if (!taskData.user_id) {
      return {
        success: false,
        error: 'User ID is required to create a task',
      };
    }

    try {
      const response = await apiClient.post<Task>(`/api/v1/${taskData.user_id}/tasks`, taskData);
      return response;
    } catch (error: any) {
      const apiError = handleApiError(error, 'Failed to create task');
      return {
        success: false,
        error: apiError.message,
      };
    }
  }

  async updateTask(userId: string, taskId: string, taskData: TaskUpdateRequest): Promise<{ success: boolean; data?: Task; error?: string }> {
    // Validate that the user ID matches the authenticated user
    if (!userId) {
      return {
        success: false,
        error: 'User ID is required to update a task',
      };
    }

    try {
      const response = await apiClient.put<Task>(`/api/v1/${userId}/tasks/${taskId}`, taskData);
      return response;
    } catch (error: any) {
      const apiError = handleApiError(error, 'Failed to update task');
      return {
        success: false,
        error: apiError.message,
      };
    }
  }

  async deleteTask(userId: string, taskId: string): Promise<{ success: boolean; error?: string }> {
    // Validate that the user ID matches the authenticated user
    if (!userId) {
      return {
        success: false,
        error: 'User ID is required to delete a task',
      };
    }

    try {
      const response = await apiClient.delete(`/api/v1/${userId}/tasks/${taskId}`);
      return response;
    } catch (error: any) {
      const apiError = handleApiError(error, 'Failed to delete task');
      return {
        success: false,
        error: apiError.message,
      };
    }
  }

  async toggleTaskCompletion(userId: string, taskId: string): Promise<{ success: boolean; data?: Task; error?: string }> {
    // Validate that the user ID matches the authenticated user
    if (!userId) {
      return {
        success: false,
        error: 'User ID is required to toggle task completion',
      };
    }

    try {
      const response = await apiClient.patch<Task>(`/api/v1/${userId}/tasks/${taskId}/complete`, {});
      return response;
    } catch (error: any) {
      const apiError = handleApiError(error, 'Failed to toggle task completion');
      return {
        success: false,
        error: apiError.message,
      };
    }
  }
}

export const taskService = new TaskService();
export default TaskService;