import sys
import os
import json

# Add project root to Python path
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))
os.chdir(os.path.join(ROOT, '..'))

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from http.server import HTTPServer, BaseHTTPRequestHandler

print("=== RAG Web Demo Server ===")
print("Loading modules...")

from ingest import build_knowledge_base
from src.embeddings import LocalEmbedder
from src.chunking import RecursiveChunker, FixedSizeChunker, SentenceChunker

DATA_DIR = os.path.join(ROOT, '..', 'data', 'ussh_library')

print("Loading embedding model (first time may take ~10s)...")
embedding_fn = LocalEmbedder()

print("Building 3 knowledge bases (recursive / fixed / sentence)...")
STORES = {
    'recursive': build_knowledge_base(DATA_DIR, embedding_fn, RecursiveChunker(chunk_size=400)),
    'fixed':     build_knowledge_base(DATA_DIR, embedding_fn, FixedSizeChunker(400, overlap=50)),
    'sentence':  build_knowledge_base(DATA_DIR, embedding_fn, SentenceChunker(max_sentences_per_chunk=3)),
}
print(f"  - recursive: {STORES['recursive'].get_collection_size()} chunks")
print(f"  - fixed    : {STORES['fixed'].get_collection_size()} chunks")
print(f"  - sentence : {STORES['sentence'].get_collection_size()} chunks")
print("\nServer ready! Open: http://localhost:5500\n")


class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self._serve_file('index.html', 'text/html; charset=utf-8')
        elif self.path == '/api/status':
            self._json({'status': 'ok', 'chunks': {k: v.get_collection_size() for k, v in STORES.items()}})
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/search':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(length).decode('utf-8'))
                query    = body.get('query', '').strip()
                strategy = body.get('strategy', 'recursive')
                filter_d = body.get('filter', None) or None

                if not query:
                    self._json({'error': 'query is empty'}, 400)
                    return

                store = STORES.get(strategy, STORES['recursive'])
                if filter_d:
                    results = store.search_with_filter(query, filter_dict=filter_d, top_k=3)
                else:
                    results = store.search(query, top_k=3)

                out = []
                for i, r in enumerate(results):
                    out.append({
                        'rank':     i + 1,
                        'score':    round(float(r['score']), 4),
                        'content':  r['content'],
                        'id_chunk': r.get('id', ''),
                        'metadata': {k: v for k, v in r['metadata'].items()},
                    })
                self._json(out)
            except Exception as e:
                self._json({'error': str(e)}, 500)
        else:
            self.send_response(404)
            self.end_headers()

    # ── helpers ──
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, filename, content_type):
        path = os.path.join(ROOT, filename)
        with open(path, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(data))
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"[{args[1]}] {self.path}")


if __name__ == '__main__':
    PORT = 5500
    server = HTTPServer(('localhost', PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
