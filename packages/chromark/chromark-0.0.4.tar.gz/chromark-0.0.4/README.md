# chromark

Use as CLI

```sh
chromark /path/to/bookmark.html --folders --url --datetime --title --netloc
```

Use as pakcage

```python
import chromark

for entry in chromark.read('/path/to/bookmark.html'):
    # ...
```