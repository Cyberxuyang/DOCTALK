import ChatSection from "./ChatSection";
import Paper from "./Paper";

function ChatWithPaper() {
  return (
    <div className="flex">
      <div className="w-2/3 m-5 bg-yellow-300 ">
        <Paper />
      </div>
      <div className="w-1/3 m-5 bg-red-400">
        <ChatSection />
      </div>
    </div>
  );
}

export default ChatWithPaper;
