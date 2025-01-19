import { useEffect, useContext, useState } from "react";
import { MyContext } from "@/App";
import { Worker, Viewer } from "@react-pdf-viewer/core";
import { highlightPlugin } from "@react-pdf-viewer/highlight";
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
import '@react-pdf-viewer/highlight/lib/styles/index.css';

export default function PdfViewer() {
  const { pdfUrl } = useContext(MyContext);
  const highlightPluginInstance = highlightPlugin(); // 创建高亮插件实例
  const [pluginMethods, setPluginMethods] = useState(null); // 存储插件方法

  // 触发高亮
  const highlightText = (text) => {
    if (!text || !pluginMethods) return;  // 确保有插件方法
    console.log(`🔍 Highlighting text: ${text}`);

    pluginMethods.highlight({
      keyword: text, // 高亮文本
      highlightColor: "rgba(255, 255, 0, 0.5)", // 黄色高亮
    });
  };

  // 监听 jumpToPage 事件
  useEffect(() => {
    const handleJumpToPage = (event) => {
      const { page, text } = event.detail;
      console.log(`📌 Jumping to page: ${page}, searching for text: ${text}`);
      highlightText(text); // 高亮文本
    };

    window.addEventListener("jumpToPage", handleJumpToPage);
    return () => {
      window.removeEventListener("jumpToPage", handleJumpToPage);
    };
  }, [pluginMethods]); // 确保 pluginMethods 加载后再执行

  return (
    <Worker workerUrl="/pdf.worker.min.js">
      <Viewer
        fileUrl={pdfUrl}
        plugins={[highlightPluginInstance]}
        onDocumentLoad={() => {
          console.log("✅ PDF loaded successfully!");
        }}
        onLoad={(methods) => {
          console.log("📚 Plugin methods loaded:", methods); // 确保方法正常加载
          setPluginMethods(methods); // 设置插件方法
        }}
      />
    </Worker>
  );
}
