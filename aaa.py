// ============================== // DEPLOYABLE VERSION (Next.js) // ============================== // HOW TO USE: // 1. Create a new Next.js app: //    npx create-next-app@latest europa-predictor // 2. Replace the contents of app/page.tsx with this file // 3. Run locally: npm run dev // 4. Deploy easily to Vercel

"use client";

import { useState } from "react";

function impliedProb(odds: number) { return odds > 0 ? 1 / odds : 0; }

function normalize(probs: Record<string, number>) { const total = Object.values(probs).reduce((a, b) => a + b, 0); const normalized: Record<string, number> = {}; for (let key in probs) { normalized[key] = total > 0 ? probs[key] / total : 0; } return normalized; }

function factorial(n: number): number { if (n <= 1) return 1; return n * factorial(n - 1); }

function poissonOver(lambda: number, threshold: number) { let sum = 0; for (let k = 0; k <= threshold; k++) { sum += (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k); } return 1 - sum; }

export default function Home() { const [homeTeam, setHomeTeam] = useState(""); const [awayTeam, setAwayTeam] = useState(""); const [homeStrength, setHomeStrength] = useState(1); const [awayStrength, setAwayStrength] = useState(1); const [avgGoals, setAvgGoals] = useState(2.5); const [odds1, setOdds1] = useState(""); const [oddsX, setOddsX] = useState(""); const [odds2, setOdds2] = useState(""); const [result, setResult] = useState<any>(null);

const calculate = () => { const raw: Record<string, number> = { "1": homeStrength / (homeStrength + awayStrength), "2": awayStrength / (homeStrength + awayStrength), }; raw["X"] = 1 - (raw["1"] + raw["2"]);

const prob1x2 = normalize(raw);

const goalMarkets = {
  over_1_5: poissonOver(avgGoals, 1),
  over_2_5: poissonOver(avgGoals, 2),
  over_3_5: poissonOver(avgGoals, 3),
};

const doubleChance = {
  "1X": prob1x2["1"] + prob1x2["X"],
  "12": prob1x2["1"] + prob1x2["2"],
  "X2": prob1x2["X"] + prob1x2["2"],
};

let oddsProbs = null;

if (odds1 && oddsX && odds2) {
  oddsProbs = normalize({
    "1": impliedProb(parseFloat(odds1)),
    "X": impliedProb(parseFloat(oddsX)),
    "2": impliedProb(parseFloat(odds2)),
  });
}

setResult({ prob1x2, goalMarkets, doubleChance, oddsProbs });

};

return ( <div style={{ minHeight: "100vh", padding: "40px", fontFamily: "Arial, sans-serif", background: "#f4f6f8" }}> <h1 style={{ textAlign: "center" }}>Europa League Predictor ⚽</h1>

<div style={{
    maxWidth: "600px",
    margin: "20px auto",
    padding: "20px",
    background: "white",
    borderRadius: "12px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.1)"
  }}>
    <input placeholder="Home Team" value={homeTeam} onChange={e => setHomeTeam(e.target.value)} />
    <br /><br />
    <input placeholder="Away Team" value={awayTeam} onChange={e => setAwayTeam(e.target.value)} />
    <br /><br />
    <input type="number" step="0.1" placeholder="Home Strength" value={homeStrength} onChange={e => setHomeStrength(parseFloat(e.target.value))} />
    <br /><br />
    <input type="number" step="0.1" placeholder="Away Strength" value={awayStrength} onChange={e => setAwayStrength(parseFloat(e.target.value))} />
    <br /><br />
    <input type="number" step="0.1" placeholder="Average Goals" value={avgGoals} onChange={e => setAvgGoals(parseFloat(e.target.value))} />
    <br /><br />
    <input placeholder="Odds 1" value={odds1} onChange={e => setOdds1(e.target.value)} />
    <br /><br />
    <input placeholder="Odds X" value={oddsX} onChange={e => setOddsX(e.target.value)} />
    <br /><br />
    <input placeholder="Odds 2" value={odds2} onChange={e => setOdds2(e.target.value)} />
    <br /><br />
    <button onClick={calculate} style={{
      padding: "10px 20px",
      borderRadius: "8px",
      border: "none",
      background: "black",
      color: "white",
      cursor: "pointer"
    }}>Calculate</button>
  </div>

  {result && (
    <div style={{
      maxWidth: "600px",
      margin: "20px auto",
      padding: "20px",
      background: "white",
      borderRadius: "12px",
      boxShadow: "0 10px 25px rgba(0,0,0,0.1)"
    }}>
      <h2>Results</h2>
      <p>1: {(result.prob1x2["1"] * 100).toFixed(1)}%</p>
      <p>X: {(result.prob1x2["X"] * 100).toFixed(1)}%</p>
      <p>2: {(result.prob1x2["2"] * 100).toFixed(1)}%</p>

      <p>Over 1.5: {(result.goalMarkets.over_1_5 * 100).toFixed(1)}%</p>
      <p>Over 2.5: {(result.goalMarkets.over_2_5 * 100).toFixed(1)}%</p>
      <p>Over 3.5: {(result.goalMarkets.over_3_5 * 100).toFixed(1)}%</p>

      <p>1X: {(result.doubleChance["1X"] * 100).toFixed(1)}%</p>
      <p>12: {(result.doubleChance["12"] * 100).toFixed(1)}%</p>
      <p>X2: {(result.doubleChance["X2"] * 100).toFixed(1)}%</p>

      {result.oddsProbs && (
        <>
          <h3>Bookmaker Implied Probabilities</h3>
          <p>1: {(result.oddsProbs["1"] * 100).toFixed(1)}%</p>
          <p>X: {(result.oddsProbs["X"] * 100).toFixed(1)}%</p>
          <p>2: {(result.oddsProbs["2"] * 100).toFixed(1)}%</p>
        </>
      )}
    </div>
  )}
</div>

); }
