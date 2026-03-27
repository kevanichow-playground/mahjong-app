const express = require('express');
const Database = require('better-sqlite3');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// DB setup
const db = new Database(path.join(__dirname, 'mahjong.db'));
db.pragma('journal_mode = WAL');

db.exec(`
  CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    notes TEXT DEFAULT ''
  );
  CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    player TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
  );
`);

// ── SEED DATA ──
const SEED = [
  {date:'2025-07-26',r:{Yin:-12.4,Ceci:-25.2,Sa:18.1,Crystal:3.8,Kevani:15.7}},
  {date:'2025-07-29',r:{Yin:-3.3,Ceci:43.0,Sa:-19.5,Crystal:-8.1,Kevani:-12.1}},
  {date:'2025-07-31',r:{Yin:53.6,Ceci:-50.0,Sa:11.6,Crystal:-15.2}},
  {date:'2025-08-05',r:{Yin:-14.6,Kevani:-5.6,Jacky:-12.5,Ruby:11.7,Cousin:21.0}},
  {date:'2025-08-06',r:{Yin:24.6,Ceci:-14.8,Sa:2.8,Crystal:-21.0,Kevani:8.4}},
  {date:'2025-08-09',r:{Yin:-12.3,Ceci:42.1,Sa:-10.0,Crystal:-19.8}},
  {date:'2025-08-16',r:{Yin:-12.0,Ceci:26.4,Sa:-22.8,Crystal:16.8,Kevani:-8.4}},
  {date:'2025-08-17',r:{Yin:8.8,Ceci:-4.6,Sa:4.2,Crystal:-8.3}},
  {date:'2025-08-24',r:{Yin:29.7,Ceci:7.6,Sa:-20.3,Crystal:-21.1,Jacky:-10.1,Ruby:14.2}},
  {date:'2025-09-07',r:{Yin:-7.0,Ceci:-15.2,Kevani:8.8,Jacky:-3.2,Ruby:16.6}},
  {date:'2025-09-08',r:{Yin:7.1,Ceci:-2.6,Sa:19.6,Crystal:-12.0,Kevani:-12.0}},
  {date:'2025-09-14',r:{Yin:1.6,Ceci:0.7,Sa:0.9,Crystal:13.5,Kevani:-10.9,Jacky:-6.7,Ruby:-11.7,Tung:12.6}},
  {date:'2025-09-16',r:{Yin:15.8,Ceci:-20.9,Sa:-0.1,Crystal:5.2}},
  {date:'2025-09-21',r:{Yin:13.5,Ceci:-2.7,Sa:-15.2,Crystal:11.8,Kevani:-7.4}},
  {date:'2025-09-26',r:{Yin:-28.1,Ceci:39.6,Sa:10.2,Crystal:-21.8}},
  {date:'2025-09-27',r:{Yin:12.9,Ceci:-0.6,Sa:-10.8,Crystal:-1.4}},
  {date:'2025-09-30',r:{Yin:21.9,Ceci:11.3,Sa:4.2,Crystal:-24.1,Kevani:6.1,Jacky:2.8,Ruby:-22.3}},
  {date:'2025-10-19',r:{Yin:7.9,Ceci:-1.6,Sa:27.3,Kevani:-12.4,Jacky:-18.7,Ruby:19.3,'Auntie J':-17.3,Leo:-4.6}},
  {date:'2025-10-24',r:{Yin:-15.7,Ceci:-9.7,Sa:28.9,'Auntie J':4.5,Leo:-8.0}},
  {date:'2025-10-31',r:{Yin:5.3,Ceci:-23.6,Sa:25.7,Crystal:-0.6,'Auntie J':11.3,Leo:-18.1}},
  {date:'2025-11-09',r:{Yin:10.6,Jacky:9.7,Ruby:0.0,Tung:-5.6,'Auntie J':-0.4,"Tung's Sis":-0.8,Sum:-13.3}},
  {date:'2025-11-11',r:{Yin:-26.5,Ceci:7.8,Kevani:4.1,'Auntie J':15.1,Leo:-0.6}},
  {date:'2025-11-23',r:{Yin:2.2,Sa:6.4,Crystal:4.2,Kevani:-24.1,'Auntie J':8.1,Leo:3.2}},
  {date:'2025-11-28',r:{Ceci:-27.8,Sa:0.6,Crystal:37.6,'Auntie J':7.0,Leo:-17.4}},
  {date:'2025-11-29',r:{Yin:12.4,Sa:-14.1,Crystal:33.4,Jacky:-24.9,Ruby:-1.5,Tung:-2.7,"Tung's Sis":-2.6}},
  {date:'2025-12-06',r:{Yin:-20.4,Ceci:15.8,Crystal:-15.5,'Auntie J':27.9,Leo:-7.8}},
  {date:'2025-12-11',r:{Yin:-23.3,Ceci:3.5,Crystal:32.7,Kevani:-23.9,'Auntie J':17.9,Leo:-6.8}},
  {date:'2025-12-24',r:{Yin:16.1,Ceci:45.0,Cousin:-26.3,'Auntie J':-10.5,Leo:-6.7,'東':-21.8}},
  {date:'2025-12-25',r:{Yin:5.5,Ceci:-6.1,Crystal:-0.3,'Auntie J':1.2,Leo:-0.4}},
  {date:'2025-12-27',r:{Yin:21.9,Ceci:-16.5,Crystal:17.0,'Auntie J':-11.3,Leo:-11.1}},
  {date:'2025-12-29',r:{Yin:-22.6,Ceci:3.4,Sa:-5.3,Crystal:59.8,'Auntie J':5.7,Leo:-41.0}},
  {date:'2026-01-01',r:{Yin:12.4,Ceci:0.8,Jacky:6.7,Ruby:3.6,Tung:2.1,Alex:-25.5}},
  {date:'2026-01-08',r:{Yin:-0.6,Ceci:-1.2,Sa:-16.0,Crystal:17.8}},
  {date:'2026-01-11',r:{Yin:21.6,Ceci:-35.5,Sa:-11.1,Crystal:24.9}},
  {date:'2026-01-15',r:{Yin:18.5,Ceci:-2.0,Sa:8.7,Crystal:-25.2}},
  {date:'2026-01-20',r:{Yin:4.8,Ceci:54.2,Sa:-40.3,Crystal:12.2,Kevani:-30.9}},
  {date:'2026-01-28',r:{Yin:-13.2,Ceci:34.4,Sa:-10.5,Crystal:-0.1,Kevani:-10.8}},
  {date:'2026-02-23',r:{Yin:16.0,Sa:-18.9,Crystal:14.5,Kevani:-11.7}},
  {date:'2026-02-27',r:{Yin:-5.9,Sa:5.6,Crystal:26.6,Kevani:-0.2,Jacky:-17.1,Ruby:-9.1}},
  {date:'2026-03-09',r:{Yin:8.0,Ceci:23.9,Cousin:43.2,'東':-80.7,Joyce:4.8}},
  {date:'2026-03-10',r:{Yin:30.8,Ceci:2.8,Sa:-6.5,Crystal:-35.9,Joyce:8.8}},
  {date:'2026-03-15',r:{Yin:14.4,Ceci:-17.9,Jacky:6.4,Ruby:6.2,Cousin:-2.3,'東':1.4,Joyce:-8.4}},
  {date:'2026-03-20',r:{Yin:-1.1,Ceci:-19.7,Sa:32.9,Crystal:-29.1,Kevani:16.0}},
  {date:'2026-03-22',r:{Yin:8.7,Ceci:-4.9,Crystal:-19.3,Kevani:-27.4,Cousin:32.5,'東':10.4}}
];

