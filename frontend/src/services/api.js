import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api";

export const checkApiHealth = async () => {
  try {
    const response = await fetch("http://localhost:5000/");
    if (!response.ok) {
      throw new Error("API server is not responding");
    }
    return await response.json();
  } catch (error) {
    console.error("API Health Check Failed:", error);
    throw error;
  }
};

export const processText = async (text) => {
  try {
    const response = await fetch(`${API_BASE_URL}/process-text`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to process text");
    }

    return await response.json();
  } catch (error) {
    console.error("Error processing text:", error);
    throw error;
  }
};

export const processSpeech = async (audioBlob) => {
  try {
    const formData = new FormData();
    formData.append("audio", audioBlob);

    const response = await fetch(`${API_BASE_URL}/process-speech`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to process speech");
    }

    return await response.json();
  } catch (error) {
    console.error("Error processing speech:", error);
    throw error;
  }
};
