import axios from "axios";

const postApi = axios.create({
  baseURL: "http://localhost:8080",
  headers: {
    "Content-Type": "application/json",
    // "Access-Control-Allow-Origin": "*",
  },
  maxContentLength: Infinity,
  maxBodyLength: Infinity,
});

const formdataApi = axios.create({
  baseURL: "http://localhost:8080",

  maxContentLength: Infinity,
  maxBodyLength: Infinity,
});

export { postApi, formdataApi };
