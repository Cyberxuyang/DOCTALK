"use client";
import { ScrollArea } from "@/components/ui/scroll-area";
import React, { useContext, useEffect, useState } from "react";
import { MyContext } from "@/app/MyContext";

export default function PDFViewer() {
  const { pdfUrl } = useContext(MyContext);

  const [error, setError] = useState<string | null>(null);

  // 如果 pdfUrl 为空，提示用户上传文件
  useEffect(() => {
    if (!pdfUrl) {
      setError("Please upload a PDF file first.");
    }
  }, [pdfUrl]);

  return (
    <ScrollArea className="h-screen w-full overflow-auto rounded-md border p-4">
      <div className="pdf-viewer-container">
        {error ? (
          <p>{error}</p>
        ) : (
          <iframe
            src={pdfUrl}
            width="100%"
            height="600px"
            title="PDF Viewer"
            className="pdf-viewer"
          />
        )}
      </div>
    </ScrollArea>
  );
}
