# Deploying to Vercel

This FastAPI application can be deployed to Vercel as a serverless function.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed (optional, for CLI deployment)
3. Your repository pushed to GitHub, GitLab, or Bitbucket (for automatic deployments)

## Environment Variables

Before deploying, make sure to set these environment variables in Vercel:

1. **GROQ_API_KEY** - Your Groq API key for AI weather advice
2. **EMAIL_USER** - Your email address for sending emails
3. **EMAIL_PASS** - Your email app password (not your regular password)

### Setting Environment Variables in Vercel:

1. Go to your project settings in Vercel dashboard
2. Navigate to "Environment Variables"
3. Add each variable for Production, Preview, and Development environments

## Deployment Methods

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. Push your code to GitHub/GitLab/Bitbucket
2. Go to https://vercel.com/new
3. Import your repository
4. Vercel will automatically detect the `vercel.json` configuration
5. Add your environment variables
6. Click "Deploy"

### Method 2: Deploy via Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

4. For production deployment:
   ```bash
   vercel --prod
   ```

## Project Structure

```
weather-notifier/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── main.py               # FastAPI application
├── weather_agent.py      # Weather data fetching and AI advice
├── email_service.py      # Email sending functionality
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── .vercelignore        # Files to ignore during deployment
```

## API Endpoints

Once deployed, your API will be available at:
- `https://your-project.vercel.app/`
- `https://your-project.vercel.app/weather`
- `https://your-project.vercel.app/weather/advice`
- `https://your-project.vercel.app/send-email`

## Testing the Deployment

After deployment, test your endpoints:

```bash
# Test root endpoint
curl https://your-project.vercel.app/

# Test weather endpoint
curl -X POST https://your-project.vercel.app/weather \
  -H "Content-Type: application/json" \
  -d '{"latitude": 27.7172, "longitude": 85.3240}'

# Test weather advice endpoint
curl -X POST https://your-project.vercel.app/weather/advice \
  -H "Content-Type: application/json" \
  -d '{"latitude": 27.7172, "longitude": 85.3240, "location": "Kathmandu"}'
```

## Important Notes

1. **Cold Starts**: Serverless functions may have cold start delays (usually 1-2 seconds on first request)
2. **Timeout**: Vercel serverless functions have a maximum execution time (10 seconds on Hobby plan, 60 seconds on Pro)
3. **Email Service**: Make sure your email provider allows serverless function access (Gmail requires app-specific passwords)
4. **Environment Variables**: Never commit `.env` files - use Vercel's environment variables instead

## Troubleshooting

### Import Errors
If you encounter import errors, make sure:
- All dependencies are in `requirements.txt`
- `PYTHONPATH` is set to "." in `vercel.json`
- Files are in the correct directory structure

### Environment Variables Not Working
- Verify variables are set in Vercel dashboard
- Redeploy after adding new environment variables
- Check variable names match exactly (case-sensitive)

### Email Sending Fails
- Verify EMAIL_USER and EMAIL_PASS are set correctly
- For Gmail, use an app-specific password, not your regular password
- Check if your email provider blocks serverless function IPs

## Support

For more information, visit:
- Vercel Python Documentation: https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Mangum Documentation: https://mangum.io/

