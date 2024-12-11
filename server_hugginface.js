//Code to interact with model
// run `node server_hugginface.js` to start the server
const express = require('express');
const { HfInference } = require('@huggingface/inference');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());  
require('dotenv').config();

console.log(process.env.HUGGINGFACE_API_KEY);
const client = new HfInference(process.env.HUGGINGFACE_API_KEY,);

app.post('/query', async (req, res) => {
    try {
        const inputs = req.body.content;
        console.log(inputs);
        const chatCompletion = await client.chatCompletion({
            model: "meta-llama/Llama-3.1-8B-Instruct",
            messages: [
                {
                    role: "user",
                    content: inputs  
                }
            ],
            max_tokens: 500
        });

        res.json({ message: chatCompletion.choices[0].message });
    } catch (error) {
        console.error('Error with Hugging Face API:', error);
        res.status(500).json({ error: 'Error processing your request' });
    }
});

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => {
    console.log(`Server is running on http://10.27.19.122:${PORT}`);
});
