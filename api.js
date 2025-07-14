import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export async function uploadVoice(formData) {
  const res = await axios.post(`${BASE_URL}/upload-voice/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}
