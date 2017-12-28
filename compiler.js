const fs = require('fs');
const readline = require('readline');

var header = "import { open, fill, click, find} from './library';\n";

process.argv.forEach((val, index) => {
    console.log(`${index}: ${val}`);
});

source = process.argv[2];
console.log(source);
sourcef = source.split(".wal")[0];

fs.writeFileSync(sourcef + '.jsp', header);
fs.readFile(source, function (err, data) {
    if (err) throw err;
    fs.appendFileSync(sourcef + '.jsp', data);
});
var exec = require('child_process').exec, child;
exec('sjs '+ sourcef + '.jsp' +' -o '+ sourcef +'.jsc',
    function (error, stdout, stderr) {
        if (error != null) {
            console.log('exec error: ' + error);
        }
        const rl = readline.createInterface({
            input: require('fs').createReadStream(source + '.jsc'),
        });
        var header2 = "(async function() {\nconst phantom = require('phantom');\nconst instance = await phantom.create();\nconst page = await instance.createPage();\n";
        
        fs.writeFileSync(sourcef + '.js', header2, function (err) {
            if (err) throw err;
        });
        rl.on('line', function (line) {
            line = line.replace("await__", "await ");
            let strarr =  String.prototype.trim(line.split("=",2)[0]).split(" ")
            if(line.split("=",2).length == 2 && strarr.length == 1 && line.split("=")[0].split('.').length == 1 && line.split("=")[0].split(',').length == 1){
                fs.appendFileSync('tsweet_o.js', 'var ' + line + '\n', function (err) {
                if (err) throw err;
            });
            }else{
                fs.appendFileSync('tsweet_o.js', line + '\n', function (err) {
                    if (err) throw err;
                });
            }
        });

        var footer2 = "})();";
        rl.on('close', function(){
            fs.appendFileSync(sourcef + '.js', footer2, function (err) {
                if (err) throw err;
            });
        })
        fs.unlinkSync('./'+source+'.jsc');
        fs.unlinkSync('./'+source+'.jsp');
    }
);