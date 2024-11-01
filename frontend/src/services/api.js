import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8080",
  headers: {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  },
  maxContentLength: Infinity,
  maxBodyLength: Infinity,
});

export default api;
