import api from "./api";

export const chatService = {
  sendMessage: async (message) => {
    try {
      const response = await api.post(
        "/chat",
        {
          question: message,
        },
        {
          timeout: 60000,
        }
      );
      return response.data.answer;
    } catch (error) {
      console.error("Error sending message:", error);
      throw new Error(
        error.response?.data?.message || "Failed to send message"
      );
    }
  },

  extractPdfText: async (file) => {
    try {
      const formData = new FormData();
      formData.append("pdf", file);

      const response = await api.post("/extract", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Extracted text:", response.data.text);
      return response.data.text;
    } catch (error) {
      console.error("Error extracting PDF text:", error);
      throw new Error(
        error.response?.data?.message || "Failed to extract PDF text"
      );
    }
  },
};
