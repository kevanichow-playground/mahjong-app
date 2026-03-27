import os
import json
import sqlite3
import math
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory, abort

app = Flask(__name__, static_folder='public', static_url_path='')
DB_PATH = os.path.join(os.path.dirname(__file__), 'mahjong.db')

SEED = [
  {"date":"2025-07-26","r":{"Yin":-12.4,"Ceci":-25.2,"Sa":18.1,"Crystal":3.8,"Kevani":15.7}},
  {"date":"2025-07-29","r":{"Yin":-3.3,"Ceci":43.0,"Sa":-19.5,"Crystal":-8.1,"Kevani":-12.1}},
  {"date":"2025-07-31","r":{"Yin":53.6,"Ceci":-50.0,"Sa":11.6,"Crystal":-15.2}},
  {"date":"2025-08-05","r":{"Yin":-14.6,"Kevani":-5.6,"Jacky":-12.5,"Ruby":11.7,"Cousin":21.0}},
  {"date":"2025-08-06","r":{"Yin":24.6,"Ceci":-14.8,"Sa":2.8,"Crystal":-21.0,"Kevani":8.4}},
  {"date":"2025-08-09","r":{"Yin":-12.3,"Ceci":42.1,"Sa":-10.0,"Crystal":-19.8}},
  {"date":"2025-08-16","r":{"Yin":-12.0,"Ceci":26.4,"Sa":-22.8,"Crystal":16.8,"Kevani":-8.4}},
  {"date":"2025-08-17","r":{"Yin":8.8,"Ceci":-4.6,"Sa":4.2,"Crystal":-8.3}},
  {"date":"2025-08-24","r":{"Yin":29.7,"Ceci":7.6,"Sa":-20.3,"Crystal":-21.1,"Jacky":-10.1,"Ruby":14.2}},
  {"date":"2025-09-07","r":{"Yin":-7.0,"Ceci":-15.2,"Kevani":8.8,"Jacky":-3.2,"Ruby":16.6}},
  {"date":"2025-09-08","r":{"Yin":7.1,"Ceci":-2.6,"Sa":19.6,"Crystal":-12.0,"Kevani":-12.0}},
  {"date":"2025-09-14","r":{"Yin":1.6,"Ceci":0.7,"Sa":0.9,"Crystal":13.5,"Kevani":-10.9,"Jacky":-6.7,"Ruby":-11.7,"Tung":12.6}},
  {"date":"2025-09-16","r":{"Yin":15.8,"Ceci":-20.9,"Sa":-0.1,"Crystal":5.2}},
  {"date":"2025-09-21","r":{"Yin":13.5,"Ceci":-2.7,"Sa":-15.2,"Crystal":11.8,"Kevani":-7.4}},
  {"date":"2025-09-26","r":{"Yin":-28.1,"Ceci":39.6,"Sa":10.2,"Crystal":-21.8}},
  {"date":"2025-09-27","r":{"Yin":12.9,"Ceci":-0.6,"Sa":-10.8,"Crystal":-1.4}},
  {"date":"2025-09-30","r":{"Yin":21.9,"Ceci":11.3,"Sa":4.2,"Crystal":-24.1,"Kevani":6.1,"Jacky":2.8,"Ruby":-22.3}},
  {"date":"2025-10-19","r":{"Yin":7.9,"Ceci":-1.6,"Sa":27.3,"Kevani":-12.4,"Jacky":-18.7,"Ruby":19.3,"Auntie J":-17.3,"Leo":-4.6}},
  {"date":"2025-10-24","r":{"Yin":-15.7,"Ceci":-9.7,"Sa":28.9,"Auntie J":4.5,"Leo":-8.0}},
  {"date":"2025-10-31","r":{"Yin":5.3,"Ceci":-23.6,"Sa":25.7,"Crystal":-0.6,"Auntie J":11.3,"Leo":-18.1}},
  {"date":"2025-11-09","r":{"Yin":10.6,"Jacky":9.7,"Ruby":0.0,"Tung":-5.6,"Auntie J":-0.4,"Tung's Sis":-0.8,"Sum":-13.3}},
  {"date":"2025-11-11","r":{"Yin":-26.5,"Ceci":7.8,"Kevani":4.1,"Auntie J":15.1,"Leo":-0.6}},
  {"date":"2025-11-23","r":{"Yin":2.2,"Sa":6.4,"Crystal":4.2,"Kevani":-24.1,"Auntie J":8.1,"Leo":3.2}},
  {"date":"2025-11-28","r":{"Ceci":-27.8,"Sa":0.6,"Crystal":37.6,"Auntie J":7.0,"Leo":-17.4}},
  {"date":"2025-11-29","r":{"Yin":12.4,"Sa":-14.1,"Crystal":33.4,"Jacky":-24.9,"Ruby":-1.5,"Tung":-2.7,"Tung's Sis":-2.6}},
  {"date":"2025-12-06","r":{"Yin":-20.4,"Ceci":15.8,"Crystal":-15.5,"Auntie J":27.9,"Leo":-7.8}},
  {"date":"2025-12-11","r":{"Yin":-23.3,"Ceci":3.5,"Crystal":32.7,"Kevani":-23.9,"Auntie J":17.9,"Leo":-6.8}},
  {"date":"2025-12-24","r":{"Yin":16.1,"Ceci":45.0,"Cousin":-26.3,"Auntie J":-10.5,"Leo":-6.7,"\u6771":-21.8}},
  {"date":"2025-12-25","r":{"Yin":5.5,"Ceci":-6.1,"Crystal":-0.3,"Auntie J":1.2,"Leo":-0.4}},
  {"date":"2025-12-27","r":{"Yin":21.9,"Ceci":-16.5,"Crystal":17.0,"Auntie J":-11.3,"Leo":-11.1}},
  {"date":"2025-12-29","r":{"Yin":-22.6,"Ceci":3.4,"Sa":-5.3,"Crystal":59.8,"Auntie J":5.7,"Leo":-41.0}},
  {"date":"2026-01-01","r":{"Yin":12.4,"Ceci":0.8,"Jacky":6.7,"Ruby":3.6,"Tung":2.1,"Alex":-25.5}},
  {"date":"2026-01-08","r":{"Yin":-0.6,"Ceci":-1.2,"Sa":-16.0,"Crystal":17.8}},
  {"date":"2026-01-11","r":{"Yin":21.6,"Ceci":-35.5,"Sa":-11.1,"Crystal":24.9}},
  {"date":"2026-01-15","r":{"Yin":18.5,"Ceci":-2.0,"Sa":8.7,"Crystal":-25.2}},
  {"date":"2026-01-20","r":{"Yin":4.8,"Ceci":54.2,"Sa":-40.3,"Crystal":12.2,"Kevani":-30.9}},
  {"date":"2026-01-28","r":{"Yin":-13.2,"Ceci":34.4,"Sa":-10.5,"Crystal":-0.1,"Kevani":-10.8}},
  {"date":"2026-02-23","r":{"Yin":16.0,"Sa":-18.9,"Crystal":14.5,"Kevani":-11.7}},
  {"date":"2026-02-27","r":{"Yin":-5.9,"Sa":5.6,"Crystal":26.6,"Kevani":-0.2,"Jacky":-17.1,"Ruby":-9.1}},
  {"date":"2026-03-09","r":{"Yin":8.0,"Ceci":23.9,"Cousin":43.2,"\u6771":-80.7,"Joyce":4.8}},
  {"date":"2026-03-10","r":{"Yin":30.8,"Ceci":2.8,"Sa":-6.5,"Crystal":-35.9,"Joyce":8.8}},
  {"date":"2026-03-15","r":{"Yin":14.4,"Ceci":-17.9,"Jacky":6.4,"Ruby":6.2,"Cousin":-2.3,"\u6771":1.4,"Joyce":-8.4}},
  {"date":"2026-03-20","r":{"Yin":-1.1,"Ceci":-19.7,"Sa":32.9,"Crystal":-29.1,"Kevani":16.0}},
  {"date":"2026-03-22","r":{"Yin":8.7,"Ceci":-4.9,"Crystal":-19.3,"Kevani":-27.4,"Cousin":32.5,"\u6771":10.4}}
]

