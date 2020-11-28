const mongoose = require('mongoose');

mongoose.connect('mongodb://mongo:27017/dbHack', { useNewUrlParser: true });
mongoose.set('useCreateIndex', true);

const db = mongoose.connection;

db.on('error', console.error.bind(console, 'MongoDB connection error:'));
