function $(id) {
    return document.getElementById(id);
}

// חיבור ל-WebSocket
const ws = new WebSocket("ws://192.168.3.249:9999");

ws.onopen = function () {
    console.log("WebSocket connected");
};

// טיפול בשליחת טופס הלוגין
loginForm.onsubmit = function (e) {
    e.preventDefault();

    // ניקוי הודעה קודמת
    $('loginStatus').textContent = '';

    const username = $('l_username').value.trim();
    const password = $('l_password').value;

    if (ws.readyState === WebSocket.OPEN) {
        const loginData = JSON.stringify({
            action: "login",
            username: username,
            password: password
        });

        ws.send(loginData);
        console.log("request sent successfully");
    } else {
        console.log("WebSocket not ready");
    }
};

// קבלת תשובה מהשרת
ws.onmessage = function (event) {
    const res = JSON.parse(event.data);

    if (res.action === "login" && res.status === "Clear") {
        console.log("Login successful");
        window.location.href = "http://127.0.0.1:5000/login-success";    }
    else {
        $('loginStatus').textContent = "SQL Injection attempt detected";
    }
};
