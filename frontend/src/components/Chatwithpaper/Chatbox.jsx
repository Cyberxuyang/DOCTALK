import { Card, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useState } from "react";

export function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    // 添加用户消息
    setMessages((prev) => [...prev, { role: "user", content: input }]);

    // TODO: 这里添加调用 AI API 的逻辑
    // const aiResponse = await callAIAPI(input)
    // setMessages(prev => [...prev, { role: 'assistant', content: aiResponse }])

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
          <Button onClick={handleSend}>Send</Button>
        </div>
      </CardFooter>
    </Card>
  );
}
