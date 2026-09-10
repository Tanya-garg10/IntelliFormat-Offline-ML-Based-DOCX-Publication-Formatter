import express from "express";
import path from "path";
import fs from "fs";
import { execFile } from "child_process";
import { promisify } from "util";
import multer from "multer";
import { createServer as createViteServer } from "vite";

const execFileAsync = promisify(execFile);
const app = express();
const PORT = 3000;

app.use(express.json());

// Configure multer storage for uploaded manuscripts
const uploadDir = path.join(process.cwd(), "uploads");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

const storage = multer.diskStorage({
  destination: (_req, _file, cb) => cb(null, uploadDir),
  filename: (_req, file, cb) => {
    const safeName = file.originalname.replace(/[^a-zA-Z0-9._-]/g, "_");
    cb(null, `${Date.now()}_${safeName}`);
  },
});
const upload = multer({ storage });

let bootstrapPromise: Promise<void> | null = null;

async function ensurePythonEnvironment(): Promise<void> {
  try {
    await execFileAsync("python3", ["-c", "import docx, sklearn, joblib, numpy, pandas, psutil"]);
    return;
  } catch (_err) {
    console.log("Python dependencies missing. Bootstrapping container environment...");
    try {
      await execFileAsync("sh", [
        "-c",
        "mkdir -p /etc/dpkg/dpkg.cfg.d && echo 'force-confold' > /etc/dpkg/dpkg.cfg.d/force-conf && echo 'force-confdef' >> /etc/dpkg/dpkg.cfg.d/force-conf && DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip python3-docx python3-sklearn python3-joblib python3-numpy python3-pandas python3-psutil"
      ], { timeout: 180000 });
      console.log("Python dependencies successfully initialized.");
    } catch (e) {
      console.error("Dependency bootstrap warning:", e);
    }
  }
}

// Helper to run server_api.py safely
async function runPythonApi(action: string, extraArgs: string[] = []): Promise<any> {
  if (!bootstrapPromise) {
    bootstrapPromise = ensurePythonEnvironment();
  }
  await bootstrapPromise;

  const scriptPath = path.join(process.cwd(), "server_api.py");
  const args = [scriptPath, "--action", action, ...extraArgs];

  try {
    const { stdout, stderr } = await execFileAsync("python3", args, {
      maxBuffer: 20 * 1024 * 1024,
    });
    if (stderr && !stdout) {
      console.error("Python API stderr:", stderr);
    }
    return JSON.parse(stdout.trim());
  } catch (error: any) {
    if (error && typeof error.message === "string" && error.message.includes("ModuleNotFoundError")) {
      console.log("Detected ModuleNotFoundError during execution, attempting immediate re-bootstrap...");
      bootstrapPromise = ensurePythonEnvironment();
      await bootstrapPromise;
      try {
        const retryResult = await execFileAsync("python3", args, {
          maxBuffer: 20 * 1024 * 1024,
        });
        return JSON.parse(retryResult.stdout.trim());
      } catch (retryErr: any) {
        console.error(`Retry failed for '${action}':`, retryErr);
        return { error: retryErr.message || "Failed to execute Python service after retry" };
      }
    }
    console.error(`Failed to execute action '${action}':`, error);
    return { error: error.message || "Failed to execute Python service" };
  }
}

// API Routes FIRST
app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", offline: true, engine: "IntelliFormat v1.0" });
});

app.post("/api/upload", upload.single("manuscript"), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "No file uploaded." });
  }

  const filePath = req.file.path;
  const summary = await runPythonApi("summary", ["--file", filePath]);
  res.json({
    success: true,
    file_path: filePath,
    filename: req.file.originalname,
    summary,
  });
});

app.get("/api/summary", async (req, res) => {
  const filePath = (req.query.file as string) || "samples/input.docx";
  const result = await runPythonApi("summary", ["--file", filePath]);
  res.json(result);
});

app.get("/api/analyze", async (req, res) => {
  const filePath = (req.query.file as string) || "samples/input.docx";
  const result = await runPythonApi("analyze", ["--file", filePath]);
  res.json(result);
});

app.post("/api/format", async (req, res) => {
  const filePath = req.body.file || "samples/input.docx";
  const outputName = req.body.output || `formatted_${Date.now()}.docx`;
  const outputDir = path.join(process.cwd(), "output");
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  const outputPath = path.join(outputDir, path.basename(outputName));

  const specs = JSON.stringify(req.body.specs || {});
  const args = ["--file", filePath, "--output", outputPath, "--specs", specs];
  if (req.body.include_toc !== false) {
    args.push("--toc");
  }

  const result = await runPythonApi("format", args);
  res.json(result);
});

app.get("/api/benchmark", async (_req, res) => {
  const result = await runPythonApi("benchmark");
  res.json(result);
});

app.get("/api/accuracy", async (_req, res) => {
  const result = await runPythonApi("accuracy");
  res.json(result);
});

app.get("/api/download", (req, res) => {
  const targetFile = (req.query.file as string) || "output/formatted_book.docx";
  const resolvedPath = path.resolve(process.cwd(), targetFile);

  if (fs.existsSync(resolvedPath)) {
    res.download(resolvedPath, path.basename(resolvedPath));
  } else {
    res.status(404).json({ error: "File not found" });
  }
});

async function startServer() {
  // Proactively verify and ensure python dependencies in background
  bootstrapPromise = ensurePythonEnvironment();

  // Add security headers for production
  app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    next();
  });

  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (_req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`IntelliFormat server running on port ${PORT}`);
  });
}

startServer();
