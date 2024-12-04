// code to extract text from image using OCR
// run `node server_text_api.js` to start the server
const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');
const { createWorker } = require('tesseract.js');

const app = express();
app.use(cors());
app.use(express.json());



app.post('/ocr', async (req, res) => {
  const { imageUrl } = req.body;
  console.log(`Received request for URL: ${imageUrl}`);
  try {
    const response = await fetch(imageUrl);
    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    const worker = await createWorker('eng', 1, {
        logger: m => console.log(m), // Add logger here
      });
    await worker.load();
    await worker.loadLanguage('eng');
    await worker.initialize('eng');
    const result = await worker.recognize(buffer);
    await worker.terminate();

    res.json({ text: result.data.text });
  } catch (error) {
    console.error('OCR error:', error);
    res.status(500).json({ error: 'Failed to process image', details: error.toString() });
  }
});

const PORT = process.env.PORT || 5003;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
