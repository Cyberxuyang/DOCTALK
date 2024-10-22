import { useState } from "react";
import { Button } from "../ui/button";

function UploadSection() {
  const [file, setFile] = useState(null);

  // 处理文件上传
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]; // 只允许一个文件
    setFile(selectedFile);
  };

  // 处理拖放文件
  const handleDrop = (event) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0]; // 只允许一个文件
    setFile(droppedFile);
  };

  // 阻止默认拖放行为
  const handleDragOver = (event) => {
    event.preventDefault();
  };

  return (
    <>
      <div className="container mx-auto">
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
            Drag and drop file here or click to upload.
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
        <Button className="mt-4" disabled={!file}>
          Upload
        </Button>
      </div>
    </>
  );
}

export default UploadSection;
