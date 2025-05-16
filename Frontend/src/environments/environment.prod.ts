export interface Environment {
    API_URL: string;
  }
  
export const environment = {
    apiUrl: '${API_URL}'
  }