import { postApi } from "./api";

export const chatService = {
  sendMessage: async (message) => {
    try {
      const response = await postApi.post(
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
};
