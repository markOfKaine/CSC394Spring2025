import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const getArticles = () => axios.get(`${API_BASE}/get-articles`);
export const addArticle = (article) => axios.post(`${API_BASE}/add-article`, null, { params: { article } });
export const delArticle = (article) => axios.delete(`${API_BASE}/delete-article`, null, { params: { article } });