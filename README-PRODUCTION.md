# Stable Diffusion WebUI - Production Backend

This repository has been configured for production deployment on Render as a backend service for the [uwear-virtual-shop](https://github.com/AlphaZee01/uwear-virtual-shop.git) frontend.

## 🚀 Quick Deploy on Render

1. **Fork this repository** to your GitHub account
2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Create a new Web Service
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration

3. **Environment Variables** (optional - already configured in render.yaml):
   - `PORT`: 10000 (default)
   - `GRADIO_SERVER_NAME`: 0.0.0.0
   - `API_ONLY`: true
   - `ENABLE_CORS`: true
   - `ALLOW_ORIGINS`: https://uwear-virtual-shop.onrender.com,http://localhost:3000,http://localhost:5173

## 📋 API Endpoints

Once deployed, your API will be available at:
- **Base URL**: `https://your-service-name.onrender.com`
- **API Documentation**: `https://your-service-name.onrender.com/docs`
- **Health Check**: `https://your-service-name.onrender.com/docs`

### Key Endpoints for uwear-virtual-shop:

- `POST /sdapi/v1/txt2img` - Text-to-image generation
- `POST /sdapi/v1/img2img` - Image-to-image generation
- `GET /sdapi/v1/samplers` - Available samplers
- `GET /sdapi/v1/models` - Available models
- `POST /sdapi/v1/options` - Update settings

## 🔧 Configuration

### CORS Configuration
The API is configured to accept requests from:
- `https://uwear-virtual-shop.onrender.com` (production)
- `http://localhost:3000` (development)
- `http://localhost:5173` (Vite development)

### Model Management
- Models should be uploaded to the `/models` directory
- Supported formats: `.safetensors`, `.ckpt`, `.pt`
- Models are automatically detected on startup

## 🐳 Docker Deployment

If you prefer Docker deployment:

```bash
# Build the image
docker build -t stable-diffusion-webui-backend .

# Run the container
docker run -p 10000:10000 stable-diffusion-webui-backend
```

## 🔍 Health Monitoring

The service includes health checks:
- Automatic health monitoring via `/docs` endpoint
- 30-second intervals with 3 retries
- Automatic restart on failure

## 📊 Performance Considerations

- **Memory**: Requires at least 4GB RAM for basic models
- **Storage**: Models can be several GB each
- **CPU**: Multi-core recommended for faster generation
- **GPU**: Not available on Render free tier, but CPU fallback works

## 🔒 Security

- CORS is configured for specific origins only
- API endpoints are protected
- No authentication by default (add if needed)

## 🛠️ Development

For local development:

```bash
# Install dependencies
pip install -r requirements-production.txt

# Run the API
python main.py
```

## 📝 Integration with uwear-virtual-shop

In your frontend application, make API calls to:

```javascript
const API_BASE = 'https://your-service-name.onrender.com';

// Example: Generate an image
const response = await fetch(`${API_BASE}/sdapi/v1/txt2img`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: "a beautiful dress",
    negative_prompt: "ugly, blurry",
    steps: 20,
    cfg_scale: 7,
    width: 512,
    height: 512
  })
});

const result = await response.json();
```

## 🆘 Troubleshooting

1. **Service not starting**: Check Render logs for Python errors
2. **CORS errors**: Verify `ALLOW_ORIGINS` includes your frontend URL
3. **Memory issues**: Upgrade to a higher tier plan
4. **Model loading**: Ensure models are in the correct format and location

## 📞 Support

For issues specific to this production setup, please check:
1. Render deployment logs
2. Application logs in the Render dashboard
3. The original [Stable Diffusion WebUI documentation](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
