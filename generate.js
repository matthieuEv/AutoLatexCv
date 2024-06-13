const fs = require('fs');
const latex = require('node-latex');
const nunjucks = require('nunjucks');
const https = require('https');

function generatePDF(data, lang){
    if (!fs.existsSync('images')) {
        fs.mkdirSync('images');
    }

    data, _ = downloadImages(data);

    let input = "";
    if (lang === "fr"){
        input = './template/texFileFr.tex';
    } else {
        input = './template/texFileEn.tex';
    }
    
    let render = nunjucksRender(input, data);
    
    if (render){
        console.log("Generating PDF...");
        const inputStream = fs.createReadStream('./out.tex');
        const outputStream = fs.createWriteStream('output.pdf');
        const pdf = latex(inputStream);
        
        pdf.pipe(outputStream);
        pdf.on('error', err => console.error(err));
        pdf.on('finish', () => console.log('PDF generated!'));
    } else {
        console.log("Error: PDF not generated");
    }
}

function downloadImages(data, imgCount = 0, imgDir = 'images') {
    if (typeof data === 'object') {
        for (let key in data) {
            if (key === 'image') {
                imgCount++;
                const imgPath = `${imgDir}/image${imgCount}.png`;
                downloadImage(data[key], imgPath);
                data[key] = imgPath;
            } else {
                [data[key], imgCount] = downloadImages(data[key], imgCount, imgDir);
            }
        }
    } else if (Array.isArray(data)) {
        for (let i = 0; i < data.length; i++) {
            [data[i], imgCount] = downloadImages(data[i], imgCount, imgDir);
        }
    }
    return [data, imgCount];
}

function downloadImage(url, dest) {
    const file = fs.createWriteStream(dest);
    https.get(url, (response) => {
        response.pipe(file);
        file.on('finish', () => {
            file.close();
            console.log('Download Completed');
        });
    }).on('error', (err) => {
        fs.unlink(dest);
        console.error('Error downloading the image: ', err.message);
    });
}

function nunjucksRender(filePath, data){
    nunjucks.configure({ autoescape: false });
    try {
        let file = fs.readFileSync(filePath, 'utf8');
        let template = nunjucks.compile(file);
        let result = template.render(data);
        fs.writeFileSync("./out.tex", result, 'utf8');
        console.log("File out.tex written");
        return true;
    } catch (error) {
        console.log("Error nunjucksRender: ", error);
        return false;
    }
}

const templateData = JSON.parse(fs.readFileSync("./template.json", 'utf8'));
generatePDF(templateData, "fr");
