# AI Meeting Summarizer Frontend

A modern, professional frontend for the AI Meeting Summarizer application that converts MP3 meeting recordings into professional minutes of meeting using Whisper and DeepSeek AI.

## Features

- **Modern UI/UX**: Clean, professional design with smooth animations
- **Drag & Drop Upload**: Easy file upload with drag and drop support
- **Real-time Processing**: Visual feedback during transcription and summarization
- **Copy & Download**: Easy sharing and saving of generated minutes
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Toast Notifications**: Non-intrusive success and error notifications

## File Structure

```
frontend/
├── index.html          # Main HTML file
├── styles.css          # CSS styles and animations
├── script.js           # JavaScript functionality
└── README.md          # This file
```

## Setup Instructions

1. **Start the Backend Server**
   ```bash
   cd "Ai meeting summarize"
   python mainapp.py
   ```
   The Flask server will start on `http://localhost:5000`

2. **Serve the Frontend**
   You can serve the frontend using any of these methods:

   **Option A: Python HTTP Server**
   ```bash
   cd "Ai meeting summarize/frontend"
   python -m http.server 8000
   ```
   Then open `http://localhost:8000` in your browser

   **Option B: Node.js HTTP Server**
   ```bash
   cd "Ai meeting summarize/frontend"
   npx http-server -p 8000
   ```

   **Option C: Live Server (VS Code Extension)**
   - Install the "Live Server" extension in VS Code
   - Right-click on `index.html` and select "Open with Live Server"

3. **Access the Application**
   Open your browser and navigate to the frontend URL (e.g., `http://localhost:8000`)

## Usage

1. **Upload Audio File**
   - Click the upload area or drag and drop an MP3 file
   - File must be in MP3 format and under 100MB

2. **Process Recording**
   - Click "Generate Minutes of Meeting" button
   - Wait for the processing to complete (transcription + AI summarization)

3. **View Results**
   - Review the generated meeting minutes
   - Copy to clipboard or download as text file
   - Start a new meeting if needed

## API Configuration

The frontend is configured to connect to the Flask backend at `http://localhost:5000`. If your backend is running on a different port or host, update the `API_BASE_URL` variable in `script.js`:

```javascript
const API_BASE_URL = 'http://your-backend-host:port';
```

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Features Breakdown

### Upload Section
- Drag and drop file upload
- File validation (MP3 only, max 100MB)
- File information display
- Remove file option

### Processing Section
- Visual loading spinner
- Step-by-step progress indicators
- Real-time status updates

### Results Section
- Formatted meeting minutes display
- Copy to clipboard functionality
- Download as text file
- Start new meeting option

### Error Handling
- Network error handling
- File validation errors
- Server error messages
- Retry functionality

## Customization

### Styling
- Modify `styles.css` to change colors, fonts, or layout
- The design uses CSS Grid and Flexbox for responsive layout
- Color scheme can be easily changed by updating CSS custom properties

### Functionality
- Extend `script.js` to add new features
- API endpoints can be modified in the configuration section
- Toast notifications can be customized for different message types

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure the Flask backend has CORS enabled
   - Add `flask-cors` to your backend if needed

2. **File Upload Fails**
   - Check file format (must be MP3)
   - Verify file size (must be under 100MB)
   - Ensure backend server is running

3. **Processing Stuck**
   - Check browser console for errors
   - Verify backend API is responding
   - Check network connectivity

### Development Tips

- Use browser developer tools to debug issues
- Check the Network tab for API request/response details
- Console logs are available for debugging
- Backend logs will show processing status

## License

This frontend is part of the AI Meeting Summarizer project.
