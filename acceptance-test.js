import http from 'k6/http';
import { sleep } from 'k6';

export const options= {
    virtual_users: 10,
    duration: "10s",
    thresholds: {
        http_req_duration: ["p(90)<600"], // 90% of response times must be below 600ms
    },
};

// The default exported function is gonna be picked up by k6 as the entry point for the test script. It will be executed repeatedly in "iterations" (virtual users) for the whole duration of the test.
export default function () {
    // Make a GET request to the target URL
    http.get(`http://localhost:5000/`);

    // Sleep for 1 second to simulate real-world usage
    sleep(1);
}