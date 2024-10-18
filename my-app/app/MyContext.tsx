import { createContext, useState, ReactNode } from "react";

// 定义 Context 类型
interface MyContextType {
  pdfUrl: string;
  setPdfUrl: (url: string) => void;
}

// 提供默认的 Context 值，setPdfUrl 是一个空函数
const MyContext = createContext<MyContextType>({
  pdfUrl: "",
  setPdfUrl: () => {},
});

// 定义 Provider 组件的 props 类型
interface ProviderProps {
  children: ReactNode;
}

// Provider 组件
function Provider({ children }: ProviderProps) {
  const [pdfUrl, setPdfUrl] = useState<string>("asdas");

  return (
    <MyContext.Provider value={{ pdfUrl, setPdfUrl }}>
      {children}
    </MyContext.Provider>
  );
}

export { MyContext, Provider };
