import express from "express";
import path from "path";
import dotenv from "dotenv";
import { GoogleGenAI, Type } from "@google/genai";
import { createServer as createViteServer } from "vite";

// Load environment variables
dotenv.config();

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json({ limit: "10mb" }));

// Lazy initializer for Gemini client
let aiClient: GoogleGenAI | null = null;
function getGeminiClient(): GoogleGenAI {
  if (!aiClient) {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error("GEMINI_API_KEY environment variable is missing. Please add it to your secrets or environment.");
    }
    aiClient = new GoogleGenAI({
      apiKey,
      httpOptions: {
        headers: {
          "User-Agent": "aistudio-build",
        },
      },
    });
  }
  return aiClient;
}

// Ensure server handles errors gracefully
const handleRouteError = (res: express.Response, error: any) => {
  console.error("API Route Error:", error);
  res.status(500).json({
    error: error.message || "An unexpected error occurred during processing.",
  });
};

// API: Check status/health
app.get("/api/health", (req, res) => {
  res.json({ status: "ok", message: "StudyMate AI Backend Running" });
});

// API: AI Chat Q&A
app.post("/api/chat", async (req, res) => {
  try {
    const { messages } = req.body;
    if (!messages || !Array.isArray(messages)) {
      return res.status(400).json({ error: "Invalid messages array provided." });
    }

    const ai = getGeminiClient();

    // Map client messages to Gemini content format
    // Filter to last 15 messages to prevent context overflow or slow responses
    const history = messages.slice(-15).map((m: any) => ({
      role: m.role === "user" ? "user" : "model",
      parts: [{ text: m.content }],
    }));

    // The last message is the current prompt
    const lastMessage = history.pop();
    const promptText = lastMessage?.parts?.[0]?.text || "";

    const chatSession = ai.chats.create({
      model: "gemini-3.5-flash",
      config: {
        systemInstruction: "You are StudyMate AI, a friendly, modern, and encouraging academic tutor. Help the student understand complex concepts, solve homework problems step-by-step, explain equations, or practice language skills. Keep your answers clear, concise, and structured with clean markdown. Always maintain an encouraging and positive educational tone. Do not give direct answers immediately if leading questions would help them learn better.",
      },
      history: history,
    });

    const response = await chatSession.sendMessage({ message: promptText });
    res.json({ content: response.text });
  } catch (error: any) {
    handleRouteError(res, error);
  }
});

// API: Study Planner
app.post("/api/planner", async (req, res) => {
  try {
    const { subject, examDate, hoursPerDay } = req.body;
    if (!subject || !examDate || !hoursPerDay) {
      return res.status(400).json({ error: "Subject, exam date, and hours per day are required." });
    }

    const ai = getGeminiClient();
    const prompt = `Generate a comprehensive day-by-day study schedule for the subject: "${subject}" leading up to the exam date: "${examDate}". The student can dedicate ${hoursPerDay} hours per day to study. Outline the key milestones, specific topics, daily study breakdown, and expert preparation tips. Return the data as structured JSON.`;

    const response = await ai.models.generateContent({
      model: "gemini-3.5-flash",
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            subject: { type: Type.STRING },
            examDate: { type: Type.STRING },
            daysRemaining: { type: Type.INTEGER, description: "Number of study days between today and the exam." },
            overallStrategy: { type: Type.STRING, description: "General summary strategy for scoring high." },
            milestones: {
              type: Type.ARRAY,
              items: { type: Type.STRING },
              description: "Key milestones to achieve throughout the study period."
            },
            schedule: {
              type: Type.ARRAY,
              items: {
                type: Type.OBJECT,
                properties: {
                  day: { type: Type.STRING, description: "Day label (e.g., 'Day 1', 'Day 2' or specific dates)" },
                  title: { type: Type.STRING, description: "Main theme of the study session" },
                  topics: {
                    type: Type.ARRAY,
                    items: { type: Type.STRING },
                    description: "Specific sub-topics to cover"
                  },
                  hours: { type: Type.NUMBER, description: "Number of hours to study on this day" },
                  activities: {
                    type: Type.ARRAY,
                    items: { type: Type.STRING },
                    description: "Specific actions (e.g., 'Read chapter 3', 'Solve 10 practice equations', 'Flashcards')"
                  },
                  tips: { type: Type.STRING, description: "Encouraging tip or focus area for this day" }
                },
                required: ["day", "title", "topics", "hours", "activities"]
              }
            }
          },
          required: ["subject", "examDate", "overallStrategy", "milestones", "schedule"]
        }
      }
    });

    const parsedPlan = JSON.parse(response.text || "{}");
    res.json(parsedPlan);
  } catch (error: any) {
    handleRouteError(res, error);
  }
});

// API: Quiz Generator
app.post("/api/quiz", async (req, res) => {
  try {
    const { topic } = req.body;
    if (!topic) {
      return res.status(400).json({ error: "Topic is required for quiz generation." });
    }

    const ai = getGeminiClient();
    const prompt = `Generate exactly 5 multiple-choice questions (MCQs) for the topic: "${topic}". Each question must have exactly 4 options, a correct answer index (0, 1, 2, or 3), and a clear, constructive explanation of why the correct option is right and others are wrong. Make the questions challenging yet educational. Return the data as structured JSON.`;

    const response = await ai.models.generateContent({
      model: "gemini-3.5-flash",
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.ARRAY,
          items: {
            type: Type.OBJECT,
            properties: {
              question: { type: Type.STRING, description: "The multiple choice question text." },
              options: {
                type: Type.ARRAY,
                items: { type: Type.STRING },
                description: "Exactly 4 options to choose from."
              },
              correctAnswerIndex: { type: Type.INTEGER, description: "0-based index of the correct option (0 to 3)." },
              explanation: { type: Type.STRING, description: "Explaining the correct answer and reinforcing learning." }
            },
            required: ["question", "options", "correctAnswerIndex", "explanation"]
          }
        }
      }
    });

    const parsedQuiz = JSON.parse(response.text || "[]");
    res.json(parsedQuiz);
  } catch (error: any) {
    handleRouteError(res, error);
  }
});

// Setup Vite Dev Server Middleware or Static production file serving
async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    console.log("Starting server in DEVELOPMENT mode with Vite Middleware...");
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    console.log("Starting server in PRODUCTION mode with static file assets...");
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`StudyMate AI Server successfully listening on http://0.0.0.0:${PORT}`);
  });
}

startServer().catch((err) => {
  console.error("Critical: Failed to start StudyMate AI server:", err);
  process.exit(1);
});
