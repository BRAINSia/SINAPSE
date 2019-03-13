// server.js

const csvFilePath = __dirname + "/available_putamen_test.csv"
const outputFilePath = __dirname + "/identified_putamen_test.csv"
console.log(csvFilePath);
console.log(outputFilePath);
var photo_directory = '/Shared/johnsonhj/2018Projects/'


var express = require('express');
var app = express();
var fs = require("fs");

var bodyParser = require('body-parser');
var multer  = require('multer');

var http = require("http");
app.use(express.static(photo_directory));
	
var file_index = 0;

app.set('view engine', 'ejs');

let ejs = require('ejs');

var good_file_names = [];
var bad_file_names = [];
var good_and_bad_file_names = [];
var image_index = 0;
//const csvFilePath = "/Shared/johnsonhj/2018Projects/20181112_RecodeLabelMaps/src/Identify_Putamen/available_putamen.csv"
//const outputFilePath = "/Shared/johnsonhj/2018Projects/20181112_RecodeLabelMaps/src/Identify_Putamen/identified_putamen.csv"

app.get('/Identify_Putamen.html', function(req, res){
	const csv = require('csvtojson')
	var file_names = [];
	csv().fromFile(csvFilePath).then((jsonObj)=>{
		current_full_file_path = ""
		image_index = jsonObj[Object.keys(jsonObj).length-1].file_path;
		console.log(current_full_file_path);
		max_image_index = Object.keys(jsonObj).length-1;
		current_full_file_path = "";
		/*if (typeof jsonObj[image_index] === 'undefined')
		{
				template_vars = {title: 		"Identify Good Putamen",
				photo_index:		parseInt(image_index),
				max_photo_index:	max_image_index
				
				}
				ejs.renderFile(__dirname + '/' + "Identify_Putamen.ejs", template_vars,  function(err, data){
					res.send(data);
				})
		}
		else
		{*/
			if (image_index <= max_image_index)
			{
				current_full_file_path = jsonObj[image_index].file_path;
			}
			console.log(current_full_file_path);
			console.log("image index: " + image_index);
			var current_photo_index = 0;
			
			if (typeof req.query['index'] !== 'undefined')
			{
					image_index = parseInt(req.query['index']);
					current_full_file_path = jsonObj[image_index].file_path;
			}
			if(typeof req.query['back'] !== 'undefined')
			{
				good_and_bad_file_names.pop();
				current_full_file_path = jsonObj[image_index].file_path;
				template_vars = {title: 		"Identify Good Putamen",
				file_path: 		current_full_file_path.replace(photo_directory, ""),
				photo_index:		parseInt(image_index),
				max_photo_index:	max_image_index,
				full_file_path:	current_full_file_path}
				ejs.renderFile(__dirname + '/' + "Identify_Putamen.ejs", template_vars,  function(err, data){
					res.send(data);
				})
			}
			else{
				if(req.query['good_or_bad'] == 'good')
				{
					good_file_names[good_file_names.length] = req.query['current_file_name'];
					good_and_bad_file_names[good_and_bad_file_names.length] = [req.query['current_file_name'], 'good'];
					console.log("\nGood and Bad: \n" + JSON.stringify(good_and_bad_file_names) +  "\n\n");	
				}
				if(req.query['good_or_bad'] == 'bad')
				{
					bad_file_names[bad_file_names.length] = req.query['current_file_name']; 
					good_and_bad_file_names[good_and_bad_file_names.length] = [req.query['current_file_name'], 'bad'];
					console.log("\nGood and Bad: \n" + JSON.stringify(good_and_bad_file_names) +  "\n\n");	
				}
				template_vars = {title: 		"Identify Good Putamen",
					 file_path: 		current_full_file_path.replace(photo_directory, ""),
					 photo_index:		parseInt(image_index),
					 full_file_path:	current_full_file_path,
					 max_photo_index: 	max_image_index	
				}
				ejs.renderFile(__dirname + '/' + "Identify_Putamen.ejs", template_vars,  function(err, data){
					res.send(data);
				})	
			}
	//	}
		
	})
});


app.post('/write_csv', function(req, res){
	console.log("Writing file");
	/*var date = new Date();
	var write_stream_good = fs.createWriteStream("good_files.txt", {'flags': 'a'});
	write_stream_good.on('error', function(err){});
	good_file_names.forEach(function(v) {
		write_stream_good.write(v + '\n');
	});
	write_stream_good.end();
	var write_stream_bad = fs.createWriteStream("bad_files.txt", {'flags': 'a'});
	write_stream_bad.on('error', function(err){});
	bad_file_names.forEach(function(v) {
		write_stream_bad.write(v + '\n');
	});
	write_stream_bad.end();*/
	
	//if 
	
	
	var previous_saved_photo_index = 0;
	fs.readFile(csvFilePath, 'utf8', function(err, data){
		let csv_data_by_line = data.split('\n');
		
		test = csv_data_by_line.pop();
		
		previous_saved_photo_index = csv_data_by_line.pop();
		csv_data_by_line[csv_data_by_line.length] = image_index;
		var write_stream = fs.createWriteStream(csvFilePath);
		write_stream.on('error', function(err){});
		csv_data_by_line.forEach(function(v) {write_stream.write(v + '\n');});
		write_stream.end();
	})
	
	fs.readFile(outputFilePath, 'utf8', function(err, data){
		if(typeof data !== 'undefined')
		{
			let identified_putamen_by_line = data.split('\n');
		}
		else
		{
			identified_putamen_by_line = [];
		}
		console.log("Lines in identified_putamen_by_line: " + identified_putamen_by_line.length);
		console.log("good_and_bad_file_names: " + good_and_bad_file_names.length);
		console.log("image_index: " + image_index);
		/*if ((idenfified_putamen_by_line.length - good_and_bad_file_names.length) < image_index)
		{*/

		// If the back button was pressed too many times, remove lines from the identified_putamen.csv file
		if (image_index+1 < identified_putamen_by_line.length)
		{
			var lines_to_remove = identified_putamen_by_line.length - (image_index+1);
			// Remove lines from identified_putamen_by_line
			identified_putamen_by_line.pop();
			for (var i=0; i<lines_to_remove; i++)
			{
				popped = identified_putamen_by_line.pop();
				console.log("popped: " + popped);
			}
			var write_stream_identified_putamen = fs.createWriteStream(outputFilePath);
			write_stream_identified_putamen.on('error', function(err){});
			identified_putamen_by_line.forEach(function(v) {
				write_stream_identified_putamen.write(v + '\n');
			});
			write_stream_identified_putamen.end();
		}
		else{
			var write_stream_identified_putamen = fs.createWriteStream(outputFilePath, {'flags': 'a'});
			write_stream_identified_putamen.on('error', function(err){});
			good_and_bad_file_names.forEach(function(v) {
				write_stream_identified_putamen.write(v + '\n');
			});
			write_stream_identified_putamen.end();
		}
		good_and_bad_file_names = [];
	})

	/*good_file_names.forEach(function(v) {
		good_file_names = [];	
	});
	bad_file_names.forEach(function(v) {
		bad_file_names = [];
	});*/
	//good_and_bad_file_names = [];
	res.redirect("/Identify_Putamen.html");
	res.end();
});

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   
   console.log("Example app listening at http://127.0.0.1:8081/Identify_Putamen.html")
});

