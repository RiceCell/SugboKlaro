import { genAI } from "./geminiClient";
import chatbotSources from "../../data/chatbot_sources.json";
import brcwgsResults from "../../data/compliance_results/brcwgs.json";

export async function generateProjectOverview(projectRef: string): Promise<void> {
  const model = genAI.getGenerativeModel({
    model: "gemini-3.5-flash-lite",
    systemInstruction: `
      You are the SugboKlaro AI Overview generator.
      Create a short, formal, and concise overview explaining why a project passed or failed compliance checks.
      Use the provided JSON data to explain the specific flags (e.g., Zero-Variance, Vendor Concentration, ABC Ceiling) based on Philippine procurement laws.
      
      Data Context:
      Chatbot Sources: ${JSON.stringify(chatbotSources)}
      Compliance Results: ${JSON.stringify(brcwgsResults)}
      
      Do not hallucinate. Be objective and non-accusatory.
    `
  });

  // Target the specific project using the reference number
  const prompt = `Generate a concise compliance overview for the project with reference number: ${projectRef}. Explain any anomalies or confirm its compliance based on the context.`;
  
    try {
        const result = await model.generateContent(prompt);
        console.log(`[AI Overview Result for ${projectRef}]:`);
        console.log(result.response.text());
    } catch (error) {
        console.error("Failed to generate AI overview:", error);
    };
}