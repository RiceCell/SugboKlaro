import { genAI } from "./geminiClient";
import chatbotSources from "../../data/chatbot_sources.json";
import brcwgsResults from "../../data/compliance_results/brcwgs.json";
import qscfResults from "../../data/compliance_results/qscf.json";
import ucaResults from "../../data/compliance_results/uca.json";

export async function generateProjectOverview(reportItem: any): Promise<string> {
  const model = genAI.getGenerativeModel({
    model: "gemini-3.5-flash-lite",
    generationConfig: {
      temperature: 0.2,
      maxOutputTokens: 300,
    },
    systemInstruction: `
      You are the SugboKlaro AI Overview generator for Cebu City public financial and procurement compliance reports.
      Your task is to generate a concise, objective, and high-level 2 to 4 sentence summary for a given report finding, similar to Google Search AI Overviews.

      STRICT OUTPUT GUIDELINES:
      1. Length: Exactly 2 to 4 sentences. Do not use bullet points or introductory phrases like "Here is the summary".
      2. If status is "FLAGGED" or "FAIL":
         - Clearly state the specific reason why the item was flagged (such as zero-variance bid, excessive vendor concentration, budget ceiling violation, cash flow arithmetic mismatch, or past-due unliquidated cash advance).
         - Include the key figures or threshold violations involved.
         - Mention the relevant legal standard (e.g., RA 9184, COA Circulars) in plain terms.
      3. If status is "PASS":
         - Provide a short recap and summary of the project or fund transaction, confirming that it complies with allowable thresholds and statutory limits.
      4. If status is "MISSING_DATA":
         - State what critical record or value is absent and needed for verification.
      5. Tone: Factual, professional, non-accusatory, and grounded strictly in the provided data context. Never hallucinate.

      Data Context:
      - BRCWGS Data: ${JSON.stringify(brcwgsResults)}
      - QSCF Data: ${JSON.stringify(qscfResults)}
      - UCA Data: ${JSON.stringify(ucaResults)}
      - Legal & Regulatory Sources: ${JSON.stringify(chatbotSources)}
    `
  });

  const ruleId = reportItem?.rule_id || "N/A";
  const status = reportItem?.status || "UNKNOWN";
  const message = reportItem?.message || "No observation recorded.";
  const legalBasis = reportItem?.legal_basis
    ? `${reportItem.legal_basis.law} ${reportItem.legal_basis.section}: ${reportItem.legal_basis.title}`
    : "N/A";
  const details = reportItem?.details ? JSON.stringify(reportItem.details) : "N/A";
  const rowRef = reportItem?.row_ref ?? "N/A";

  const prompt = `Generate a 2-4 sentence AI overview for this compliance finding:
- Document Type / Rule ID: ${ruleId}
- Status: ${status}
- Finding / Message: ${message}
- Legal Basis: ${legalBasis}
- Item Details: ${details}
- Row / Identifier: ${rowRef}
`;

  try {
    const result = await model.generateContent(prompt);
    const text = result.response.text();
    return text.trim();
  } catch (error) {
    console.error("Failed to generate AI overview:", error);
    throw error;
  }
}