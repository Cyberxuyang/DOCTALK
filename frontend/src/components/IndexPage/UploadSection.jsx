import { useEffect, useContext } from "react";
import { Button } from "../ui/button";
import { MyContext } from "@/App";
import { useNavigate } from "react-router-dom";
import { uploadPdf } from "@/services/upload";
// import chatService from "@/services/chat";

function UploadSection() {
  const navigate = useNavigate();
  const { file, setFile, pdfUrl, setPdfUrl } = useContext(MyContext);
  // 当 file 变化时，打印当前文件名，触发重新渲染

  useEffect(() => {
    if (file) {
      console.log("File has changed:", file.name);
    }
  }, [file]); // 只有 file 变化时才会执行此 useEffect

  // 处理文件上传
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]; // 只允许一个文件
    setFile(selectedFile);
    const newPdfUrl = URL.createObjectURL(selectedFile);
    setPdfUrl(newPdfUrl);
    console.log("New PDF URL:", newPdfUrl, pdfUrl);
  };

  // 处理拖放文件
  const handleDrop = (event) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0]; // 只允许一个文件

    // 检查是否为 PDF
    if (droppedFile && droppedFile.type === "application/pdf") {
      setFile(droppedFile);
      const newPdfUrl = URL.createObjectURL(droppedFile);
      setPdfUrl(newPdfUrl);
    } else {
      alert("Please upload a PDF file.");
    }
  };

  // 阻止默认拖放行为
  const handleDragOver = (event) => {
    event.preventDefault();
  };

  // 点击上传
  const handleUpload = async () => {
    if (file) {
      try {
        await uploadPdf(file);
        navigate("/chatwithpaper");
      } catch (error) {
        console.error("上传失败:", error);
        // 可以添加错误提示
      }
    }
  };

  return (
    <>
      <div className="container mx-auto mt-5">
        {/* upload section */}
        <div
          className="border-dashed border-2 border-gray-300 rounded-lg p-10 text-center hover:bg-gray-100 cursor-pointer "
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <input
            type="file"
            className="hidden"
            id="file-input"
            onChange={handleFileChange}
            accept="application/pdf"
          />
          <label htmlFor="file-input" className="block text-gray-500 text-l">
            Drag and drop PDF file here or click to upload.
          </label>
        </div>

        {/* show uploaded file */}
        {file && (
          <div className="mt-4">
            <h3 className="text-lg font-bold mb-2">Uploaded File:</h3>
            <ul>
              <li className="text-gray-600">{file.name}</li>
            </ul>
          </div>
        )}
      </div>
      <div className="text-center">
        <Button className="mt-4" disabled={!file} onClick={handleUpload}>
          Upload
        </Button>
      </div>
    </>
  );
}

export default UploadSection;
