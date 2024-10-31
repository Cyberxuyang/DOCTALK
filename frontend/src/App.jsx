import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./components/Home";
import ChatWithPaper from "./components/Chatwithpaper/ChatWithPaper";
import AppLayout from "./components/AppLayout";
import Error from "./components/Error";
import { createContext, useState } from "react";

export const MyContext = createContext();

function App() {
  const [file, setFile] = useState(null);
  const [pdfUrl, setPdfUrl] = useState("pdfUrl");

  const router = createBrowserRouter([
    {
      element: (
        <MyContext.Provider value={{ file, setFile, pdfUrl, setPdfUrl }}>
          <AppLayout />
        </MyContext.Provider>
      ),
      errorElement: <Error />,
      children: [
        {
          path: "/",
          element: <Home />,
        },
        {
          path: "chatwithpaper",
          element: <ChatWithPaper />,
        },
      ],
    },
  ]);
  return <RouterProvider router={router} />;
}

export default App;
