"use client";

import { useState } from "react";
import { chatResponseApi, getChatStatus } from "../api/chat.api"

export default function ChatBox() {
  const [message, setMessage] = useState("Hello from frontend");
  const [result, setResult] = useState<string>("No API call yet.");
  const [isLoading, setIsLoading] = useState(false);

  async function handleGetStatus() {
    setIsLoading(true);
    try {
      const data = await getChatStatus();
      setResult(JSON.stringify(data));
    } catch (error) {
      setResult(error instanceof Error ? error.message : "Unknown error");
    } finally {
      setIsLoading(false);
    }
  }

  async function handlePostMessage() {
    setIsLoading(true);
    try {
      const data = await chatResponseApi({ message });
      setResult(JSON.stringify(data));
    } catch (error) {
      setResult(error instanceof Error ? error.message : "Unknown error");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-zinc-50 px-6 py-10 text-zinc-950">
      <div className="mx-auto flex max-w-2xl flex-col gap-6">
        <h1 className="text-3xl font-semibold">Chat API Test</h1>

        <div className="flex flex-col gap-3">
          <label className="text-sm font-medium" htmlFor="message">
            Message
          </label>
          <input
            id="message"
            className="rounded-md border border-zinc-300 bg-white px-3 py-2"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
          />
        </div>

        <div className="flex gap-3">
          <button
            className="rounded-md bg-zinc-950 px-4 py-2 text-white disabled:opacity-50"
            disabled={isLoading}
            onClick={handleGetStatus}
            type="button"
          >
            GET Status
          </button>
          <button
            className="rounded-md bg-blue-700 px-4 py-2 text-white disabled:opacity-50"
            disabled={isLoading}
            onClick={handlePostMessage}
            type="button"
          >
            POST Response
          </button>
        </div>

        <pre className="min-h-32 overflow-auto rounded-md border border-zinc-200 bg-white p-4 text-sm">
          {result}
        </pre>
      </div>
    </main>
  );
}