function seedDb() {
  const count = db.prepare('SELECT COUNT(*) as c FROM sessions').get();
  if (count.c > 0) return;
  console.log('Seeding database...');
  const ins = db.prepare('INSERT OR IGNORE INTO sessions (date) VALUES (?)');
  const insr = db.prepare('INSERT INTO results (session_id, player, amount) VALUES (?, ?, ?)');
  const tx = db.transaction(() => {
    for (const s of SEED) {
      const { lastInsertRowid: sid } = ins.run(s.date);
      for (const [player, amount] of Object.entries(s.r)) {
        insr.run(sid, player, amount);
      }
    }
  });
  tx();
  console.log(`Seeded ${SEED.length} sessions.`);
}
seedDb();

// ── MIDDLEWARE ──
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ── API ROUTES ──

// GET all data (sessions + results)
app.get('/api/data', (req, res) => {
  const sessions = db.prepare(`
    SELECT s.id, s.date, s.notes,
           json_group_object(r.player, r.amount) as results
    FROM sessions s
    LEFT JOIN results r ON r.session_id = s.id
    GROUP BY s.id
    ORDER BY s.date ASC
  `).all();

  const parsed = sessions.map(s => ({
    id: s.id,
    date: s.date,
    notes: s.notes,
    results: JSON.parse(s.results || '{}')
  }));

  // Compute player stats
  const playerMap = {};
  for (const s of parsed) {
    const dow = new Date(s.date).toLocaleDateString('en-US', { weekday: 'long' });
    for (const [player, amount] of Object.entries(s.results)) {
      if (!playerMap[player]) playerMap[player] = { name: player, sessions: [] };
      playerMap[player].sessions.push({ date: s.date, dow, amount });
    }
  }

  const players = Object.values(playerMap).map(p => {
    const amounts = p.sessions.map(s => s.amount);
    const total = amounts.reduce((a, b) => a + b, 0);
    const wins = amounts.filter(a => a > 0).length;
    const losses = amounts.filter(a => a < 0).length;
    const plays = amounts.length;
    const winrate = plays > 0 ? (wins / plays) * 100 : 0;
    const topwin = Math.max(...amounts);
    const toploss = Math.min(...amounts);
    const avgPerPlay = plays > 0 ? total / plays : 0;

    // DOW stats
    const dowStats = {};
    for (const d of ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']) {
      const ds = p.sessions.filter(s => s.dow === d);
      if (ds.length > 0) {
        const davg = ds.reduce((a, s) => a + s.amount, 0) / ds.length;
        const dwins = ds.filter(s => s.amount > 0).length;
        dowStats[d] = { avg: Math.round(davg * 10) / 10, winrate: Math.round((dwins / ds.length) * 1000) / 10, sessions: ds.length };
      } else {
        dowStats[d] = { avg: 0, winrate: 0, sessions: 0 };
      }
    }

    // Trend (sorted by date)
    const sorted = [...p.sessions].sort((a, b) => a.date.localeCompare(b.date));
    let cum = 0;
    const trend = sorted.map(s => {
      cum += s.amount;
      return { date: s.date, amount: s.amount, cumulative: Math.round(cum * 10) / 10 };
    });

    // Moving averages (3-session, 5-session)
    const ma3 = trend.map((_, i) => {
      if (i < 2) return null;
      return Math.round((trend[i].amount + trend[i-1].amount + trend[i-2].amount) / 3 * 10) / 10;
    });
    const ma5 = trend.map((_, i) => {
      if (i < 4) return null;
      return Math.round((trend[i].amount + trend[i-1].amount + trend[i-2].amount + trend[i-3].amount + trend[i-4].amount) / 5 * 10) / 10;
    });

    // Momentum: slope of last 5 sessions
    const last5 = trend.slice(-5);
    let momentum = 0;
    if (last5.length >= 3) {
      const n = last5.length;
      const sumX = n * (n - 1) / 2;
      const sumX2 = last5.reduce((a, _, i) => a + i * i, 0);
      const sumY = last5.reduce((a, s) => a + s.amount, 0);
      const sumXY = last5.reduce((a, s, i) => a + i * s.amount, 0);
      momentum = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    }

    // Best day
    const bestDay = Object.entries(dowStats)
      .filter(([, v]) => v.sessions > 0)
      .sort(([, a], [, b]) => b.avg - a.avg)[0]?.[0] || '-';

    return {
      name: p.name,
      total: Math.round(total * 10) / 10,
      wins, losses, plays,
      winrate: Math.round(winrate * 10) / 10,
      topwin: Math.round(topwin * 10) / 10,
      toploss: Math.round(toploss * 10) / 10,
      avgPerPlay: Math.round(avgPerPlay * 10) / 10,
      dowStats,
      bestDay,
      trend,
      ma3,
      ma5,
      momentum: Math.round(momentum * 100) / 100,
      recentForm: trend.slice(-5).map(s => s.amount),
      stdDev: (() => {
        const mean = total / (plays || 1);
        const variance = amounts.reduce((a, x) => a + Math.pow(x - mean, 2), 0) / (plays || 1);
        return Math.round(Math.sqrt(variance) * 10) / 10;
      })()
    };
  }).sort((a, b) => b.total - a.total);

  // Assign ranks
  players.forEach((p, i) => { p.rank = i + 1; });

  res.json({ sessions: parsed, players });
});

