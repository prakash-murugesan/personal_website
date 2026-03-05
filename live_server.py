#!/usr/bin/env python3
"""
Live reload development server for static sites.
Automatically refreshes browser when files change.
"""

import http.server
import socketserver
import os
import time
import threading
from pathlib import Path

PORT = 8000
DIRECTORY = "."

class LiveReloadHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with live reload injection"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add headers to prevent caching
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        """Inject live reload script into HTML files"""
        if self.path == '/' or self.path.endswith('.html'):
            # Serve the HTML with injected live reload script
            file_path = self.path
            if file_path == '/':
                file_path = '/index.html'

            try:
                full_path = os.path.join(DIRECTORY, file_path.lstrip('/'))
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Inject live reload script before </body>
                reload_script = """
<script>
(function() {
    let lastModified = null;

    function checkForChanges() {
        fetch(window.location.href, { method: 'HEAD' })
            .then(response => {
                const modified = response.headers.get('Last-Modified');
                if (lastModified && modified && lastModified !== modified) {
                    console.log('Changes detected, reloading...');
                    window.location.reload();
                }
                lastModified = modified;
            })
            .catch(err => console.error('Live reload check failed:', err));
    }

    // Check for changes every second
    setInterval(checkForChanges, 1000);
    console.log('Live reload enabled');
})();
</script>
"""
                content = content.replace('</body>', reload_script + '</body>')

                # Send the modified content
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-Length', str(len(content.encode('utf-8'))))
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                return

            except FileNotFoundError:
                self.send_error(404, "File not found")
                return

        # For non-HTML files, serve normally
        super().do_GET()

def watch_files():
    """Monitor files for changes and print updates"""
    watched_extensions = {'.html', '.css', '.js'}
    last_modified = {}

    print(f"👀 Watching for file changes in {os.path.abspath(DIRECTORY)}")

    while True:
        for path in Path(DIRECTORY).rglob('*'):
            if path.suffix in watched_extensions:
                try:
                    mtime = path.stat().st_mtime
                    if path in last_modified and last_modified[path] != mtime:
                        print(f"📝 Changed: {path}")
                    last_modified[path] = mtime
                except:
                    pass
        time.sleep(1)

def main():
    """Start the live reload server"""
    print(f"🚀 Starting live reload server at http://localhost:{PORT}")
    print("📁 Serving files from:", os.path.abspath(DIRECTORY))
    print("✨ Live reload is enabled - changes will auto-refresh the browser")
    print("Press Ctrl+C to stop\n")

    # Start file watcher in a separate thread
    watcher = threading.Thread(target=watch_files, daemon=True)
    watcher.start()

    # Start the HTTP server
    with socketserver.TCPServer(("", PORT), LiveReloadHandler) as httpd:
        # Don't auto-open browser due to permission issues
        print(f"\n👉 Open http://localhost:{PORT} in your browser\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
            return

if __name__ == "__main__":
    main()