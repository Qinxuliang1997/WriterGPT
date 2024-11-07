import axios from "axios";

// Create an axios instance
const apiClient = axios.create({
  baseURL: 'http://106.14.184.241', // Set your base URL
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

let refresh = false;

export const setupAxiosInterceptors = (navigate, onSetErrorMessage) => {
  apiClient.interceptors.response.use(
    response => response,
    async (error) => {
      if (error.response && error.response.status === 401 && !refresh) {
        refresh = true;
        try {
          const response = await apiClient.post('/token/refresh/', {
            refresh: localStorage.getItem('refresh_token')
          });
          localStorage.setItem('access_token', response.data.access);
          if (response.data.refresh) {
            localStorage.setItem('refresh_token', response.data.refresh);
          }
          
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
          error.config.headers['Authorization'] = `Bearer ${response.data.access}`;
          return apiClient(error.config);
        } catch (refreshError) {
          if (onSetErrorMessage) {
            onSetErrorMessage('请先登录');
          }
          setTimeout(() => {
            navigate('/login');
          }, 1000);
          return Promise.reject(refreshError);
        } finally {
          refresh = false;
        }
      } else {
          if (onSetErrorMessage) {
              onSetErrorMessage('出错啦！请稍后再试');
          }
      }
      refresh = false;
      return Promise.reject(error);
    }
  );
};

export default apiClient;