// POST new session
app.post('/api/sessions', (req, res) => {
  const { date, results, notes } = req.body;
  if (!date || !results || Object.keys(results).length === 0) {
    return res.status(400).json({ error: 'Missing date or results' });
  }
  try {
    const ins = db.prepare('INSERT OR REPLACE INTO sessions (date, notes) VALUES (?, ?)');
    const delOld = db.prepare('DELETE FROM results WHERE session_id = (SELECT id FROM sessions WHERE date = ?)');
    const insr = db.prepare('INSERT INTO results (session_id, player, amount) VALUES (?, ?, ?)');
    const tx = db.transaction(() => {
      delOld.run(date);
      const { lastInsertRowid: sid } = ins.run(date, notes || '');
      for (const [player, amount] of Object.entries(results)) {
        if (amount !== '' && amount !== null && !isNaN(amount)) {
          insr.run(sid, player, parseFloat(amount));
        }
      }
    });
    tx();
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE a session
app.delete('/api/sessions/:id', (req, res) => {
  db.prepare('DELETE FROM results WHERE session_id = ?').run(req.params.id);
  db.prepare('DELETE FROM sessions WHERE id = ?').run(req.params.id);
  res.json({ success: true });
});

// GET odds for a set of players + day
app.get('/api/odds', (req, res) => {
  const { players: pStr, day } = req.query;
  if (!pStr) return res.status(400).json({ error: 'Missing players' });

  const playerNames = pStr.split(',').map(s => s.trim()).filter(Boolean);

  // Fetch all results
  const allResults = db.prepare(`
    SELECT r.player, r.amount, s.date
    FROM results r JOIN sessions s ON s.id = r.session_id
    ORDER BY s.date
  `).all();

  const calcOdds = (name) => {
    const pr = allResults.filter(r => r.player === name);
    if (pr.length === 0) return { name, score: 0, winProb: 0.25, odds: 4.0 };

    const total = pr.length;
    const wins = pr.filter(r => r.amount > 0).length;
    const baseWR = wins / total;

    // Recent form (last 5)
    const last5 = pr.slice(-5);
    const recentWins = last5.filter(r => r.amount > 0).length;
    const recentWR = last5.length > 0 ? recentWins / last5.length : baseWR;

    // DOW adjustment
    let dowWR = baseWR;
    if (day) {
      const dowGames = pr.filter(r => new Date(r.date).toLocaleDateString('en-US', { weekday: 'long' }) === day);
      if (dowGames.length >= 2) {
        dowWR = dowGames.filter(r => r.amount > 0).length / dowGames.length;
      }
    }

    // Weighted: 40% base, 35% recent, 25% dow
    const weightedWR = baseWR * 0.4 + recentWR * 0.35 + dowWR * 0.25;

    // Average gain
    const avgGain = pr.reduce((a, r) => a + r.amount, 0) / total;

    // Score: combination of winrate and avg gain
    const score = weightedWR * 70 + Math.min(Math.max(avgGain / 50, -1), 1) * 30;

    return { name, total, wins, baseWR, recentWR, dowWR, weightedWR, score, avgGain };
  };

  const scores = playerNames.map(calcOdds);
  const totalScore = scores.reduce((a, s) => a + Math.max(s.score, 1), 0);

  const odds = scores.map(s => {
    const prob = Math.max(s.score, 1) / totalScore;
    const decimalOdds = Math.round((1 / prob) * 100) / 100;
    return {
      name: s.name,
      winProb: Math.round(prob * 1000) / 10,
      odds: decimalOdds,
      baseWR: Math.round((s.baseWR || 0) * 1000) / 10,
      recentWR: Math.round((s.recentWR || 0) * 1000) / 10,
      dowWR: Math.round((s.dowWR || 0) * 1000) / 10,
      momentum: s.avgGain > 0 ? '🔥上升' : '❄️下滑',
      avgGain: Math.round((s.avgGain || 0) * 10) / 10,
    };
  }).sort((a, b) => a.odds - b.odds);

  res.json({ odds, day });
});

// SPA fallback
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => console.log(`🀄 Mahjong app running on port ${PORT}`));
