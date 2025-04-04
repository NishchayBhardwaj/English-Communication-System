import { useState, useEffect } from "react";
import { PlusCircle, MessageCircle, Trash2 } from "lucide-react";

export default function Sidebar({ onNewChat, onSelectChat, currentChatId }) {
  const [chatHistory, setChatHistory] = useState([]);

  // Fetch chat histories from MongoDB (through your backend API)
  useEffect(() => {
    fetchChatHistories();
  }, []);

  const fetchChatHistories = async () => {
    try {
      const response = await fetch("http://localhost:8080/api/chat-histories");
      const data = await response.json();
      setChatHistory(data);
    } catch (error) {
      console.error("Error fetching chat histories:", error);
    }
  };

  const handleDeleteChat = async (chatId) => {
    try {
      await fetch(`http://localhost:8080/api/chat-histories/${chatId}`, {
        method: "DELETE",
      });
      fetchChatHistories(); // Refresh the list
    } catch (error) {
      console.error("Error deleting chat:", error);
    }
  };

  return (
    <div className="w-64 bg-gray-900 h-screen flex flex-col">
      {/* New Chat Button */}
      <button
        onClick={onNewChat}
        className="flex items-center gap-2 p-4 hover:bg-gray-800 text-white w-full"
      >
        <PlusCircle size={20} />
        <span>New Chat</span>
      </button>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto">
        {chatHistory.map((chat) => (
          <div
            key={chat._id}
            className={`flex items-center justify-between p-4 hover:bg-gray-800 cursor-pointer ${
              currentChatId === chat._id ? "bg-gray-800" : ""
            }`}
          >
            <div
              className="flex items-center gap-2 text-white flex-1"
              onClick={() => onSelectChat(chat._id)}
            >
              <MessageCircle size={20} />
              <span className="truncate">
                {chat.title || new Date(chat.timestamp).toLocaleDateString()}
              </span>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleDeleteChat(chat._id);
              }}
              className="text-gray-400 hover:text-red-500"
            >
              <Trash2 size={16} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
