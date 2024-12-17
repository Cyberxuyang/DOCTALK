import { MyContext } from "@/App";
import { useContext } from "react";
import { Worker, Viewer } from "@react-pdf-viewer/core";
// import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';

import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';


export default function PdfViewer() {
  const { pdfUrl } = useContext(MyContext);
  // const pdfUrl = "/ca4_5.pdf";
  console.log("inpdfview"); 
  console.log(pdfUrl); 
  // const defaultLayoutPluginInstance = defaultLayoutPlugin();


  return (

    <Worker workerUrl="/pdf.worker.min.js">
            <Viewer
                fileUrl={pdfUrl}
                // plugins={[defaultLayoutPluginInstance]}
            />
        </Worker>

   
);
}