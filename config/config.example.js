const config = {
    api_url: "https://monitor.gaz492.uk",
    api_token: "api_token_here",
    use_schedule: false,
    interval: 120,
    retries: 3,
    monitoring: [
        {
            name: "Site 1",
            scheme: 'http',
            host: "google.com",
            port: 80,
            method: "GET",
            component_id: 1,
            timeout: 5,
            expected_status_code: [200]
        },
        {
            name: "Site 2",
            scheme: 'https',
            host: "bing.com",
            port: 443,
            method: "POST",
            component_id: 1,
            timeout: 5,
            expected_status_code: [200, 201]
        }
    ]
};

module.exports = config;