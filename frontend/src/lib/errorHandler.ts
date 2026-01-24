/**
 * Error handling utilities for the application
 */

export interface ApiError {
  status: number;
  message: string;
  details?: any;
}

export const handleApiError = (error: any, defaultMessage: string = 'An error occurred'): ApiError => {
  if (error.status) {
    // This is an API error with status
    return {
      status: error.status,
      message: error.error || defaultMessage,
      details: error.details || undefined
    };
  } else if (error.message) {
    // This is a generic error
    return {
      status: 500,
      message: error.message || defaultMessage,
    };
  } else {
    // Unknown error
    return {
      status: 500,
      message: defaultMessage,
    };
  }
};

export const isUnauthorizedError = (error: ApiError): boolean => {
  return error.status === 401;
};

export const isNotFoundError = (error: ApiError): boolean => {
  return error.status === 404;
};

export const isValidationError = (error: ApiError): boolean => {
  return error.status === 422;
};

export const handleErrorNotification = (error: ApiError): void => {
  // This could be replaced with a toast notification or similar
  console.error(`Error ${error.status}: ${error.message}`);

  // Additional error reporting logic could go here
  // e.g., sending to error tracking service
};