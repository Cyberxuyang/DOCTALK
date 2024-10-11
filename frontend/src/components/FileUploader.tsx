"use client";

import { useState } from "react";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// Helper function to truncate file name with ellipsis in the middle
const truncateFileName = (name: string, maxLength: number) => {
  if (name.length <= maxLength) return name;
  const start = name.slice(0, Math.ceil(maxLength / 2));
  const end = name.slice(-Math.floor(maxLength / 2));
  return `${start}...${end}`;
};

export default function FileUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;
    setFile(selectedFile);
  };

  const handleFileInputClick = () => {
    document.getElementById("file")?.click();
  };

  return (
    <div className="flex justify-center items-center min-h-screen">
      <Card className="max-w-lg min-w-[600px] min-h-[300px] max-h-[500px] max-w-[700px] overflow-auto">
        <CardContent className="p-6 space-y-4">
          <div className="border-2 border-dashed border-gray-200 rounded-lg flex flex-col gap-1 p-6 items-center">
            <span className="text-sm font-medium text-gray-500">
              Drag and drop a PDF file or click to browse
            </span>
            <span className="text-xs text-gray-500">
              File size should not exceed 10MB
            </span>
          </div>

          {errorMessage && (
            <p className="text-red-500 text-sm">{errorMessage}</p>
          )}

          {/* Container to match the style of the drag-and-drop area */}
          <div className="border-2 border-dashed border-gray-200 rounded-lg p-4 flex items-center space-x-4">
            {/* Transparent button */}
            <Button
              onClick={handleFileInputClick}
              className="bg-transparent border-2 border-gray-200 hover:bg-gray-100 text-gray-600"
            >
              Choose File
            </Button>

            {/* Display truncated file name with middle ellipsis */}
            {file && (
              <div className="text-sm text-gray-600 truncate max-w-xs">
                {truncateFileName(file.name, 40)}{" "}
                {/* Adjust maxLength as needed */}
              </div>
            )}
          </div>

          <input
            id="file"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            style={{ display: "none" }} // Hide the file input
          />
        </CardContent>

        <CardFooter className="flex justify-center">
          <Button size="lg" disabled={!file}>
            Upload
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
