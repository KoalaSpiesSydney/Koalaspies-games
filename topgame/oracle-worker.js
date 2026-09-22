/* AI oracle server for "Ask the AI oracle" (Top 5 game)
   A Cloudflare Worker that asks Claude to rank the answers to a Top 5 question.
   It keeps your Anthropic API key secret: the key lives in the worker's settings, never in the game page.

   Settings (Cloudflare dashboard > your worker > Settings > Variables and Secrets):
     ANTHROPIC_API_KEY  (Secret, required)   your key from console.anthropic.com
     ALLOWED_ORIGIN     (Text, recommended)  your website address, e.g. https://www.example.com
                                             (leave empty while testing; then any site can use it)
     MODEL              (Text, optional)     a Claude model id; defaults to the one below
*/
const DEFAULT_MODEL = "claude-haiku-4-5";

function buildPrompt(q, n) {
  const today = new Date().toLocaleDateString("en-AU", { day: "numeric", month: "long", year: "numeric" });
  return `You are "The AI oracle" in a party game played like Family Feud. Teams try to guess the answers on YOUR board, so give your own honest best judgement from what you know (today is ${today}). Commit to one ranking — don't hedge.

Question: "${q}"

Give exactly ${n} answers ranked from #1 (top) down. For each:
- "name": short (max 4 words)
- "aliases": up to 4 other ways players might say it (nicknames, short forms, other spellings, e.g. "USA", "United States", "America")
- "points": how strongly you back this answer; integers that go down the list and add up to 100
- "reason": a punchy one-sentence reason (max 18 words) read aloud when it's revealed
Keep it family-friendly. If the question is not family-friendly, answer a family-friendly version of it.

Reply with only JSON in this shape:
{"answers":[{"name":"...","aliases":["..."],"points":38,"reason":"..."}]}`;
}

export default {
  async fetch(request, env) {
    const allowed = env.ALLOWED_ORIGIN || "*";
    const cors = {
      "Access-Control-Allow-Origin": allowed,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "content-type",
      "Vary": "Origin",
    };
    const reply = (obj, status = 200) =>
      new Response(JSON.stringify(obj), { status, headers: { ...cors, "content-type": "application/json" } });

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (request.method !== "POST") return reply({ error: "Use POST" }, 405);
    if (allowed !== "*" && request.headers.get("Origin") !== allowed) return reply({ error: "Not allowed" }, 403);
    if (!env.ANTHROPIC_API_KEY) return reply({ error: "Server is missing ANTHROPIC_API_KEY" }, 500);

    let body;
    try { body = await request.json(); } catch { return reply({ error: "Send JSON" }, 400); }
    const question = String(body.question || "").trim().slice(0, 200);
    const n = Math.min(8, Math.max(3, parseInt(body.n, 10) || 5));
    if (question.length < 3) return reply({ error: "Question too short" }, 400);

    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
      },
      body: JSON.stringify({
        model: env.MODEL || DEFAULT_MODEL,
        max_tokens: 1200,
        messages: [{ role: "user", content: buildPrompt(question, n) }],
      }),
    });
    if (r.status === 429) return reply({ error: "Busy" }, 429);
    if (!r.ok) return reply({ error: "AI error " + r.status }, 502);

    const data = await r.json();
    const text = (data.content || []).filter(c => c.type === "text").map(c => c.text).join("");
    const m = text.match(/\{[\s\S]*\}/);
    if (!m) return reply({ error: "No answer" }, 502);
    try { return reply(JSON.parse(m[0])); } catch { return reply({ error: "Bad answer" }, 502); }
  },
};