DOW_NAMES = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
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
    """)
    # Seed
    count = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    if count == 0:
        print("Seeding database...")
        for s in SEED:
            cur = conn.execute("INSERT OR IGNORE INTO sessions (date) VALUES (?)", (s['date'],))
            sid = cur.lastrowid
            if sid:
                for player, amount in s['r'].items():
                    conn.execute("INSERT INTO results (session_id, player, amount) VALUES (?,?,?)", (sid, player, amount))
        conn.commit()
        print(f"Seeded {len(SEED)} sessions.")
    conn.close()

def compute_stats(sessions_raw, results_raw):
    # Build player map
    player_map = {}
    result_by_session = {}
    for r in results_raw:
        sid = r['session_id']
        if sid not in result_by_session:
            result_by_session[sid] = {}
        result_by_session[sid][r['player']] = r['amount']

    sessions = []
    for s in sessions_raw:
        sid = s['id']
        date = s['date']
        results = result_by_session.get(sid, {})
        try:
            dow = datetime.strptime(date[:10], '%Y-%m-%d').strftime('%A')
        except:
            dow = 'Monday'
        sessions.append({'id': sid, 'date': date, 'notes': s['notes'] or '', 'results': results})
        for player, amount in results.items():
            if player not in player_map:
                player_map[player] = []
            player_map[player].append({'date': date, 'dow': dow, 'amount': amount})

    players = []
    for name, plays_list in player_map.items():
        amounts = [p['amount'] for p in plays_list]
        total = round(sum(amounts), 1)
        wins = sum(1 for a in amounts if a > 0)
        losses = sum(1 for a in amounts if a < 0)
        plays = len(amounts)
        winrate = round((wins / plays * 100), 1) if plays else 0
        topwin = round(max(amounts), 1)
        toploss = round(min(amounts), 1)
        avg_per_play = round(total / plays, 1) if plays else 0

        # DOW stats
        dow_stats = {}
        for d in DOW_NAMES:
            ds = [p for p in plays_list if p['dow'] == d]
            if ds:
                davg = sum(p['amount'] for p in ds) / len(ds)
                dwins = sum(1 for p in ds if p['amount'] > 0)
                dow_stats[d] = {'avg': round(davg, 1), 'winrate': round(dwins / len(ds) * 100, 1), 'sessions': len(ds)}
            else:
                dow_stats[d] = {'avg': 0, 'winrate': 0, 'sessions': 0}

        # Best day
        active_days = [(d, v) for d, v in dow_stats.items() if v['sessions'] > 0]
        best_day = max(active_days, key=lambda x: x[1]['avg'])[0] if active_days else '-'

        # Trend (sorted by date)
        sorted_plays = sorted(plays_list, key=lambda p: p['date'])
        cum = 0
        trend = []
        for p in sorted_plays:
            cum += p['amount']
            trend.append({'date': p['date'], 'amount': p['amount'], 'cumulative': round(cum, 1)})

        # MA3, MA5
        amts = [t['amount'] for t in trend]
        ma3 = [None if i < 2 else round(sum(amts[i-2:i+1])/3, 1) for i in range(len(amts))]
        ma5 = [None if i < 4 else round(sum(amts[i-4:i+1])/5, 1) for i in range(len(amts))]

        # Momentum (slope of last 5)
        last5 = amts[-5:]
        momentum = 0
        if len(last5) >= 3:
            n = len(last5)
            xs = list(range(n))
            sx = sum(xs); sy = sum(last5)
            sxy = sum(x*y for x,y in zip(xs,last5)); sx2 = sum(x*x for x in xs)
            denom = n*sx2 - sx*sx
            if denom != 0:
                momentum = round((n*sxy - sx*sy) / denom, 2)

        # Std dev
        mean = total / plays if plays else 0
        variance = sum((a - mean)**2 for a in amounts) / plays if plays else 0
        std_dev = round(math.sqrt(variance), 1)

        players.append({
            'name': name, 'total': total, 'wins': wins, 'losses': losses,
            'plays': plays, 'winrate': winrate, 'topwin': topwin, 'toploss': toploss,
            'avgPerPlay': avg_per_play, 'dowStats': dow_stats, 'bestDay': best_day,
            'trend': trend, 'ma3': ma3, 'ma5': ma5,
            'momentum': momentum, 'recentForm': amts[-5:], 'stdDev': std_dev
        })

    # Sort by total desc, assign rank
    players.sort(key=lambda p: p['total'], reverse=True)
    for i, p in enumerate(players):
        p['rank'] = i + 1

    return sessions, players

@app.route('/api/data')
def get_data():
    conn = get_db()
    sessions_raw = conn.execute("SELECT * FROM sessions ORDER BY date ASC").fetchall()
    results_raw = conn.execute("SELECT * FROM results").fetchall()
    conn.close()
    sessions, players = compute_stats(sessions_raw, results_raw)
    return jsonify({'sessions': sessions, 'players': players})

@app.route('/api/sessions', methods=['POST'])
def add_session():
    data = request.json
    date = data.get('date', '').strip()
    results = data.get('results', {})
    notes = data.get('notes', '')
    if not date or not results:
        return jsonify({'error': 'Missing date or results'}), 400
    try:
        conn = get_db()
        conn.execute("PRAGMA foreign_keys = ON")
        # Delete old if exists
        old = conn.execute("SELECT id FROM sessions WHERE date=?", (date,)).fetchone()
        if old:
            conn.execute("DELETE FROM results WHERE session_id=?", (old['id'],))
            conn.execute("DELETE FROM sessions WHERE id=?", (old['id'],))
        cur = conn.execute("INSERT INTO sessions (date, notes) VALUES (?,?)", (date, notes))
        sid = cur.lastrowid
        for player, amount in results.items():
            if amount is not None and str(amount).strip() != '':
                conn.execute("INSERT INTO results (session_id, player, amount) VALUES (?,?,?)", (sid, player, float(amount)))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<int:sid>', methods=['DELETE'])
def delete_session(sid):
    conn = get_db()
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("DELETE FROM results WHERE session_id=?", (sid,))
    conn.execute("DELETE FROM sessions WHERE id=?", (sid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/odds')
def get_odds():
    players_str = request.args.get('players', '')
    day = request.args.get('day', '')
    player_names = [p.strip() for p in players_str.split(',') if p.strip()]
    if not player_names:
        return jsonify({'error': 'Missing players'}), 400

    conn = get_db()
    all_results = conn.execute("""
        SELECT r.player, r.amount, s.date
        FROM results r JOIN sessions s ON s.id = r.session_id
        ORDER BY s.date
    """).fetchall()
    conn.close()

    def calc(name):
        pr = [r for r in all_results if r['player'] == name]
        if not pr:
            return {'name': name, 'score': 5, 'avgGain': 0, 'baseWR': 25, 'recentWR': 25, 'dowWR': 25}
        total = len(pr)
        wins = sum(1 for r in pr if r['amount'] > 0)
        base_wr = wins / total
        last5 = pr[-5:]
        recent_wr = sum(1 for r in last5 if r['amount'] > 0) / len(last5) if last5 else base_wr
        dow_wr = base_wr
        if day:
            dow_games = [r for r in pr if datetime.strptime(r['date'][:10], '%Y-%m-%d').strftime('%A') == day]
            if len(dow_games) >= 2:
                dow_wr = sum(1 for r in dow_games if r['amount'] > 0) / len(dow_games)
        weighted = base_wr * 0.4 + recent_wr * 0.35 + dow_wr * 0.25
        avg_gain = sum(r['amount'] for r in pr) / total
        score = weighted * 70 + min(max(avg_gain / 50, -1), 1) * 30
        return {
            'name': name, 'score': max(score, 1),
            'baseWR': round(base_wr * 100, 1),
            'recentWR': round(recent_wr * 100, 1),
            'dowWR': round(dow_wr * 100, 1),
            'avgGain': round(avg_gain, 1),
            'momentum': '🔥上升' if avg_gain > 0 else '❄️下滑'
        }

    scores = [calc(n) for n in player_names]
    total_score = sum(s['score'] for s in scores)
    odds = []
    for s in scores:
        prob = s['score'] / total_score
        odds.append({
            'name': s['name'],
            'winProb': round(prob * 100, 1),
            'odds': round(1 / prob, 2),
            'baseWR': s['baseWR'], 'recentWR': s['recentWR'], 'dowWR': s['dowWR'],
            'avgGain': s['avgGain'], 'momentum': s['momentum']
        })
    odds.sort(key=lambda x: x['odds'])
    return jsonify({'odds': odds, 'day': day})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 3000))
    print(f"🀄 Mahjong app running on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
