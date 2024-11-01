import { formdataApi } from "./api";

export const uploadPdf = async (file) => {
  console.log("开始上传文件:", file);
  const MAX_SIZE = 10 * 1024 * 1024;
  if (file.size > MAX_SIZE) {
    throw new Error("File size exceeds 10MB limit");
  }

  try {
    const formData = new FormData();
    const blob = new Blob([file], { type: "application/pdf" });
    formData.append("pdf", blob, file.name);

    const response = await formdataApi.post("/upload", formData, {
      headers: {
        "Content-Type": undefined,
      },
    });

    if (!response.data || !response.data.text) {
      throw new Error("Invalid response format");
    }

    return response.data.text;
  } catch (error) {
    console.error("Error uploading PDF file:", error);
    if (error.code === "ECONNABORTED") {
      throw new Error("Upload timeout - please try again");
    }
    throw new Error(
      error.response?.data?.message || "Failed to upload PDF file"
    );
  }
};
