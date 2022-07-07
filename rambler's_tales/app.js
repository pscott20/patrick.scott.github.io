//require modules
const express = require('express');
const morgan = require('morgan');
const methodOverride = require('method-override');
const mongoose = require('mongoose');
const session = require('express-session');
const MongoStore = require('connect-mongo');
const flash = require('connect-flash');
const config = require('config');

const dbConfig = config.get('Database.dbConfig.dbName');
const port = config.get('Database.dbConfig.port');
const host = config.get('Database.dbConfig.host');

const storyRoutes = require('./routes/storyRoutes');
const userRoutes = require('./routes/userRoutes');


//create app
const app = express();
app.set('view engine', 'ejs');

//configure app
//let port = 3000;
//let host = 'localhost';
//app.set('view engine', 'ejs');

//configure app
//let port = 5984;
//let host = 'localhost';

//connect to database
/*mongoose.connect('mongodb://localhost:27017/demos', 
                {useNewUrlParser: true, useUnifiedTopology: true, useCreateIndex: true })*/
//mongoose.connect('mongodb+srv://db_admin:password_admin@cluster0.ptzkd.mongodb.net/?retryWrites=true&w=majority', 
  //              {useNewUrlParser: true, useUnifiedTopology: true, useCreateIndex: true })

mongoose.connect(dbConfig, {
    useNewUrlParser: true, 
    useUnifiedTopology: true, 
    useCreateIndex: true 
})
    .then(()=>{
        //start app
        app.listen(port, host, ()=>{
            console.log('Database Connected' + '\nServer is running on port', port);
    });
})
    .catch(err=>console.log('Database Not Connected' + err.message));

//mount middlware
app.use(
    session({
        secret: "ajfeirf90aeu9eroejfoefj",
        resave: false,
        saveUninitialized: false,
        //store: new MongoStore({mongoUrl: 'mongodb://localhost:27017/demos'}),
        store: new MongoStore({mongoUrl: 'mongodb+srv://db_admin:password_admin@cluster0.ptzkd.mongodb.net/?retryWrites=true&w=majority'}),
        cookie: {maxAge: 60*60*1000}
        })
);
app.use(flash());

app.use((req, res, next) => {
    //console.log(req.session);
    res.locals.user = req.session.user||null;
    res.locals.errorMessages = req.flash('error');
    res.locals.successMessages = req.flash('success');
    next();
});

app.use(express.static('public'));
app.use(express.urlencoded({extended: true}));
app.use(morgan('tiny'));
app.use(methodOverride('_method'));

//set up routes
app.get('/', (req, res)=>{
    res.render('index');
});

app.use('/stories', storyRoutes);

app.use('/users', userRoutes);

app.use((req, res, next) => {
    let err = new Error('The server cannot locate ' + req.url);
    err.status = 404;
    next(err);

});

app.use((err, req, res, next)=>{
    console.log(err.stack);
    if(!err.status) {
        err.status = 500;
        err.message = ("Internal Server Error");
    }

    res.status(err.status);
    res.render('error', {error: err});
});
