const cryptoJS = require("crypto-js");


function getParams() {
    let  n = Math.ceil(10*Math.random())
    n=1
    let i = new Date().getTime()
    i='1736548788540'
    let s = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    let f = "&key=A013F70DB97834C0A5492378BD76C53A"
    let c = "method=GET&timeStamp="+i
        +"&User-Agent="+s
        +"&index="+n
        +"&channelId=40011"
        +"&sVersion=1"
    const hashHex = cryptoJS.MD5(c + f).toString(cryptoJS.enc.Hex);

    const params = {
        channelId: 40011,
        index: n,
        timeStamp: i,
        signKey:hashHex,
        sVersion: 1,
        WuKongReady: 'h5',
        webdriver:false
    }
    return params
}


function getMygsig(url,params, headers, body) {

    const info = params
    info['path'] = url.replace('https://www.maoyan.com', '')
    const str = Object.entries(info)
        .map(([key,value]) => [key,value.toString()])
        .sort((a,b) => a[0].localeCompare(b[0]))
        .map((item) => item[1]).join('_')

    console.log(str)

    const prefix = '581409236'
    let timeStamp = new Date().getTime()
    timeStamp = '1736548788543'
    const ms1 = prefix+"#"+str+"$"+timeStamp

    const hashHex = cryptoJS.MD5(ms1).toString(cryptoJS.enc.Hex);
    console.log(hashHex)
    const mygsig = {
        'm1':'0.0.1',
        'm2':'0',
        'ms1':hashHex,
        'ts':timeStamp
    }
    console.log(mygsig)
    return JSON.stringify(mygsig)
}

const url = "https://www.maoyan.com/ajax/films/35830";

const headers = {
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
};

const body = null;

getMygsig(url,getParams(),headers, body)
