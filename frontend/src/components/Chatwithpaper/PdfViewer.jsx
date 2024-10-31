import { MyContext } from "@/App";
import { useContext } from "react";

export default function PdfViewer() {
  const { pdfUrl } = useContext(MyContext);

  if (!pdfUrl) {
    return <div>Please upload a PDF file</div>;
  }

  return (
    <div className="h-full">
      <embed src={pdfUrl} type="application/pdf" className="w-full h-full" />
    </div>
  );
}
