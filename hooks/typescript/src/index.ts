/**
 * Request to the API
 */
export interface Request {
  method: string;
  url: string;
  input?: object;
  headers: object;
}

/**
 * Response from the API
 */
export interface Response {
  data: object;
  headers: object;
  status: number;
}

/**
 * Exception thrown by the API
 */
export interface Exception extends Error {
  title: string;
  type?: string;
  detail?: string;
  instance?: string;
  statusCode: number;
}

/**
 * Standard Hook interface
 */
export interface Hook {
  /**
   * Called before the request is sent to the API
   * @param request
   */
  beforeRequest(request: Request): Promise<void>;

  /**
   * Called after the response is received from the API
   * @param request
   * @param response
   */
  afterResponse(request: Request, response: Response): Promise<void>;

  /**
   * Called when an error occurs
   * @param error
   */
  onError(error: Exception): Promise<void>;
}

/**
 * Custom Hook
 */
export default class CustomHook implements Hook {
  async beforeRequest(request: Request): Promise<void> {
    console.log('Before request on URL', request.url, 'with method', request.method.toUpperCase());
  }

  async afterResponse(request: Request, response: Response): Promise<void> {
    console.log('After response on URL', request.url, 'with method', request.method.toUpperCase(), ', returning status', response.status);
  }

  async onError(error: Exception): Promise<void> {
    console.error('an error occurred!');
  }
}
