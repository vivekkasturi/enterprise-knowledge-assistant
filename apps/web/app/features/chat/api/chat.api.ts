import { chatRequest, chatResponse } from "../types/chat.types";


const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function getChatStatus(){
    console.log("Fetching chat status from API...");
    const response = await fetch (`${API_BASE_URL}/chat`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    }
    )
    if (!response.ok) {
        throw new Error(`Failed to fetch chat status: ${response.status}`);
    }

    return response.json()
}


export async function chatResponseApi(request:chatRequest): Promise<chatResponse> {
    console.log("Requesting chat response with request:", request);
    const response = await fetch(`${API_BASE_URL}/chat/response`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
    })

    if (!response.ok) {
        throw new Error(`Failed to request chat response: ${response.status}`);
    }

    return response.json()
}

export async function chatStreamAPI(request:chatRequest, onChunk: (chunk: string) => void): Promise<void> {
    console.log("Requesting chat stream...");
    const response = await fetch(`${API_BASE_URL}/chat/stream`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(request),

    })

        if (!response.ok) {
            throw new Error(`Failed to request chat response: ${response.status}`);
        }
        const reader = response.body?.getReader();
            console.log("Reader obtained from response body:", reader);
            if (!reader) {
                throw new Error("Failed to get reader from response body");
            }
            const decoder = new TextDecoder();
            while(true) {
                const { done, value } = await reader.read();
                    if (done) {
                        console.log("Stream finished.");
                        break;
                    }

                const chunk = decoder.decode(value, { stream: true });
                console.log("Received chunk:", chunk);
                onChunk(chunk);
            }
    }


