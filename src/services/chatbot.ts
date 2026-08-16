import { genAI } from "./geminiClient";

import chatbotSources from "../../data/chatbot_sources.json";
import brcgwsResults from "../../data/compliance_results/brcwgs_2026_q1.json";
import qscfResults from "../../data/compliance_results/qscf_2026_q1.json";
import ucaResults from "../../data/compliance_results/uca_2026_q1.json";

export interface Message{
    role: 'user' | 'bot';
    text: string;
}

export async function chatbotKnowledgebase(userQues: string): Promise<string>{
    try{
        const knowledgeSource = JSON.stringify({
        chatbotSources: chatbotSources,
        budgetReports: qscfResults,
        procurementReports: brcgwsResults,
        specialpurposefundReports: ucaResults,
    });

    const model = genAI.getGenerativeModel({
        model: "gemini-3.5-flash-lite",
        systemInstruction: 
            "You are a strict compliance assistant named omai. Answer the user question " +
            "using ONLY the provided Knowledge Base datasets. Keep your answer under 2 sentences. " +
            "Be highly concise. If the information isn't in the dataset, state exactly: " +
            "'There are no such records in our compliance records.' Never mention files or JSON. " +
            "Do not hallucinate. Be objective and non-accusatory."
    });

    const response = await model.generateContent({
        contents: [
            { role: "user", parts: [{ text: `knowledge Source: \n${knowledgeSource}\n user Question: \n${userQues}` }] }
        ],
        generationConfig: {
            temperature: 0.1,
            maxOutputTokens: 200,
        }
    });

    return response.response.text() || "no response found";
        }
    catch (error){ 
        console.error("Error: ", error);
        return "Error imnida";
    }
}