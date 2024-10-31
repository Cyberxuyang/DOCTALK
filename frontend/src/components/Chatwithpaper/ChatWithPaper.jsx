import { ChatBox } from "./Chatbox";
import Paper from "./Paper";

function ChatWithPaper() {
  return (
    <div className="flex h-[calc(100vh-32px)] pb-8">
      <div className="w-2/3 m-5 overflow-hidden">
        <Paper />
      </div>
      <div className="w-1/3 m-5 flex">
        <ChatBox />
      </div>
    </div>
  );
}

export default ChatWithPaper;
