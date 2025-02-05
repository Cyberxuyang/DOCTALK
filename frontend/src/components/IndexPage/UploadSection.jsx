import { useEffect, useContext } from "react";
import { Button } from "../ui/button";
import { MyContext } from "@/App";
import { useNavigate } from "react-router-dom";
import { uploadPdf } from "@/services/upload";
// import chatService from "@/services/chat";

function UploadSection() {
  const navigate = useNavigate();
  const { file, setFile, pdfUrl, setPdfUrl } = useContext(MyContext);
  // Re-render when file changes and log the current filename

  useEffect(() => {
    if (file) {
      console.log("File has changed:", file.name);
    }
  }, [file]); // Only execute when file changes

  // Handle file upload
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]; // Only allow one file
    setFile(selectedFile);
    const newPdfUrl = URL.createObjectURL(selectedFile);
    setPdfUrl(newPdfUrl);
    console.log("New PDF URL:", newPdfUrl, pdfUrl);
  };

  // Handle file drop
  const handleDrop = (event) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0]; // Only allow one file

    // Check if file is PDF
    if (droppedFile && droppedFile.type === "application/pdf") {
      setFile(droppedFile);
      const newPdfUrl = URL.createObjectURL(droppedFile);
      setPdfUrl(newPdfUrl);
    } else {
      alert("Please upload a PDF file.");
    }
  };

  // Prevent default drag behavior
  const handleDragOver = (event) => {
    event.preventDefault();
  };

  // Handle upload button click
  const handleUpload = async () => {
    if (file) {
      try {
        await uploadPdf(file);
        navigate("/chatwithpaper");
      } catch (error) {
        console.error("Upload failed:", error);
        // Add error notification here if needed
      }
    }
  };

  return (
    <>
      <div className="container mx-auto mt-5">
        {/* Upload section */}
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

        {/* Display uploaded file */}
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
