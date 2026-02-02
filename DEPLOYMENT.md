# Deployment Guide - kacpercvch.pl

This guide will help you deploy your temperature monitoring dashboard to your domain **kacpercvch.pl**.

## 🚀 Deployment Options

### Option 1: Deploy to Vercel (Recommended)

Vercel offers free hosting for Next.js apps with automatic SSL and easy custom domain setup.

#### Step 1: Deploy to Vercel

1. **Push your code to GitHub** (if not already done):
```bash
git add -A
git commit -m "Ready for deployment"
git push
```

2. **Go to [vercel.com](https://vercel.com)** and sign in with GitHub

3. **Import your repository:**
   - Click "Add New Project"
   - Select your repository
   - Click "Deploy"

4. **Wait for deployment** (usually takes 1-2 minutes)

#### Step 2: Connect Your Custom Domain

1. **In Vercel Dashboard:**
   - Go to your project
   - Click "Settings" → "Domains"
   - Add domain: `kacpercvch.pl`
   - Also add: `www.kacpercvch.pl`

2. **In seohost.pl DNS settings:**

Add these DNS records:

| Type  | Name | Value                          | TTL  |
|-------|------|--------------------------------|------|
| A     | @    | 76.76.21.21                    | 3600 |
| CNAME | www  | cname.vercel-dns.com           | 3600 |

**Note:** Vercel will show you the exact DNS records to add. Use those values.

3. **Wait for DNS propagation** (can take up to 48 hours, usually 1-2 hours)

4. **Verify:** Visit `https://kacpercvch.pl` - your dashboard should be live!

---

### Option 2: Deploy to Railway

Railway is another great option with simple deployment.

#### Step 1: Deploy to Railway

1. **Go to [railway.app](https://railway.app)** and sign in with GitHub

2. **Create new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure build:**
   - Railway auto-detects Next.js
   - No configuration needed

4. **Get your Railway URL** (e.g., `your-app.up.railway.app`)

#### Step 2: Connect Custom Domain

1. **In Railway Dashboard:**
   - Go to your project
   - Click "Settings" → "Domains"
   - Click "Custom Domain"
   - Enter: `kacpercvch.pl`

2. **In seohost.pl DNS settings:**

Add these DNS records:

| Type  | Name | Value                          | TTL  |
|-------|------|--------------------------------|------|
| CNAME | @    | your-app.up.railway.app        | 3600 |
| CNAME | www  | your-app.up.railway.app        | 3600 |

**Note:** Railway will show you the exact DNS records. Some hosts don't allow CNAME on root (@), in which case use A record if provided.

---

### Option 3: Deploy to Your seohost.pl Server

If seohost.pl provides Node.js hosting, you can deploy directly there.

#### Requirements Check

Contact seohost.pl support to verify:
- Node.js 20+ support
- Ability to run custom Node.js applications
- SSH access or deployment method

#### Deployment Steps

1. **Build your app:**
```bash
bun build
```

2. **Upload files to server:**
   - Upload entire project folder via FTP/SFTP
   - Or use SSH and git clone

3. **On the server, install dependencies:**
```bash
cd /path/to/your/app
npm install
```

4. **Start the app:**
```bash
npm run start
```

5. **Configure domain:**
   - Point `kacpercvch.pl` to your server's IP
   - Set up reverse proxy (Nginx/Apache) to port 3000

---

## 📝 Configure Raspberry Pi

Once deployed, update your Raspberry Pi script:

### Edit raspberry-pi-sensor.py

```bash
nano raspberry-pi-sensor.py
```

Change line 14 to:
```python
SERVER_URL = "https://kacpercvch.pl/api/temperature"
```

Save and restart the script:
```bash
sudo python3 raspberry-pi-sensor.py
```

---

## 🔒 SSL Certificate

All deployment options provide automatic HTTPS:
- **Vercel:** Automatic SSL (Let's Encrypt)
- **Railway:** Automatic SSL
- **seohost.pl:** Check if they provide SSL, or use Cloudflare (free SSL)

### Using Cloudflare (Optional)

If you want extra features (CDN, DDoS protection, analytics):

1. **Sign up at [cloudflare.com](https://cloudflare.com)**
2. **Add your domain:** `kacpercvch.pl`
3. **Update nameservers at seohost.pl** to Cloudflare's nameservers
4. **Enable SSL:** Full (strict) mode
5. **Point DNS to your deployment:**
   - Add A or CNAME record to your Vercel/Railway deployment

---

## ✅ Verification

After deployment, test your setup:

1. **Visit your domain:**
```
https://kacpercvch.pl
```

2. **Test API endpoint:**
```bash
curl https://kacpercvch.pl/api/temperature
```

Should return:
```json
{"readings":[]}
```

3. **Start Raspberry Pi script** and watch data appear on dashboard

---

## 🔧 Troubleshooting

### Domain not working
- Check DNS propagation: [whatsmydns.net](https://whatsmydns.net)
- Verify DNS records are correct
- Wait up to 48 hours for full propagation

### SSL certificate error
- Ensure you're using `https://` not `http://`
- Check SSL settings in your hosting provider
- Try Cloudflare for automatic SSL

### Raspberry Pi can't connect
- Verify the URL is correct (with `https://`)
- Check if OpenVPN is connected
- Test with curl: `curl https://kacpercvch.pl/api/temperature`

### 404 error on API
- Ensure deployment includes all files
- Check build logs for errors
- Verify API route exists: `src/app/api/temperature/route.ts`

---

## 📊 Recommended Setup

**Best setup for your use case:**

1. ✅ Deploy to **Vercel** (free, fast, reliable)
2. ✅ Connect domain **kacpercvch.pl** via Vercel
3. ✅ Configure Raspberry Pi to use `https://kacpercvch.pl/api/temperature`
4. ✅ Optional: Add Cloudflare for extra features

This gives you:
- Free hosting
- Automatic SSL
- Global CDN
- Automatic deployments on git push
- Works perfectly with OpenVPN

---

## 🎉 Next Steps

1. Choose your deployment method (Vercel recommended)
2. Deploy your app
3. Configure DNS at seohost.pl
4. Update Raspberry Pi script with your domain
5. Start monitoring temperatures at `https://kacpercvch.pl`
