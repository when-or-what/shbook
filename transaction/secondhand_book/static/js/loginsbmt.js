function login() {
    console.log("登录测试");
    // 获得用户输入的用户名
    let username = $("#username").value;
    let password = $("#password").value;
    // 对用户密码进行SHA256加密
    // let masked_pswd = SHA256(password);
    let masked_pswd = password;
    $.ajax({
        type: "POST",
        url: "login/",    //后台处理函数的url
        data: {
            username: username,
            password: masked_pswd
        },
        success: function (result) {  //获取后台处理后传过来的result 
            console.log(result);
        },
    });
}