// JavaScript Document
var stop;
var Alert={	  
	show3sMsg:function(obj){
		var subhtml='<div id="alert_dialog_show_3s_box" style=" overflow:hidden;"><div id="alert_show_3" class="time1" style="height:100px; width:200px; background-color:#000; color:#fff; opacity:0.8;  border-radius:8px;font-size:24px; text-align:center;z-index: 2000; position:fixed;top:20%;left:45%;"><p style="padding-top:30px;">'+obj+'</p></div></div>';
		$("body").append(subhtml);
		stop=setInterval(closedShow3sMsg,1000)	
	},	
	//确认
	showMsg:function(obj){
		var subhtml='<div id="alert_dialog_show_msg_box" style=" overflow:hidden;height:100px;width:200px;margin:15% auto;"><div class="sweet-overlay" tabIndex="-1" style=" background-color:#000; opacity:0.4; position: fixed; left: 0; right: 0; top: 0; bottom: 0; z-index:1000;"></div><div id="alert_show_3" style="height:100px; width:200px; background-color:#fff; color:#000; border-radius:8px;font-size:20px; text-align:center;z-index:2000;position:absolute;"><p style="font-size:14px; margin-top:20px;">'+obj+'</p><input name="button" onclick="closedShowMsg()" type="button" value="确认" style=" cursor: pointer;width:60px; height:30px; line-height:30px;background-color:#428BCA;color:#FFF;font-size:14px;box-shadow:none;border-radius:8px;"  /></div></div>';
		$("body").append(subhtml);
	},
	showConfirmMsg:function(obj,callback){
	var subhtml='<div id="alert_dialog_show_confirm_box" style=" overflow:hidden;height:100px;width:200px;margin:15% auto;"><div class="sweet-overlay" tabIndex="-1" style=" background-color:#000; opacity:0.4; position: fixed; left: 0; right: 0; top: 0; bottom: 0; z-index:1000;"></div><div id="alert_show_3" style="height:100px; width:200px; background-color:#fff; color:#000; border-radius:8px;font-size:20px; text-align:center; position:absolute;z-index:2000;"><p style="font-size:14px; margin-top:20px;">'+obj+'</p><input name="button" onclick="rec('+callback+')" type="button" value="确认" style=" width:60px; height:30px;line-height:30px;"  /><input name="button" onclick="rec()" type="button" value="取消" style=" width:60px; height:30px;line-height:30px;"  /></div></div>';
		$("body").append(subhtml);
	 callback = callback || function(){};
	},
	
	//
	loading:function(){
   var subhtml='<style>.spinner{margin:0 auto;width:40px;height:40px;position:relative}.container1>div,.container2>div,.container3>div{width:10px;height:10px;background-color:#53d653;border-radius:100%;position:absolute;-webkit-animation:bouncedelay 1.2s infinite ease-in-out;animation:bouncedelay 1.2s infinite ease-in-out;-webkit-animation-fill-mode:both;animation-fill-mode:both}.spinner .spinner-container{position:absolute;width:100%;height:100%}.container2{-webkit-transform:rotateZ(45deg);transform:rotateZ(45deg)}.container3{-webkit-transform:rotateZ(90deg);transform:rotateZ(90deg)}.circle1{top:0;left:0}.circle2{top:0;right:0}.circle3{right:0;bottom:0}.circle4{left:0;bottom:0}.container2 .circle1{-webkit-animation-delay:-1.1s;animation-delay:-1.1s}.container3 .circle1{-webkit-animation-delay:-1.0s;animation-delay:-1.0s}.container1 .circle2{-webkit-animation-delay:-0.9s;animation-delay:-0.9s}.container2 .circle2{-webkit-animation-delay:-0.8s;animation-delay:-0.8s}.container3 .circle2{-webkit-animation-delay:-0.7s;animation-delay:-0.7s}.container1 .circle3{-webkit-animation-delay:-0.6s;animation-delay:-0.6s}.container2 .circle3{-webkit-animation-delay:-0.5s;animation-delay:-0.5s}.container3 .circle3{-webkit-animation-delay:-0.4s;animation-delay:-0.4s}.container1 .circle4{-webkit-animation-delay:-0.3s;animation-delay:-0.3s}.container2 .circle4{-webkit-animation-delay:-0.2s;animation-delay:-0.2s}.container3 .circle4{-webkit-animation-delay:-0.1s;animation-delay:-0.1s}@-webkit-keyframes bouncedelay{0%,80%,100%{-webkit-transform:scale(0.0)}40%{-webkit-transform:scale(1.0)}}@keyframes bouncedelay{0%,80%,100%{transform:scale(0.0);-webkit-transform:scale(0.0)}40%{transform:scale(1.0);-webkit-transform:scale(1.0)}}</style><div id="alert_dialog_show_loading_box" style="overflow:hidden;height:40px;width:40px;margin-left:50%;margin-top:20%;"><div class="sweet-overlay" tabIndex="-1" style="background-color:#000;opacity:0.4;position:fixed;left:0;right: 0; top: 0;bottom: 0;z-index:1000;"></div><div id="alert_show_3"  style=" position:absolute;z-index:2000;"><div class="spinner"><div class="spinner-container container1"><div class="circle1"></div><div class="circle2"></div><div class="circle3"></div><div class="circle4"></div></div><div class="spinner-container container2"><div class="circle1"></div><div class="circle2"></div><div class="circle3"></div><div class="circle4"></div></div><div class="spinner-container container3"><div class="circle1"></div><div class="circle2"></div><div class="circle3"></div><div class="circle4"></div></div></div></div></div>';
		$("body").append(subhtml);	
 
	},
	closedLoading:function(){
		  $("#alert_dialog_show_loading_box").remove();
	}	
}

//关闭弹出框
function closedShowMsg(){
		$("#alert_dialog_show_msg_box").remove();
	}


