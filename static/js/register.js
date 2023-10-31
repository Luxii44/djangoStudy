$(function(){

	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;
	var error_check = false;


	$('#user_name').blur(function() {
		check_user_name();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#email').blur(function() {
		check_email();
	});

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意').show();
		}
	});


	function check_user_name(){
		var len = $('#user_name').val().length;
		if(len<5||len>20)
		{
			$('#user_name').next().html('请输入5-20个字符的用户名').show();
			error_name = true;
		}
		else
		{
			//ajax校验用户名是否重名
			$.get('/user/username_exist/',{'username':$('#user_name').val()},function (xhr) {
				if(xhr.code == 400){
					$('#user_name').next().html(xhr.msg).show();
					error_name = true;
				}else{
					$('#user_name').next().hide();
					error_name = false;
				}
            });
		}
	}

	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<6||len>20)
		{
			$('#pwd').next().html('密码最少6位，最长20位').show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}		
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致').show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}		
		
	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
		if(re.test($('#email').val()))
		{
			$('#email').next().hide();
			error_email = false;
			//ajax校验邮箱是否重名
			$.get('/user/email_exist/',{'email':$('#email').val()},function (xhr) {
				if(xhr.code == 400){
					$('#email').next().html(xhr.msg).show();
					error_name = true;
				}else{
					$('#email').next().hide();
					error_name = false;
				}
            });
		}
		else
		{
			$('#email').next().html('你输入的邮箱格式不正确').show();
			error_email= true;
		}
	}


	$('#reg_form').submit(function() {
		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();

		if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
		{
		    //各项检测都通过，可以提交表单
			return true;
		}
		else
		{
			return false;
		}
	});
});