"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Mic, MicOff, FileText, Loader } from "lucide-react";
import { processText, processSpeech, checkApiHealth } from "@/services/api";
import Sidebar from "./Sidebar";

export default function ChatInterface({ onSubmitText }) {
  const [messages, setMessages] = useState([
    {
      role: "system",
      content:
        "Welcome to the English Communication Assessment Tool! You can type or speak to begin your assessment.",
    },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showReport, setShowReport] = useState(false);
  const [report, setReport] = useState(null);
  const [result, setResult] = useState(null);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [showSidebar, setShowSidebar] = useState(true);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Add API health check
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await checkApiHealth();
      } catch (error) {
        setMessages((prev) => [
          ...prev,
          {
            role: "system",
            content:
              "Unable to connect to the assessment service. Please try again later.",
          },
        ]);
      }
    };
    checkHealth();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() && !isRecording) return;

    setIsProcessing(true);
    try {
      // Add the user message to chat first
      setMessages((prev) => [...prev, { role: "user", content: inputMessage }]);

      // Process the text
      const result = await processText(inputMessage);

      console.log(result); // Add the system responses
      if (result.language_analysis) {
        // Add grammar analysis
        setMessages((prev) => [
          ...prev,
          {
            role: "system",
            content: `Grammar Analysis: ${result.language_analysis[0][1]}`,
          },
        ]);
      }

      if (result.performance_analysis) {
        // Add vocabulary analysis
        setMessages((prev) => [
          ...prev,
          {
            role: "system",
            content: `Scores: \n${result.performance_analysis[0][1]}`,
          },
        ]);

        // Add improvement suggestions
        if (result.performance_analysis[2]) {
          setMessages((prev) => [
            ...prev,
            {
              role: "system",
              content: `Improvement Suggestions: ${result.performance_analysis[2][1]}`,
            },
          ]);
        }
      }

      // Add improvement suggestions
      if (
        result.interview_questions &&
        result.interview_questions !== "No questions generated"
      ) {
        const updatedMessages = [];

        // Add the header
        updatedMessages.push({
          role: "ai",
          content: "Follow-up Questions:",
          className: "question-header",
        });

        let questions = [];
        if (Array.isArray(result.interview_questions)) {
          questions = result.interview_questions;
        } else {
          // If it's a string, split by numbered pattern like "1. ", "2. ", etc.
          questions = result.interview_questions
            .split(/\d+\.\s+/)
            .filter((q) => q.trim());
        }

        questions.forEach((question, index) => {
          updatedMessages.push({
            role: "system",
            content: `${index + 1}. ${question.trim()}`,
            className: "question-item",
          });
        });

        setMessages((prev) => [...prev, ...updatedMessages]);
      }

      // Update report if available
      if (result.report) {
        setReport(result.report);
      }

      setInputMessage("");
    } catch (error) {
      console.error("Error processing message:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "system",
          content:
            "Sorry, there was an error processing your message. Please try again.",
        },
      ]);
    } finally {
      setIsProcessing(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: 16000,
          echoCancellation: true,
          noiseSuppression: true,
        },
      });

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: "audio/webm;codecs=opus",
        audioBitsPerSecond: 16000,
      });
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/webm;codecs=opus",
        });
        processAudioInput(audioBlob);

        // Stop all tracks of the stream
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start(100); // Start recording with 100ms timeslices
      setIsRecording(true);

      setMessages((prev) => [
        ...prev,
        {
          role: "system",
          content:
            "Recording started. Speak clearly and then click the mic button again to stop.",
        },
      ]);
    } catch (error) {
      console.error("Error starting recording:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "system",
          content:
            "Could not access microphone. Please check permissions and try again.",
        },
      ]);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setMessages((prev) => [
        ...prev,
        { role: "system", content: "Processing your speech..." },
      ]);
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const processAudioInput = async (audioBlob) => {
    setIsProcessing(true);

    try {
      // Process the audio input
      const result = await processSpeech(audioBlob);

      // Add transcription to chat
      if (result.transcribed_text) {
        setMessages((prev) => [
          ...prev,
          { role: "user", content: result.transcribed_text },
        ]);
      }

      // Add grammar analysis if available
      if (result.language_analysis) {
        setMessages((prev) => [
          ...prev,
          {
            role: "system",
            content: `Grammar Analysis: ${result.language_analysis[0][1]}`,
          },
        ]);
      }

      // Add performance analysis if available
      if (result.performance_analysis) {
        // Scores
        setMessages((prev) => [
          ...prev,
          {
            role: "system",
            content: `Scores: \n${result.performance_analysis[0][1]}`,
          },
        ]);

        // Suggestions
        if (result.performance_analysis[2]) {
          setMessages((prev) => [
            ...prev,
            {
              role: "system",
              content: `Improvement Suggestions: ${result.performance_analysis[2][1]}`,
            },
          ]);
        }
      }

      // Add follow-up questions
      if (
        result.interview_questions &&
        result.interview_questions !== "No questions generated"
      ) {
        const updatedMessages = [];

        updatedMessages.push({
          role: "ai",
          content: "Follow-up Questions:",
          className: "question-header",
        });

        let questions = [];
        if (Array.isArray(result.interview_questions)) {
          questions = result.interview_questions;
        } else {
          questions = result.interview_questions
            .split(/\d+\.\s+/)
            .filter((q) => q.trim());
        }

        questions.forEach((question, index) => {
          updatedMessages.push({
            role: "ai",
            content: `${index + 1}. ${question.trim()}`,
            className: "question-item",
          });
        });

        setMessages((prev) => [...prev, ...updatedMessages]);
      }

      // Update report and charts
      if (result.report) {
        setReport(result.report);
        setResult(result); // Store the full result for charts
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "system",
          content:
            "Sorry, there was an error processing your speech. Please try again.",
        },
      ]);
    } finally {
      setIsProcessing(false);
    }
  };

  const processResponse = (response) => {
    console.log("Full API response:", response); // Debug log

    const messages = [];

    // 1. Add user's input
    if (response.input_text || response.transcribed_text) {
      messages.push({
        role: "user",
        content: response.input_text || response.transcribed_text,
      });
    }

    // Add scores if present
    if (response.scores) {
      const scoreLines = response.scores
        .split("\n")
        .filter((line) => line.trim()) // remove empty lines
        .map((line) => line.trim())
        .join("\n"); // combine all scores into a single string

      messages.push({
        role: "system",
        content: `Scores:\n${scoreLines}`,
        className: "score-box", // you can style this differently if you want
      });
    }

    // // 3. Add Feedback
    // if (response.feedback) {
    //   messages.push({
    //     role: "ai",
    //     content: "Detailed Feedback:",
    //     className: "feedback-header",
    //   });
    //   const feedbackLines = response.feedback.split("\n");
    //   feedbackLines.forEach((line) => {
    //     if (line.trim()) {
    //       messages.push({
    //         role: "ai",
    //         content: line.trim(),
    //         className: "feedback-item",
    //       });
    //     }
    //   });
    // }

    // Add suggestions if present
    if (response.Suggestions) {
      const suggestionLines = response.Suggestions.split("\n")
        .map((line) => line.trim())
        .filter((line) => line.length > 0);

      let revisedVersion = "";
      let bulletPoints = [];

      suggestionLines.forEach((line) => {
        if (line.startsWith("Here's a revised version")) {
          revisedVersion += `${line}`;
        } else if (line.startsWith('"') || revisedVersion.endsWith(":")) {
          // If the next line is the actual revised content
          revisedVersion += `\n${line}`;
        } else if (line.startsWith("- ") || line.startsWith("• - ")) {
          bulletPoints.push(`• ${line.replace(/^•?\s*- /, "")}`);
        }
      });

      if (revisedVersion) {
        messages.push({
          role: "system",
          content: `Suggestions:\n${revisedVersion}`,
          className: "suggestion-box",
        });
      }

      if (bulletPoints.length > 0) {
        messages.push({
          role: "system",
          content: `Suggestions:\n${bulletPoints.join("\n")}`,
          className: "suggestion-box",
        });
      }
    }

    // 5. Add Follow-up Questions
    if (
      response["Follow-up Questions"] &&
      response["Follow-up Questions"] !== "No questions generated"
    ) {
      messages.push({
        role: "ai",
        content: "Follow-up Questions:",
        className: "question-header",
      });

      let questions = [];
      if (Array.isArray(response["Follow-up Questions"])) {
        questions = response["Follow-up Questions"];
      } else {
        // If it's a string, split by numbered pattern
        questions = response["Follow-up Questions"]
          .split(/\d+\.\s+/)
          .filter((q) => q.trim());
      }

      questions.forEach((question, index) => {
        messages.push({
          role: "system",
          content: `${index + 1}. ${question.trim()}`,
          className: "question-item",
        });
      });
    }

    console.log("Processed messages:", messages); // Debug log
    return messages;
  };

  const handleNewChat = () => {
    setMessages([
      {
        role: "system",
        content:
          "Welcome to the English Communication Assessment Tool! You can type or speak to begin your assessment.",
      },
    ]);
    setCurrentChatId(null);
    setReport(null);
    setResult(null);
  };

  const handleSelectChat = async (chatId) => {
    try {
      const response = await fetch(
        `http://localhost:8080/api/chat-histories/${chatId}`
      );
      const chatData = await response.json();

      // Reconstruct messages from chat history
      const newMessages = processResponse(chatData);
      setMessages(newMessages);
      setCurrentChatId(chatId);

      // Set report and result if available
      if (chatData.report) {
        setReport(chatData.report);
      }
      if (chatData.charts) {
        setResult({ ...chatData, charts: chatData.charts });
      }
    } catch (error) {
      console.error("Error loading chat:", error);
    }
  };

  return (
    <div className="flex h-screen bg-neutral-800">
      {showSidebar && (
        <Sidebar
          onNewChat={handleNewChat}
          onSelectChat={handleSelectChat}
          currentChatId={currentChatId}
        />
      )}

      <div className="flex-1 flex flex-col relative">
        <div className="absolute top-0 left-0 p-4 z-10">
          <button
            onClick={() => setShowSidebar(!showSidebar)}
            className="p-2 hover:bg-gray-700 rounded-lg text-gray-400 hover:text-white transition-colors"
          >
            ☰
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 pt-16 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              } items-end space-x-2`}
            >
              {message.role === "system" && (
                <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
                  <span className="text-white text-sm">AI</span>
                </div>
              )}
              {message.role === "ai" && <div className="w-8 h-8"></div>}
              <div
                className={`max-w-[70%] p-4 rounded-2xl ${
                  message.role === "user"
                    ? "bg-blue-600 text-white rounded-br-none"
                    : message.className === "score-item"
                    ? "bg-gray-800 text-green-400 rounded-bl-none"
                    : message.className === "feedback-item"
                    ? "bg-gray-800 text-orange-400 rounded-bl-none"
                    : message.className === "question-item"
                    ? "bg-gray-800 text-yellow-400 rounded-bl-none"
                    : message.className === "question-header"
                    ? "bg-gray-700 text-white font-bold rounded-bl-none"
                    : "bg-gray-800 text-white rounded-bl-none"
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              </div>
              {message.role === "user" && (
                <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                  <span className="text-white text-sm">You</span>
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="border-t border-gray-800 p-4 bg-gray-900">
          <form onSubmit={handleSubmit} className="flex items-center gap-2">
            <button
              type="button"
              onClick={toggleRecording}
              className={`p-3 rounded-full transition-colors ${
                isRecording
                  ? "bg-red-600 text-white hover:bg-red-700"
                  : "bg-gray-700 hover:bg-gray-600 text-white"
              }`}
              disabled={isProcessing}
            >
              {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
            </button>

            <div className="flex-1 relative">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message..."
                className="w-full p-3 pr-12 rounded-full border border-gray-700 bg-gray-800 text-white focus:outline-none focus:border-blue-600"
                disabled={isRecording || isProcessing}
              />
              {isProcessing && (
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <Loader className="animate-spin text-gray-400" size={20} />
                </div>
              )}
            </div>

            <button
              type="submit"
              className="p-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors disabled:bg-gray-700 disabled:cursor-not-allowed"
              disabled={(!inputMessage.trim() && !isRecording) || isProcessing}
            >
              <Send size={20} />
            </button>

            {report && (
              <button
                type="button"
                onClick={() => setShowReport(!showReport)}
                className={`p-3 rounded-full transition-colors ${
                  showReport
                    ? "bg-green-600 text-white"
                    : "bg-gray-700 text-white hover:bg-gray-600"
                }`}
              >
                <FileText size={20} />
              </button>
            )}
          </form>
        </div>

        {showReport && report && (
          <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4">
            <div className="bg-gray-900 rounded-lg p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto text-white">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold">Assessment Report</h3>
                <button
                  onClick={() => setShowReport(false)}
                  className="text-gray-400 hover:text-white"
                >
                  ×
                </button>
              </div>

              <pre className="whitespace-pre-wrap text-sm text-gray-300 mb-6">
                {report}
              </pre>

              {result?.charts && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                  {result.charts.radar && (
                    <div className="bg-gray-800 p-4 rounded-lg">
                      <h4 className="text-lg font-medium mb-2">
                        Skills Assessment
                      </h4>
                      <div className="relative">
                        <img
                          src={`data:image/png;base64,${result.charts.radar}`}
                          alt="Skills Radar Chart"
                          className="w-full"
                          onError={(e) => {
                            console.error("Error loading radar chart");
                            e.target.style.display = "none";
                          }}
                        />
                      </div>
                    </div>
                  )}
                  {result.charts.vocabulary && (
                    <div className="bg-gray-800 p-4 rounded-lg">
                      <h4 className="text-lg font-medium mb-2">
                        Vocabulary Analysis
                      </h4>
                      <div className="relative">
                        <img
                          src={`data:image/png;base64,${result.charts.vocabulary}`}
                          alt="Vocabulary Analysis Chart"
                          className="w-full"
                          onError={(e) => {
                            console.error("Error loading vocabulary chart");
                            e.target.style.display = "none";
                          }}
                        />
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
