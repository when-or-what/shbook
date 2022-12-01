//展现显现错误提示信息
function showError(message) {
    document.getElementById("messBox").style.display = "block";
    $("#errorMess").html(message);//修改span标签内容
    setTimeout("hidden()", 2000);
}
//隐藏错误提示信息
function hidden() {
    document.getElementById("messBox").style.display = "none";
}
//邮箱验证
function testEmail(str) {
    var re = /^\w+@[0-9a-z]+\.[a-z]+$/;
    return re.test(str);
}

$("#sendEmail").click(function () {
    var email = $("#email").val();//获取用户输入邮箱
    if (email === '' || !testEmail(email)) {//验证邮箱格式
        showError('邮箱格式不正确，请重输');
    }
    else {
        //按钮不可再次点击，开始倒计时
        $.ajax({
            url: "../enter_ver_code",
            type: "post",
            data: {
                type: 'sendMessage',
                csrfmiddlewaretoken: '{{ csrf_token }}',
                email: email
            },
            dataType: "json",
            success: function (reg) {
                // 短信发送失败
                if (!reg.state) {
                    showError(reg.errmsg);
                }
                else {
                    console.log(reg.state);
                    settime();//短信发送成功，倒计时
                }
            }
        });
        var btn_sendEmail = $("#sendEmail");
        var countdown = 60;
        function settime() {
            if (countdown === 0) {
                btn_sendEmail.attr("disabled", false);
                btn_sendEmail.val("获取验证码");
                return false;
            } else {
                btn_sendEmail.attr("disabled", true);
                btn_sendEmail.val("重新发送(" + countdown + ")");
                countdown--;
            }
            setTimeout(function () {
                settime();
            }, 1000);
        }
    }
});
