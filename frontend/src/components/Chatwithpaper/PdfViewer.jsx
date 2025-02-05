import { useEffect, useContext, useState } from "react";
import { MyContext } from "@/App";
import { Worker, Viewer } from "@react-pdf-viewer/core";
import { highlightPlugin } from "@react-pdf-viewer/highlight";
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
import '@react-pdf-viewer/highlight/lib/styles/index.css';

export default function PdfViewer() {
  const { pdfUrl } = useContext(MyContext);
  const highlightPluginInstance = highlightPlugin(); // Create highlight plugin instance
  const [pluginMethods, setPluginMethods] = useState(null); // Store plugin methods

  // Trigger highlight
  const highlightText = (text) => {
    if (!text || !pluginMethods) return;  // Ensure plugin methods exist
    console.log(`🔍 Highlighting text: ${text}`);

    pluginMethods.highlight({
      keyword: text, // Text to highlight
      highlightColor: "rgba(255, 255, 0, 0.5)", // Yellow highlight
    });
  };

  // Listen for jumpToPage event
  useEffect(() => {
    const handleJumpToPage = (event) => {
      const { page, text } = event.detail;
      console.log(`📌 Jumping to page: ${page}, searching for text: ${text}`);
      highlightText(text); // Highlight the text
    };

    window.addEventListener("jumpToPage", handleJumpToPage);
    return () => {
      window.removeEventListener("jumpToPage", handleJumpToPage);
    };
  }, [pluginMethods]); // Execute after pluginMethods is loaded

  return (
    <Worker workerUrl="/pdf.worker.min.js">
      <Viewer
        fileUrl={pdfUrl}
        plugins={[highlightPluginInstance]}
        onDocumentLoad={() => {
          console.log("✅ PDF loaded successfully!");
        }}
        onLoad={(methods) => {
          console.log("📚 Plugin methods loaded:", methods); // Ensure methods are loaded correctly
          setPluginMethods(methods); // Set plugin methods
        }}
      />
    </Worker>
  );
}
