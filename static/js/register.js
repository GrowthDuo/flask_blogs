// 点击事件
// alert("hello")
// // 定义一个函数，等待页面加载完毕再执行
$(function () {
    // 绑定点击事件
    $("#captcha-btn").click(function (event) {
       // $this 代表当前点击的按钮对象
        var $this = $(this);
        //  阻止默认行为
        event.preventDefault();
        //     获取邮箱输入框输入值
        var emails = $("#exampleInputEmail1").val();
        $.ajax({
            url: "/auth/number/email?email="+emails,
            methods: "GET",
            success:function (result) {
                var code = result['code'];
                if (code == 200){
                    // 进行倒计时
                    var countdown = 60;
                    // 倒计时中，不可再点击
                    $this.off("click");
                    var timer = setInterval(function(){
                       //  修改值
                        $this.text(countdown);
                        countdown-=1;
                        if (countdown <= 0){
                            // 清除定时器
                            clearInterval(timer);
                            // 修改文字
                            $this.text("获取验证码");
                            // 倒计时结束可重新获取点击事件
                            $this.on("click",function (event) {
                                //  阻止默认行为
                                event.preventDefault();
                                //  重新获取验证码
                                $("#captcha-btn").click();
                            });
                        }
                       // 更新倒计时，1000为1秒
                    },1000);
                    alert("验证码已发送到您的邮箱，请注意查收")
                }else {
                   alert(result["message"]);
                }
            },
            fail:function (error) {
                console.log(error);
            }
        })

    });
});


