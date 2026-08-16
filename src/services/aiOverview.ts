import { genAI } from "./geminiClient";

// REMOVED: import chatbotSources, brcwgsResults, qscfResults, ucaResults

export async function generateProjectOverview(reportItem: any): Promise<string> {
  const model = genAI.getGenerativeModel({
    model: "gemini-3.5-flash-lite",
    generationConfig: {
      temperature: 0.1,
      maxOutputTokens: 300,
    },
    systemInstruction: `
      You are the SugboKlaro AI Overview generator for Cebu City public financial and procurement compliance reports.
      Your task is to generate a concise, objective, and high-level 2 to 4 sentence summary for a given report finding.

      STRICT OUTPUT GUIDELINES:
      1. Length: Exactly 2 to 4 sentences. Do not use bullet points or introductory phrases.
      2. If status is "FLAGGED" or "FAIL":
         Explain the specific reason why the item was flagged.
         Include the key figures or threshold violations involved.
         Mention the relevant legal standard provided in the context in plain terms.
      3. If status is "PASS":
         Provide a short recap and summary of the project or fund transaction, confirming compliance.
      4. If status is "MISSING_DATA":
         State what critical record or value is absent.
      5. Tone: Factual, professional, non-accusatory, and grounded strictly in the provided data context.
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

  // Inject only the specific row data into the prompt
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
    return result.response.text().trim();
  } catch (error) {
    console.error("Failed to generate AI overview:", error);
    throw error;
  }
}