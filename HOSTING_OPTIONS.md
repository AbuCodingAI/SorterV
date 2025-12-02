# Sorter - Hosting & Distribution Options

## File Size Problem

Sorter.exe is **35.49 MB**, which exceeds limits on some platforms:
- GitHub: 100 MB limit (OK, but large for releases)
- npm: 100 MB limit (not applicable for desktop apps)
- PyPI: 100 MB limit (not applicable for exe)

## Hosting Comparison

| Platform | File Limit | Bandwidth | Best For | Notes |
|---|---|---|---|---|
| **GitHub Releases** | 2 GB | Unlimited | Primary distribution | Recommended - free, reliable |
| **Vercel** | 50 MB | 100 GB/month | Web hosting only | ❌ Can't host exe directly |
| **Surge** | 200 MB | Unlimited | Static files | ❌ Can't host exe directly |
| **Netlify** | 300 MB | Unlimited | Static files | ❌ Can't host exe directly |
| **AWS S3** | Unlimited | Pay per GB | Large files | ✓ Works, costs money |
| **Google Drive** | 5 TB | Unlimited | Personal sharing | ✓ Works, slower downloads |
| **Dropbox** | 2 GB free | Unlimited | Personal sharing | ✓ Works, slower downloads |

## Recommended Solutions

### Option 1: GitHub Releases (Best)
**Pros:**
- Free, unlimited bandwidth
- Direct download links
- Version management
- No file size issues

**How:**
1. Create a GitHub release
2. Upload `Sorter.exe.part1` and `Sorter.exe.part2`
3. Upload `construct.bat`
4. Users download all three and run construct.bat

**Download URL:**
```
https://github.com/your-repo/Sorter/releases/download/v1.0.0/Sorter.exe.part1
https://github.com/your-repo/Sorter/releases/download/v1.0.0/Sorter.exe.part2
https://github.com/your-repo/Sorter/releases/download/v1.0.0/construct.bat
```

### Option 2: Vercel/Surge/Netlify + Download Page
**Pros:**
- Fast CDN delivery
- Professional hosting
- Easy to set up

**How:**
1. Create a simple HTML download page
2. Host on Vercel/Surge/Netlify
3. Link to GitHub releases or external storage for exe files

**Example:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Sorter - Download</title>
</head>
<body>
    <h1>Download Sorter</h1>
    <p>Download both parts and run construct.bat</p>
    <a href="https://github.com/your-repo/releases/download/v1.0.0/Sorter.exe.part1">
        Download Part 1 (17.74 MB)
    </a>
    <a href="https://github.com/your-repo/releases/download/v1.0.0/Sorter.exe.part2">
        Download Part 2 (17.74 MB)
    </a>
    <a href="https://github.com/your-repo/releases/download/v1.0.0/construct.bat">
        Download construct.bat
    </a>
</body>
</html>
```

Deploy to Vercel:
```bash
vercel deploy
```

### Option 3: AWS S3 (For Scale)
**Pros:**
- Unlimited file size
- Scalable bandwidth
- CloudFront CDN

**Cons:**
- Costs money (~$0.023 per GB downloaded)

**How:**
1. Upload exe to S3
2. Enable CloudFront CDN
3. Share download link

### Option 4: Direct GitHub Release (Simplest)
Just upload the full `Sorter.exe` to GitHub releases:
- GitHub allows up to 2 GB per file
- 35 MB is well within limits
- Users download directly

**Pros:**
- Simplest for users
- No construct.bat needed
- Direct download

**Cons:**
- Larger file size in repo

## Verdict

**For Sorter, use GitHub Releases:**
1. Upload split files + construct.bat (saves bandwidth)
2. Or upload full exe (simplest for users)
3. Create a download page on Vercel/Surge pointing to GitHub

**Why?**
- Free
- Reliable
- No bandwidth limits
- Professional
- Easy for users

## Example Setup

```
GitHub Releases (v1.0.0)
├── Sorter.exe.part1 (17.74 MB)
├── Sorter.exe.part2 (17.74 MB)
├── construct.bat
└── README.md

Vercel/Surge (Download Page)
└── index.html (links to GitHub releases)
```

Users visit your Vercel page → click download → GitHub releases → get files

This gives you the best of both worlds:
- Professional download page (Vercel/Surge)
- Reliable file hosting (GitHub)
- No bandwidth costs
- Fast CDN delivery
