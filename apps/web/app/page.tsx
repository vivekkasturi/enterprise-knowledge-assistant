import ChatBox from "./features/chat/components/ChatBox";


export default function Home() {

  return (
    <main className="min-h-screen bg-zinc-50 px-6 py-10 text-zinc-950">
      <div className="mx-auto flex max-w-2xl flex-col gap-6">
        <h1 className="text-3xl font-semibold">Chat API Test</h1>
        <ChatBox />
      </div>
    </main>
  );
}