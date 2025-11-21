import axios from 'axios';

const BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000/api';

const instance = axios.create({
  baseURL: BASE,
  timeout: 30000,
});

export default {
  get: (path, opts) => instance.get(path, opts),
  post: (path, data, opts) => instance.post(path, data, opts),
  getBaseURL: () => BASE.replace('/api',''),
};
