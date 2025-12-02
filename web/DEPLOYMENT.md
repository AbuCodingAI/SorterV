# Deploying Sorter Web to Vercel/Netlify/Surge

## File Structure

```
web/
├── index.html          # Main download page
├── downloads/          # Folder for exe files
│   ├── Sorter.exe
│   ├── Sorter.exe.part1
│   ├── Sorter.exe.part2
│   └── construct.bat
├── package.json        # For Vercel
├── vercel.json         # Vercel config
├── netlify.toml        # Netlify config
└── DEPLOYMENT.md       # This file
```

## Step 1: Add Download Files

Create a `downloads` folder and add:
- `Sorter.exe` (or split files)
- `Sorter.exe.part1`
- `Sorter.exe.part2`
- `construct.bat`

```bash
mkdir web/downloads
cp Sorter/dist/Sorter.exe.part1 web/downloads/
cp Sorter/dist/Sorter.exe.part2 web/downloads/
cp Sorter/dist/construct.bat web/downloads/
```

## Option 1: Deploy to Vercel

### Via CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd web
vercel
```

### Via GitHub

1. Push to GitHub
2. Go to vercel.com
3. Import your repository
4. Select `web` folder as root
5. Deploy

**Result:** `https://your-project.vercel.app`

## Option 2: Deploy to Netlify

### Via CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd web
netlify deploy --prod
```

### Via GitHub

1. Push to GitHub
2. Go to netlify.com
3. Connect your repository
4. Set build command: `echo 'Static site'`
5. Set publish directory: `web`
6. Deploy

**Result:** `https://your-project.netlify.app`

## Option 3: Deploy to Surge

### Via CLI

```bash
# Install Surge
npm install -g surge

# Deploy
cd web
surge
```

**Result:** `https://your-project.surge.sh`

## Hosting Large Files

### Option A: Host on Same Platform

If your platform supports large files (Netlify: 300 MB, Surge: 200 MB):

1. Add files to `downloads/` folder
2. Deploy normally
3. Files accessible at `https://your-domain.com/downloads/Sorter.exe`

### Option B: Host on GitHub Releases

If files are too large:

1. Upload to GitHub Releases
2. Update download links in `index.html`:

```html
<a href="https://github.com/your-repo/releases/download/v1.0.0/Sorter.exe.part1" 
   class="btn btn-primary" download>⬇️ Download Part 1</a>
```

3. Deploy web page to Vercel/Netlify/Surge

### Option C: Use CDN

For maximum speed:

1. Upload files to AWS S3 or Cloudflare R2
2. Update links in `index.html`
3. Deploy web page

## File Size Limits

| Platform | Limit | Notes |
|---|---|---|
| Vercel | 50 MB | Use GitHub Releases for exe |
| Netlify | 300 MB | Can host exe directly |
| Surge | 200 MB | Can host exe directly |

## Recommended Setup

**Best for Sorter:**

1. **Web Page:** Deploy to Vercel/Netlify/Surge
2. **Exe Files:** Host on GitHub Releases
3. **Links:** Point from web page to GitHub

This gives you:
- ✓ Professional download page
- ✓ Unlimited file hosting
- ✓ No bandwidth costs
- ✓ Fast CDN delivery

## Example: Complete Setup

```bash
# 1. Create web folder
mkdir web
cd web

# 2. Copy files
cp ../index.html .
mkdir downloads
cp ../Sorter/dist/Sorter.exe.part1 downloads/
cp ../Sorter/dist/Sorter.exe.part2 downloads/
cp ../Sorter/dist/construct.bat downloads/

# 3. Deploy to Vercel
vercel

# 4. Share link
# https://sorter.vercel.app
```

## Updating Downloads

To update the exe files:

1. Rebuild Sorter.exe
2. Split into parts
3. Update `downloads/` folder
4. Redeploy

```bash
# Rebuild
cd Sorter
python build.py

# Split
# (use PowerShell script)

# Update web
cp dist/Sorter.exe.part1 ../web/downloads/
cp dist/Sorter.exe.part2 ../web/downloads/
cp dist/construct.bat ../web/downloads/

# Redeploy
cd ../web
vercel --prod
```

## Troubleshooting

### Files not downloading
- Check file paths in `index.html`
- Ensure `downloads/` folder exists
- Verify file permissions

### Page not loading
- Check `vercel.json` or `netlify.toml`
- Ensure `index.html` is in root
- Check browser console for errors

### Large file uploads fail
- Use GitHub Releases instead
- Update links in `index.html`
- Test locally first

## Local Testing

```bash
# Test locally
cd web
python -m http.server 8000

# Visit http://localhost:8000
```

---

**Happy deploying!** 🚀
