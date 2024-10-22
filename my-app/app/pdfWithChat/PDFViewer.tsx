"use client";
import { ScrollArea } from "@/components/ui/scroll-area";
import React, { useContext, useEffect, useState } from "react";
import { MyContext } from "@/app/MyContext";
// import { getDocument } from "pdfjs-dist";

export default function PDFViewer() {
  const { pdfUrl } = useContext(MyContext);
  const [parsedContent, setParsedContent] = useState<string>(""); // 存储解析出的 PDF 内容
  const [error, setError] = useState<string | null>(null);

  // 解析 PDF 内容的函数
  async function parsePdfContent(url: string) {
    const loadingTask = getDocument(url);
    const pdf = await loadingTask.promise;
    let textContent = "";

    // 遍历每一页，提取文字内容
    for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
      const page = await pdf.getPage(pageNumber);
      const text = await page.getTextContent();

      // 遍历文本内容
      text.items.forEach((item) => {
        if ("str" in item) {
          // 类型守卫，确保 item 包含 'str' 属性
          textContent += (item as any).str + " ";
        }
      });
    }

    return textContent;
  }
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
