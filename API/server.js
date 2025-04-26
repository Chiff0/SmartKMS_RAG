
const express = require('express');

const serverless = require('serverless-http');


const app = express();


app.use(express.json());


app.post('/query', (req, res) => {

  const query = req.body.query || 'No query provided';

  res.json({ query });
});


const port = 3000;

if (require.main === module) {
  app.listen(port, () => {
    console.log(`Server listening locally on port ${port}`);
  });
}



module.exports.handler = serverless(app);
