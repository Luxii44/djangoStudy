$(function(){
    var usernameError = false;
    var passwordError = false;
    //校验用户名
	$('#username').blur(function () {
		var username = $.trim($('#username').val());
		if(username.length < 5 || username.length > 20){
			$('.user_error').text('请输入长度为5-20位的用户名').show();
			usernameError = true;
		}else{
            $('.user_error').hide();
            usernameError = false;
		}
    });
	//校验密码
	$('#password').blur(function () {
		var password = $.trim($('#password').val());
		if(password.length < 6 || password.length > 20){
			$('.pwd_error').text('请输入长度为6-20位的密码').show();
			passwordError = true;
		}else{
            $('.pwd_error').hide();
            passwordError = false;
		}
    });
	//表单提交
    $('form').submit(function () {
        $('#username').blur();
        $('#password').blur();
        if (usernameError || passwordError){
            return false;
        }else{
            //判断记住密码选项是否被勾选
            if($('#remember').is(':checked')){
               var remember = 1;
            }else{
                var remember = 0;
            }
            //ajax提交表单
            var url = '/user/login/';
            var data = {
                'username': $.trim($('#username').val()),
                'password': $.trim($('#password').val()),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'remember': remember
            };
            $.post(url,data,function (xhr) {
                if (xhr.code == 200){
                    var from_url = $('#from_url').val();
                    if ( from_url != '')
                        window.location.href = from_url;
                    else
                        window.location.href = xhr.pre_url;
                }else{
                    $('#info').text(xhr.msg).show();
                }
            });
        }
        return false;
    });

});