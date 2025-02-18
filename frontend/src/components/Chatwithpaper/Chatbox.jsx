import { Card, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useState } from "react";
import { chatService } from "@/services";

export function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [hoveredMessage, setHoveredMessage] = useState(null);
  const [isInputLocked, setIsInputLocked] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    setIsInputLocked(true);
    setMessages((prev) => [...prev, { role: "user", content: input }]);
    setInput("");

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

    setIsInputLocked(false);
  };

  const handleVectorSearch = async () => {
    if (!input.trim()) return;

    setIsInputLocked(true);
    setMessages((prev) => [...prev, { role: "user", content: input }]);
    setInput("");

    try {
      const response = await chatService.searchVectorDB(input);
      console.log("response:::", response);

      const formattedResponse = {
        role: "assistant",
        content: response.answer,
        metadata: response.page
          ? {
              page: response.page,
              text: response.vectorDB_answer,
            }
          : null,
        isVectorResult: !!response.page,
      };

      setMessages((prev) => [...prev, formattedResponse]);
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

    setIsInputLocked(false);
  };

  return (
    <Card className="w-full h-full flex flex-col">
      <ScrollArea className="flex-1 p-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className="mb-4 text-left"
          >
            <div
              className={`inline-block p-3 rounded-lg ${
                message.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : message.isVectorResult
                  ? "bg-blue-200 cursor-pointer hover:bg-blue-300"
                  : "bg-muted"
              }`}
              onMouseEnter={() => setHoveredMessage(index)}
              onMouseLeave={() => setHoveredMessage(null)}
              onClick={() => {
                if (message.isVectorResult && message.metadata?.page) {
                  window.dispatchEvent(
                    new CustomEvent("jumpToPage", {
                      detail: {
                        page: message.metadata.page,
                        text: message.metadata.text,
                      },
                    })
                  );
                }
              }}
            >
              {message.content}
              {hoveredMessage === index && message.metadata && (
                <div className="absolute bg-white border p-2 mt-1 rounded shadow-lg">
                  <p><strong>Page:</strong> {message.metadata.page}</p>
                  <p><strong>Text:</strong> {message.metadata.text}</p>
                </div>
              )}
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
            onKeyDown={(e) => e.key === "Enter" && !isInputLocked && handleSend()}
            disabled={isInputLocked}
          />
          <Button onClick={handleSend} disabled={isInputLocked}>Ask AI</Button>
          <Button onClick={handleVectorSearch} disabled={isInputLocked}>From DB</Button>
        </div>
      </CardFooter>
    </Card>
  );
}
