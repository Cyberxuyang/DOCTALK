import PDFViewer from "./PDFViewer";
import Chatbot from "./Chatbot";

export default function pdfWithChat() {
  return (
    <div>
      <h1>PDF Viewer with Chat</h1>
      <div className="flex h-screen">
        {/* 左侧三分之二部分 */}
        <div className="w-2/3 p-4">
          <PDFViewer />
        </div>
        {/* 右侧三分之一部分 */}
        <div className="w-1/3 p-4 bg-gray-100">
          <Chatbot />
        </div>
      </div>
    </div>
  );
}
