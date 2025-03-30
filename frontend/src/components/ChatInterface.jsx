"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Mic, MicOff, FileText, Loader } from "lucide-react";
import { processText, processSpeech, checkApiHealth } from "@/services/api";

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

      // Add the system responses
      if (result.language_analysis) {
        // Add grammar analysis
        setMessages((prev) => [
          ...prev,
          {
            role: "system",
            content: `Grammar Analysis: ${result.language_analysis[0][1]}`,
          },
        ]);

        // Add grammar score
        if (result.language_analysis[1]) {
          setMessages((prev) => [
            ...prev,
            {
              role: "system",
              content: `Grammar Score: ${result.language_analysis[1][1]}`,
            },
          ]);
        }
      }

      if (result.performance_analysis) {
        // Add vocabulary analysis
        setMessages((prev) => [
          ...prev,
          {
            role: "system",
            content: `${result.performance_analysis[0][1]}`,
          },
        ]);

        // Add improvement suggestions
        if (result.performance_analysis[1]) {
          setMessages((prev) => [
            ...prev,
            {
              role: "system",
              content: `Improvement Suggestions: ${result.performance_analysis[1][1]}`,
            },
          ]);
        }
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

      // Add analysis results
      if (result.language_analysis) {
        result.language_analysis.forEach((analysis) => {
          setMessages((prev) => [
            ...prev,
            { role: "system", content: `${analysis[0]} ${analysis[1]}` },
          ]);
        });
      }

      if (result.performance_analysis) {
        result.performance_analysis.forEach((analysis) => {
          setMessages((prev) => [
            ...prev,
            { role: "system", content: `${analysis[0]} ${analysis[1]}` },
          ]);
        });
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

  return (
    <div className="flex flex-col h-screen bg-black">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
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
            <div
              className={`max-w-[70%] p-4 rounded-2xl ${
                message.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
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

      {/* Input Area */}
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

      {/* Report Panel */}
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

            {/* Text Report */}
            <pre className="whitespace-pre-wrap text-sm text-gray-300 mb-6">
              {report}
            </pre>

            {/* Visualizations */}
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
  );
}
