const express = require('express');
const { exec } = require('child_process');
const path = require('path');

const app = express();

// Serve static files from the "DT" directory
app.use(express.static(path.join(__dirname, 'DT')));

app.get('/show_graph', (req, res) => {
    exec('python graph.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing graph.py: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`graph.py script encountered an error: ${stderr}`);
            return;
        }
        console.log(`graph.py script executed successfully: ${stdout}`);
    });
    res.redirect('http://127.0.0.1:5000/');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
