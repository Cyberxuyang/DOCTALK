import { Card, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useState } from "react";
import { chatService } from "@/services";

export function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);

    try {
      const response = await chatService.sendMessage(input);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response },
      ]);
    } catch (error) {
      console.error("Failed to get response:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I encountered an error. Please try again.",
        },
      ]);
    }

    setInput("");
  };

  const handleVectorSearch = async () => {
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { role: "user", content: input }]);
    try {
      const response = await chatService.searchVectorDB(input);

      // 收到响应后，更新消息列表，添加助手的回复
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response },
      ]);
    } catch (error) {
      console.error("Failed to get response:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I encountered an error. Please try again.",
        },
      ]);
    }
    setInput("");
  };

  return (
    <Card className="w-full h-full flex flex-col">
      <ScrollArea className="flex-1 p-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-4 ${
              message.role === "user" ? "text-right" : "text-left"
            }`}
          >
            <div
              className={`inline-block p-3 rounded-lg ${
                message.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted"
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
      </ScrollArea>

      <CardFooter className="border-t p-4 pb-6">
        <div className="flex w-full gap-2">
          <Input
            placeholder="input..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <Button onClick={handleSend}>Ask AI</Button>
          <Button onClick={handleVectorSearch}>From DB</Button>
        </div>
      </CardFooter>
    </Card>
  );
}
