$(function(){
	var error_name = false;
	var error_email = false;

	$('#user_name').blur(function() {
		check_user_name();
	});

	$('#email').blur(function() {
		check_email();
	});
    $('#user_name').focus(function() {
		$('#info').hide();
	});

	$('#email').focus(function() {
		$('#info').hide();
	});
	function check_user_name(){
		var len = $('#user_name').val().length;
		if(len<5||len>20)
		{
			$('#user_name').next().html('请输入5-20个字符的用户名').show();
			error_name = true;
		}else {
			$('#user_name').next().hide()
		}
	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
		if(!re.test($('#email').val())){
			$('#email').next().html('你输入的邮箱格式不正确').show();
		}else{
			$('#email').next().hide();
		}
	}

	//找回密码
	$('#find_password').click(function () {
		check_user_name();
		check_email();
		if(error_name == false && error_email == false){
			var url = '/user/find_password/';
			var data = {
				'username': $.trim($('#user_name').val()),
				'email': $.trim($('#email').val()),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			}
			$.post(url,data,function (xhr) {
              if (xhr.code == 200){
                   $('#info').text(xhr.msg).css('color','green').show();
              }else{
                   $('#info').text(xhr.msg).show();
              }
            });
		}
    });
});