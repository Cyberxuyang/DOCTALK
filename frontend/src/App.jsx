import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./components/Home";
import ChatWithPaper from "./components/Chatwithpaper/ChatWithPaper";
import AppLayout from "./components/AppLayout";
import Error from "./components/Error";
import { createContext, useState } from "react";

export const MyContext = createContext();

const Provider = ({ children }) => {
  const [file, setFile] = useState(null);

  return (
    <MyContext.Provider value={{ file, setFile }}>
      {children}
    </MyContext.Provider>
  );
};

const router = createBrowserRouter([
  {
    element: <AppLayout />,
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

function App() {
  return (
    <Provider>
      <RouterProvider router={router} />
    </Provider>
  );
}

export default App;
