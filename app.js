const CachetAPI = require('cachet-api');
const request = require('requestretry');
const config = require('./config/config');
const util = require('./util');

const cachet = new CachetAPI({
    url: config.api_url,
    apiKey: config.api_token
});

let monitoringList = config.monitoring;

function onlyOnError(err, response, body){
    // retry the request if we had an error or if the response was a 'Bad Gateway'
    return err || response.statusCode === 502;
}

for(let i = 0; i < monitoringList.length; i++){
    if (monitoringList[i]['scheme'].toLowerCase() === 'https') {
        let options = {
            uri: monitoringList[i]['scheme'] + '://' + monitoringList[i]['host'],
            method: monitoringList[i]['method'],
            headers: {
                'User-Agent': 'Cachet-Monitor'
            },
            timeout: monitoringList[i]['timeout'] * 1000,
            maxAttempts: config.maxAttempts,
            retryDelay: config.retryDelay * 1000,
            retryStrategy: request.RetryStrategies.NetworkError
        };

        let startTime = Date.now();
        request(options, (err, res, body) =>{
            if(!err){
                let responseTime = Date.now() - startTime;
                let statusCode = res.statusCode;
                console.log(util.httpErrors[parseInt(statusCode)]);
                if(!monitoringList[i]['expected_status_code'].includes(statusCode)){
                    console.log("Error not what i expected")
                }
                delete res['body'];
                console.log(responseTime);
                console.log(JSON.stringify(res))
            }else{
                console.log(err);
            }
        })
    }
    else if (monitoringList[i]['scheme'].toLowerCase() === 'http'){

    } else {
        console.log('Unknown schema');
    }
}