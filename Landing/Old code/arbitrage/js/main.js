$( document ).ready(function() {
	
	if ($('#priceBoxes').length > 0)
	{
		// opacity:0 und display:none werden von mixitup
		// unbedingt benötigt, damit die filter funktionieren
		// nicht direkt im css sondern hier, damit user die javascript deaktiverit haben die priceboxes überhaupt sehen
		$('#priceBoxes').prepend("<style>div.mix { opacity: 0; display: none; }</style>");
		
		// erst danach mixitup starten
		$('#priceBoxes').mixitup();
	}
	
	// fix submenus on mobiles
	$('.dropdown-submenu ul.dropdown-menu li a').on('touchstart', function(e) {
	    e.preventDefault();
	    window.location.href = $(this).attr('href');
	})
	
	$('#opener').on('click', function() {		
		var panel = $('#slide-panel');
		if (panel.hasClass("visible")) {
			panel.removeClass('visible').animate({'margin-left':'-220px'});
		} else {
			panel.addClass('visible').animate({'margin-left':'0px'});
		}	
		return false;	
	});

	// sticky menu
	/*
    var objToStick = $("body");
	//var objToStick = $("navbar");
    //var headH = $('.head-line').height();
	//var headH = $('.navbar').offsetTop;
	//var headH = 0;
	var headH = $('.head-line').height() + $('.navbar').height();
	//$(objToStick).addClass("stickyHeader");
	
    // $(window).scroll(function () { 
    $(window).bind('scroll', function () {
        var windowScroll = $(window).scrollTop(); 
        if (windowScroll > headH) { 
            $(objToStick).addClass("stickyHeader"); 
        } else { 
            $(objToStick).removeClass("stickyHeader"); 
        }; 
    });
	*/

    //add profile menu
    $(document).on("click", ".openProf", function(){
        $(".profile-list").addClass("showProfile");
    });
	$(document).click( function(event){
      if( $(event.target).closest(".profile").length ) 
        return;
      $(".profile-list").removeClass("showProfile");
      event.stopPropagation();
    });


	// cut function
    function filterView() {
     if (window.matchMedia('(max-width: 767px)').matches) {  
            $('.user-list .fitstLine').detach().prependTo('.mobList .mobFirstList');
        } 
        else{  
            $('.mobList .mobFirstList .fitstLine').detach().prependTo('.user-list');
        };
    }
    filterView();
    $(window).resize(function() {
        filterView();
    });

	// cut function
    function filterView1() {
     if (window.matchMedia('(max-width: 767px)').matches) {
            $('.user-list .secondLine').detach().prependTo('.mobList .profMobList');
        } 
        else{
            $('.profMobList .secondLine').detach().appendTo('.user-list .profile-list');
        };
    }
    filterView1();
    $(window).resize(function() {
        filterView1();
    });



    //cut second menu for mobile
    //  function secondMobMenu() {
    //  if (window.matchMedia('(max-width: 767px)').matches) {
    //         $('.secondDeskNav .second_menu').detach().prependTo('.secondMobNav');
    //     } 
    //     else{
    //         $('.secondMobNav .second_menu').detach().appendTo('.secondDeskNav');
    //     };
    // }
    // secondMobMenu();
    // $(window).resize(function() {
    //     secondMobMenu();
    // });


	// cut function2
    function filterView2() {
        if (window.matchMedia('(max-width: 767px)').matches) {  
            $('.tableCoins .thead').detach().appendTo('.mob_view');
            $('.mob_view .thead').not('.thead:first-child').remove();
        } 
        else{  
            $('.mob_view .thead').detach().prependTo('.tableCoins');
            $('.tableCoins .thead').not('.thead:first-child').remove();
        };
    }
    filterView2();
    $(window).resize(function() { 
        filterView2();
    });


	//collapse rotate arrow in mobile
	// $(document).on("click", ".name_td", function(){
	// 	$(this).toggleClass("collapsed");
	// });
	



    // spaceJs
    // sticky banner
    // var stickyBanner = $(".spaceJs");
    // var headH2 = $('.head-line').height() + 50;
    // // var footerH = $('.footer').height();
    // // var navBox = $('.nav-box').height();
    // var icoMain = $('.ico-main').height();
    // console.log(icoMain)

    // // headH2 = headH + navBox + 50;
    // $(window).scroll(function () { 
    //     var windowScroll = $(window).scrollTop(); 
    //     if (windowScroll > headH2 && windowScroll < icoMain+headH2) { 
    //         $(stickyBanner).addClass("stickySpace");
    //     } else { 
    //         $(stickyBanner).removeClass("stickySpace"); 
    //     }; 
    // });

    //second level menu
    // $('.nav-list li a').on('mouseover', function (){
    //     $('.second_menu').removeClass('active');
    //     $('.triangle-top').removeClass('active');
    //     $('.nav-list li a').removeClass('active');
    // });
    




    //cut second menu for mobile
     function secondDeskMenu() {
     if (window.matchMedia('(min-width: 768px)').matches) {
            $('.nav-list li .icos').on('mouseover', function(){
                $('.second_menu').addClass('active');
                $(this).addClass('active');
                $('.triangle-top').addClass('active');
                $('.second-nav').addClass('active');
            });
            $('.nav-list li .icos').on('mouseout', function(){
                $('.second_menu').removeClass('active');
                $('.triangle-top').removeClass('active');
                $('.nav-list li a').removeClass('active');
                $('.second-nav').removeClass('active');
            });

            $('.second_menu').on('mouseover', function(){
                $('.nav-list li .icos').addClass('active');
                $(this).addClass('active');
                $('.triangle-top').addClass('active');
                $('.second-nav').addClass('active');
            });
            $('.second_menu').on('mouseout', function(){
                $('.nav-list li .icos').removeClass('active');
                $(this).removeClass('active');
                $('.triangle-top').removeClass('active');
                $('.second-nav').removeClass('active');
            });
            if($('.second-nav').hasClass('second-active')){
                $('.nav-list .icos').addClass('b-none'); 
            }
        } 
        else{
            $('.second_menu').on('mouseover', function(){
                $('.nav-list li .icos').removeClass('active');
                $(this).removeClass('active');
                // $('.triangle-top').removeClass('active');
                $('.second-nav').removeClass('active');
            });
        }
    }
    secondDeskMenu();
    $(window).resize(function() {
        secondDeskMenu();
    });


    //
    if($('.second-nav').hasClass('second-active')){
        $('.ico-describe').addClass('marginMenu');
    }
     


    $(document).on("click", ".second_menu li a", function(){
        $(".second_menu li a").removeClass("active");
        $(this).addClass("active");
    });


    //overview page cut function
    function filterViewLink() {
        if (window.matchMedia('(max-width: 767px)').matches) {
            $('.sortable .tbody').find('.d_row').each(function(){
                $(this).find('.desk-link .link').detach().appendTo($(this).find('.mob-link'));
                
                $(".listRemove").removeClass("name_td");
                $(".listAdd").addClass("name_td");
            })
        } 
        else{
            $('.sortable .tbody').find('.d_row').each(function(){
                $(this).find('.mob-link .link').detach().prependTo($(this).find('.desk-link'));
                $(".listRemove").addClass("name_td");
                $(".listAdd").removeClass("name_td");
            })
        };
    }
    filterViewLink();
    $(window).resize(function() { 
        filterViewLink();
    });
	
	
	/*
	
$('.alert_box').addClass('animated');
    //toggle class after clic on +
    $(document).on("click", ".watch_btn", function(e){
        e.preventDefault();
        $(this).toggleClass('minus');
    });
	*/
	
	/*

    //modal upload file
    function uploadPhoto() {
      $('.upload input[type="file"]').each(function() {
        var $input = $(this);
          $input.on('change', function(e){
          if (this.files && this.files.length > 1){
            // console.log("file NOT upload")
          }else{
            // console.log("file upload")
            $(".step2Modal .loadFile").addClass("d-none");
            $(".step2Modal .load2File").removeClass("d-none");
          }
        });
      });
    }
    uploadPhoto();

    //Back to upload file
    $(document).on("click", ".changePhoto", function(){
        $(".step2Modal .load2File").addClass("d-none");
        $(".step2Modal .loadFile").removeClass("d-none");
    });
	




    // Confirm phone number MODAL
    $(document).on("click", ".confirmBtn", function(){
        $(".confirmPhone .enterDigitBody").removeClass("d-none");
        $(".confirmPhone .confirmPhoneBody").addClass("d-none");
    });
    $(document).on("click", ".changeNumberBtn", function(){
        $(".confirmPhone .confirmPhoneBody").removeClass("d-none");
        $(".confirmPhone .enterDigitBody").addClass("d-none");
    });

    
    // Confirm phone code 
    var mobileCode = $(".mobileCode");
    // mobileCode.on('change', function(){
    //     if($(".mobileCode").val().length >= 4){
    //         console.log(">4")
    //         $(".mailModalContent").removeClass("d-none");
    //         $(".phoneModalContent").addClass("d-none");
    //     }else{
    //         console.log("4<")
    //     }
    // });
    //////////////////////////////
    mobileCode.keypress(function() {
        var dInput = this.value;
        // console.log(dInput);
        if($(".mobileCode").val().length >= 3){
            console.log(">4")
            // $(".mailModalContent").removeClass("d-none");
            // $(".phoneModalContent").addClass("d-none");
            $('.confirmPhone').modal('hide');
            $('.checkEmail').modal('show');
        }else{
            console.log("4<")
        }
    });


    //copy email value from signFormModal to checkEmail
    $(document).on("click", ".signFormBtn", function(){
        var signFormEmail = $(".signFormModal .emailJs").val();
        $(".checkEmail .emailJs").val(signFormEmail);
    });

    $(document).on("click", ".checkEmail .сhangeEmailBtn", function(){
        $('.checkEmail .check-text').addClass('d-none');
        $('.checkEmail .confirm-text').removeClass('d-none');
        $(".checkEmail .emailJs").prop( "disabled", false ).removeClass('disabled');
        $('.checkEmail .resendBtn').addClass('d-none');
        $('.checkEmail .confirmBtn').removeClass('d-none');
        $(this).addClass('d-none');
    });
    */


    //lastThing Modal
    var thingInput = $(".lastThing .thingInput");
    thingInput.keypress(function() {
        var thingVal = $(".lastThing .thingInput").val();
        // var dInput = this.value;
        // console.log(dInput);
        if(thingVal.length >= 30){
            console.log(">30")
            $(".lastThing .hideBox").removeClass("d-none");
            $(".lastThing .visBox").addClass("d-none");
        }else{
            console.log("30<")
        }
    });


    //Reset password modal
    $(document).on("click", ".resetBtn", function(){
        var resetPassInpVal = $('.resetPassInp').val();
        if(resetPassInpVal.length >= 1){
            $(".passMistakeJs").addClass("fade");
            $(".passJs").removeClass("fade");

            $(".newMailJs").text(resetPassInpVal);
            // console.log("Not empty text")
        }else{
            $(".passJs").addClass("fade");
            $(".passMistakeJs").removeClass("fade");
            // console.log("Empty text")
        }
    });

    // Phone country code
    function phoneCountry() {
        var mobileSelect = $(".countryJs");
         mobileSelect.on('change', function(){
            mobileText = this.value ;
            console.log(mobileText);
            $(".confirmPhone .code").text(mobileText);
        });
    }
    phoneCountry();

});



//submit coin form
$(document).ready(function(){
    //jQuery time
    var current_fs, next_fs, previous_fs; //fieldsets
    var left, opacity, scale; //fieldset properties which we will animate
    var animating; //flag to prevent quick multi-click glitches

    // blur validation
    // $(document).on("blur", ".sub-form input", function(){
    //     if($(this).val() != ''){
    //         $(this).removeClass('error');
    //     }
    //     else{
    //         $(this).addClass('error');
    //     }
    // });

    $(document).on("click", ".sub-form .next", function(){
        var send = true;
        $(this).closest('fieldset').find('.require').each(function(){
            if(!$(this).val() || $(this).val() == ''){
               $(this).addClass('error');
               send = false;
            }else{
                $(this).removeClass('error');
            }
        });
        
        var pattern = /^[a-z0-9_-]+@[a-z0-9-]+\.[a-z]{2,6}$/i;
        $(this).closest('fieldset').find('input.mailValid').each(function(){
            if($(this).val() != ''){
                if($(this).val().search(pattern) == 0){
                    $(this).removeClass('error');
                    $(this).closest('.mailVilidBox').find('.validation_text').remove();
                }else{
                    $(this).addClass('error');
                    $(this).closest('.mailVilidBox').find('.validation_text').remove();
                    $(this).closest('.mailVilidBox').append("<div class='validation_text'>Incorrect email adress</div>");
                    send = false;
                }
            }else{
                $(this).addClass('error');
                $(this).closest('.mailVilidBox').find('.validation_text').remove();
                // $(this).closest('.mailVilidBox').append("<div class='validation_text'>This is a required field</div>");
            }
        });

        //empty radio
        $(this).closest('fieldset').find(".emptyRadio input[type='radio']").each(function(){
            var emptyRadio = $('fieldset').find(".emptyRadio input[type='radio']");
            if( ! emptyRadio.is(':checked')){
                $(".emptyRadio").closest('fieldset').find('.radioError').removeClass('d-none');
                send = false;
            }else{
                $(".emptyRadio").closest('fieldset').find('.radioError').addClass('d-none');
            }
        });
        //yes value
        $(this).closest('fieldset').find(".choiseThumb input[type='radio']").each(function(){
            var radioBtn = $(".choiseThumb input[type='radio']:checked").val();
            console.log(radioBtn)
            if(radioBtn === "no"){
                $(".choiseThumb").closest('fieldset').find('.radioError').removeClass('d-none');
                send = false;
            }else{
                $(".choiseThumb").closest('fieldset').find('.radioError').addClass('d-none');
            }
        });

        //select
        $(this).closest('fieldset').find('select.require').each(function(){
            if (!$(this).val() || $(this).val() == '') {
                $(this).addClass('error');
                // console.log('false')
                send = false;
            }else{
                $(this).removeClass('error');
                // console.log('true')
            }
        });

        //multiselect validation
        $(this).closest('fieldset').find('.multiple-selected.require').each(function(){
            if (!$(this).val() || $(this).val() == '') {
                $(this).closest('.custom_select').find('.multiselect.btn').addClass('error');
                send = false;
            }else{
                $(this).closest('.custom_select').find('.multiselect.btn').removeClass('error');
            }
        });

        //upload file
        $(this).closest('fieldset').find('.uploadBtn').each(function(){
            if($(".uploadBtn").val() == ''){ 
                $(".uploadFile").css('color','red');
                $(".uploadFile").text('file not loaded');
                send = false;
            }else{
                $(".uploadFile").css('color','#a7a7a7');
            }
        });

        $(this).closest('fieldset').find('.uploadBtn2').each(function(){
            if($(".uploadBtn2").val() == ''){ 
                $(".uploadFile2").css('color','red');
                $(".uploadFile2").text('file not loaded');
                send = false;
            }else{
                $(".uploadFile2").css('color','#a7a7a7');
            }
        });


        if(!send) return false;



        if(animating) return false;
        animating = true;
        
        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

        //activate next step on progressbar using the index of next_fs
        $(".progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
        
        //show the next fieldset
        next_fs.show(); 
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale current_fs down to 80%
                scale = 1 - (1 - now) * 0.2;
                //2. bring next_fs from the right(50%)
                left = (now * 50)+"%";
                //3. increase opacity of next_fs to 1 as it moves in
                opacity = 1 - now;
                current_fs.css({
            'transform': 'scale('+scale+')',
            'position': 'absolute'
          });
                next_fs.css({'left': left, 'opacity': opacity});
            }, 
            duration: 800, 
            complete: function(){
                current_fs.hide();
                animating = false;
            }, 
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });

        //
        var next_h = next_fs.height();
        $(".sub-form").css('padding-bottom',next_h);
        // console.log('next_h =' +next_h);
        $(".sub-form fieldset").css('position','absolute');

    });

    

    $(document).on("click", ".sub-form .previous", function(){
        if(animating) return false;
        animating = true;
        
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();
        
        //de-activate current step on progressbar
        $(".progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
        
        //show the previous fieldset
        previous_fs.show(); 
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale previous_fs from 80% to 100%
                scale = 0.8 + (1 - now) * 0.2;
                //2. take current_fs to the right(50%) - from 0%
                left = ((1-now) * 50)+"%";
                //3. increase opacity of previous_fs to 1 as it moves in
                opacity = 1 - now;
                current_fs.css({'left': left});
                previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity,  });
            }, 
            duration: 800, 
            complete: function(){
                current_fs.hide();
                animating = false;
            }, 
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });


        var previous_h = previous_fs.height();
        $(".sub-form").css('padding-bottom',previous_h);
        console.log('previous_h = ' +previous_h)

    });



    $(document).on("click", ".sub-form .submitForm", function(){
        var send = true;
        $(this).closest('fieldset').find('.require').each(function(){
            if(!$(this).val() || $(this).val() == ''){
               $(this).addClass('error');
               send = false;
            }else{
                $(this).removeClass('error');
            }
        });

        if(!send) return false;
    });



    //clone form
    var count = 0;
    $(document).on("click", ".addTeamBtn", function(){
        if(count < 4){
            var current_fs = $('.team-fieldset').height();
            var team_h = $('.teamBox').height();
            $(".sub-form").css('padding-bottom',current_fs + team_h);
            console.log("current_fs + team_h =" + current_fs + team_h)
            $(".teamBox .cloneForm").clone().appendTo(".emptyBox");

            //add remove btn
            $(".emptyBox .cloneForm").find('.removeTeamBtn').remove();
            $(".emptyBox .cloneForm").append("<div class='removeTeamBtn'>Remove a Team Member</div>");

            //remove text in clone input fields
            if($(".cloneForm .form-input").val().length >= 1){
                $(".emptyBox .cloneForm .form-input").each(function(){
                    $(".emptyBox .cloneForm .form-input").val('');
                });
            }
            // if($(".emptyBox .cloneForm .form-input").val().length >= 1){
            //     $(this).val();
            // }
            count ++;
        }else{
            console.log('stop clone')
        }
    });
    //remove clone form
    $(document).on("click", ".removeTeamBtn", function(){
        if(count <= 4){
            $(this).closest('.cloneForm').remove();
            count --;
        }
    });


    //custom upload file
    $(".uploadBtn").on('change', function(){
        $(".uploadFile").text(this.value);
        $(".uploadFile").css('color','#a7a7a7');
        var carrent_h = current_fs.height();
        // console.log('carrent_h =' +carrent_h);
        $(".sub-form").css('padding-bottom',carrent_h);
    });

    $(".uploadBtn2").on('change', function(){
        $(".uploadFile2").text(this.value);
        $(".uploadFile2").css('color','#a7a7a7');
        var carrent_h = current_fs.height();
        // console.log('carrent_h-2 =' +carrent_h);
        $(".sub-form").css('padding-bottom',carrent_h);
    });

        //custom upload file
//     $(".uploadBtn").on('change', function(){
//         // $(".uploadFile").text(this.value);
//         // $(".uploadFile").css('color','#a7a7a7');
//         $(this).closest('fieldset .control-group').find('.uploadFile').text(this.value);
//         $(this).closest('fieldset .control-group').find('.uploadFile').css('color','#a7a7a7');
//     });


        





    
    $(document).on("click", ".sendWallet", function(){
        // if($('.inputWallet').val() != ''){
        if($('.inputWallet').val() == '' || $('.inputWallet').val().length < 40){
            $('.inputWallet').addClass('error');
            $(".priority-pass .wallet-step").removeClass('d-none');
            $(".priority-pass .mail-box .text").removeClass('d-none');
            $(".sendMail").removeClass('d-none');
            $(".newChange").addClass('d-none');
            $(".priority-pass .activate").removeClass('white-btn');
        }else{
            $('.inputWallet').removeClass('error');
            $(".priority-pass .wallet-step").addClass('d-none');
            $(".priority-pass .mail-box .text").addClass('d-none');
            $(".sendMail").addClass('d-none');
            $(".changeMail").removeClass('d-none');
            $(".priority-pass .activate").addClass('white-btn');
        }
        $('.inputChangeWallet').val($('.inputWallet').val());
    });


    
    $(document).on("click", ".addWalletModal .btn", function(event){
        var inputModalWallet = $('.сhangeModalWallet').val();
        if(inputModalWallet == '' || inputModalWallet.length < 40){
            $('.сhangeModalWallet').addClass('error');
            // console.log('false')
            event.preventDefault();
        }else{
            $('.inputWallet').val(inputModalWallet);
            $('.сhangeModalWallet').removeClass('error');
            $('.addWalletModal').modal('hide');
            // console.log('true')
        }
    });

    $(document).on("click", ".changeWalletBtn", function(){
        $('.addWalletModal').addClass('changeModal');
    });

    $(document).on("click", ".changeModal .btn", function(event){
        var inputModalWallet = $('.сhangeModalWallet').val();
        if(inputModalWallet == '' || inputModalWallet.length < 40){
            $('.сhangeModalWallet').addClass('error');
            event.preventDefault();
        }else{
            $('.inputChangeWallet').val(inputModalWallet);
            $('.сhangeModalWallet').removeClass('error');
            $('.addWalletModal').modal('hide');
        }
    });


    //calculator page
    $('.calculator tr').find('.altcoin').each(function(){
        var this_val = $(this).val();
        $(this).closest('tr').find('.btc span').text(this_val);
    });

    $('.calculator tr').find('.altcoin').on('change', function(){
        var this_val = $(this).val();
        var this_price = $(this).closest('tr').find('td:nth-child(2)').text();
        var price_float = parseFloat(this_price);
        var result = (this_val * price_float).toFixed(8);
        $(this).closest('tr').find('.btc span').text(result);

        // var summ = 0;
        // $(".calculator tr .btc span").each(function(){
        //     summ += parseFloat($(this).text());
        //     console.log("summ =" + summ)
        //     $('.calculator tfoot #sum').text(summ.toFixed(8));
        // })
    });

    //profile page
    $(document).on("click", ".phone-numbers-table .close_input", function(){
        $(this).closest('.phone-numbers-table').remove();
    });
    // $(document).on("click", ".addPhone", function(){
    //     $(this).hide();
    // });
    


    // form validation 
    $(".validForm").submit(function(){
        var emailPattern = /^[a-z0-9_-]+@[a-z0-9-]+\.[a-z]{2,6}$/i;
        var send = true;
            $(this).find('.require').each(function(){
                if(!$(this).val() || $(this).val() == ''){
                   $(this).addClass('error');
                   send = false;
                }else{
                    $(this).removeClass('error');
                }
            });
            $(this).find('input.mailValid').each(function(){
                if($(this).val() != ''){
                    if($(this).val().search(emailPattern) == 0){
                        $(this).removeClass('error');
                        $(this).closest('.mailVilidBox').find('.validation_text').remove();
                    }else{
                        $(this).addClass('error');
                        $(this).closest('.mailVilidBox').find('.validation_text').remove();
                        $(this).closest('.mailVilidBox').append("<div class='validation_text'>Incorrect email adress</div>");
                        send = false;
                    }
                }else{
                    $(this).addClass('error');
                    $(this).closest('.mailVilidBox').find('.validation_text').remove();
                    send = false;
                }
            });
        if(!send) return false;
    });



// Sorting
 //   (function($) {
	//     $.fn.clickToggle = function(func1, func2) {
	//         var funcs = [func1, func2];
	//         this.data('toggleclicked', 0);
	//         this.click(function() {
	//             var data = $(this).data();
	//             var tc = data.toggleclicked;
	//             $.proxy(funcs[tc], this)();
	//             data.toggleclicked = (tc + 1) % 2;
	//         });
	//         return this;
	//     };
	// }(jQuery));

 //        var a_sort = $('.sort-head .title');
 //        var div_conteiner = jQuery.makeArray($('.sortable .d_row'));

 //   		a_sort.each(function (index, self) {
 //            var id = $(self).attr("id");
 //            var reg = new RegExp("^.*?(" + id + "\\S+).*?$");
 //            // $(self).click(function (e) {
 //   			$(self).clickToggle(function(e) {
 //                // e.preventDefault();
 //                a_sort.removeClass('sorting_desc');
 //            	a_sort.removeClass('sorting_asc');
 //                $(this).addClass('sorting_asc');
 //                div_conteiner.sort(function f(a, b) {
 //                    a = a.className.replace(reg, '$1');
 //                    b = b.className.replace(reg, '$1');
 //                    var c = 0
 //                    if (a > b) c = 1;
 //                    if (a < b) c = -1;
 //                    return c
 //                });
 //                $.map(div_conteiner, function (div) {
 //                    $(div).appendTo($('.sortable .tbody'))
 //                });
 //            },
				
	// 		function(e){
 //                // e.preventDefault();
 //                a_sort.removeClass('sorting_asc');
 //            	a_sort.removeClass('sorting_desc');
 //                $(this).addClass('sorting_desc');
 //                div_conteiner.sort(function f(a, b) {
 //                    a = a.className.replace(reg, '$1');
 //                    b = b.className.replace(reg, '$1');
 //                    var c = 0
 //                    if (a > b) c = -1;
 //                    if (a < b) c = 1;
 //                    return c
 //                });
 //                $.map(div_conteiner, function (div) {
 //                    $(div).appendTo($('.sortable .tbody'))
 //                });
 //            });
 //   		});


    //cut discover card block
    function cardCut() {
        if (window.matchMedia('(min-width:992px) and (max-width: 1630px)').matches) {
            $('.area-4 .cardCut-1').detach().appendTo('.area-1');
            $('.area-4 .cardCut-2').detach().appendTo('.area-2');
            $('.area-4 .cardCut-3').detach().appendTo('.area-3');
        }else{
            $('.area-1 .cardCut-1').detach().appendTo('.area-4');
            $('.area-1 .cardCut-2').detach().appendTo('.area-4');
            $('.area-1 .cardCut-3').detach().appendTo('.area-4');
        }
    }
    cardCut();
    $(window).resize(function() {
        cardCut();
    });


    //
    $(document).on("click", ".chart-thumb .btn", function(){
        $(".chart-thumb .btn").removeClass('active');
        $(this).addClass('active');
    });


    //pair2 page
    if($('.pair2 .market-container .market-item').length >= 12){
        $('.moreBtnJs').removeClass('d-none');
    }else{
        $('.moreBtnJs').addClass('d-none');
    }

    $('.pair2 .collapse').on('shown.bs.collapse', function () {
        $(this).closest('.pair2').find('.moreBtnJs .btn').text('See less');
    });
    $('.pair2 .collapse').on('hidden.bs.collapse', function () {
        $(this).closest('.pair2').find('.moreBtnJs .btn').text('See all');
    });
    


    // back button based on the users last web page
    $(document).on("click", ".back-btn", function(){
        parent.history.back();
        return false;
        console.log('clickclack');
    });


});


// Max height text blocks on priority-pass page
function heightTextBlocks(){
    var maxHeight = 0;
        $(".market-box").each(function(){
          if ( $(this).height() > maxHeight ){
            maxHeight = $(this).height();
          }
        });
    $(".priority-pass .market-box").height(maxHeight);
    // console.log("maxHeight= " + maxHeight);
}
function heightTextBlocksResize(){
    $(".priority-pass .market-box").css( "height", "auto" );
        var maxHeight = 0;
        $(".priority-pass .market-box").each(function(){
          if ( $(this).height() > maxHeight ){
            maxHeight = $(this).height();
          }
        });
    $(".priority-pass .market-box").height(maxHeight);
    // console.log("maxHeight-2= " + maxHeight);
}
$(document).ready(function() {
    heightTextBlocks();
});
$(window).resize(function() { 
    heightTextBlocksResize();
});






// Textarea Autosize
(function (global, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['exports', 'module'], factory);
    } else if (typeof exports !== 'undefined' && typeof module !== 'undefined') {
        factory(exports, module);
    } else {
        var mod = {
            exports: {}
        };
        factory(mod.exports, mod);
        global.autosize = mod.exports;
    }
})(this, function (exports, module) {
    'use strict';

    var map = typeof Map === "function" ? new Map() : (function () {
        var keys = [];
        var values = [];

        return {
            has: function has(key) {
                return keys.indexOf(key) > -1;
            },
            get: function get(key) {
                return values[keys.indexOf(key)];
            },
            set: function set(key, value) {
                if (keys.indexOf(key) === -1) {
                    keys.push(key);
                    values.push(value);
                }
            },
            'delete': function _delete(key) {
                var index = keys.indexOf(key);
                if (index > -1) {
                    keys.splice(index, 1);
                    values.splice(index, 1);
                }
            }
        };
    })();

    var createEvent = function createEvent(name) {
        return new Event(name, { bubbles: true });
    };
    try {
        new Event('test');
    } catch (e) {
        // IE does not support `new Event()`
        createEvent = function (name) {
            var evt = document.createEvent('Event');
            evt.initEvent(name, true, false);
            return evt;
        };
    }

    function assign(ta) {
        if (!ta || !ta.nodeName || ta.nodeName !== 'TEXTAREA' || map.has(ta)) return;

        var heightOffset = null;
        var clientWidth = ta.clientWidth;
        var cachedHeight = null;

        function init() {
            var style = window.getComputedStyle(ta, null);

            if (style.resize === 'vertical') {
                ta.style.resize = 'none';
            } else if (style.resize === 'both') {
                ta.style.resize = 'horizontal';
            }

            if (style.boxSizing === 'content-box') {
                heightOffset = -(parseFloat(style.paddingTop) + parseFloat(style.paddingBottom));
            } else {
                heightOffset = parseFloat(style.borderTopWidth) + parseFloat(style.borderBottomWidth);
            }
            // Fix when a textarea is not on document body and heightOffset is Not a Number
            if (isNaN(heightOffset)) {
                heightOffset = 0;
            }

            update();
        }

        function changeOverflow(value) {
            {
                // Chrome/Safari-specific fix:
                // When the textarea y-overflow is hidden, Chrome/Safari do not reflow the text to account for the space
                // made available by removing the scrollbar. The following forces the necessary text reflow.
                var width = ta.style.width;
                ta.style.width = '0px';
                // Force reflow:
                /* jshint ignore:start */
                ta.offsetWidth;
                /* jshint ignore:end */
                ta.style.width = width;
            }

            ta.style.overflowY = value;
        }

        function getParentOverflows(el) {
            var arr = [];

            while (el && el.parentNode && el.parentNode instanceof Element) {
                if (el.parentNode.scrollTop) {
                    arr.push({
                        node: el.parentNode,
                        scrollTop: el.parentNode.scrollTop
                    });
                }
                el = el.parentNode;
            }

            return arr;
        }

        function resize() {
            var originalHeight = ta.style.height;
            var overflows = getParentOverflows(ta);
            var docTop = document.documentElement && document.documentElement.scrollTop; // Needed for Mobile IE (ticket #240)

            ta.style.height = '';

            var endHeight = ta.scrollHeight + heightOffset;

            if (ta.scrollHeight === 0) {
                // If the scrollHeight is 0, then the element probably has display:none or is detached from the DOM.
                ta.style.height = originalHeight;
                return;
            }

            ta.style.height = endHeight + 'px';

            // used to check if an update is actually necessary on window.resize
            clientWidth = ta.clientWidth;

            // prevents scroll-position jumping
            overflows.forEach(function (el) {
                el.node.scrollTop = el.scrollTop;
            });

            if (docTop) {
                document.documentElement.scrollTop = docTop;
            }
        }

        function update() {
            resize();

            var styleHeight = Math.round(parseFloat(ta.style.height));
            var computed = window.getComputedStyle(ta, null);

            // Using offsetHeight as a replacement for computed.height in IE, because IE does not account use of border-box
            var actualHeight = computed.boxSizing === 'content-box' ? Math.round(parseFloat(computed.height)) : ta.offsetHeight;

            // The actual height not matching the style height (set via the resize method) indicates that
            // the max-height has been exceeded, in which case the overflow should be allowed.
            if (actualHeight !== styleHeight) {
                if (computed.overflowY === 'hidden') {
                    changeOverflow('scroll');
                    resize();
                    actualHeight = computed.boxSizing === 'content-box' ? Math.round(parseFloat(window.getComputedStyle(ta, null).height)) : ta.offsetHeight;
                }
            } else {
                // Normally keep overflow set to hidden, to avoid flash of scrollbar as the textarea expands.
                if (computed.overflowY !== 'hidden') {
                    changeOverflow('hidden');
                    resize();
                    actualHeight = computed.boxSizing === 'content-box' ? Math.round(parseFloat(window.getComputedStyle(ta, null).height)) : ta.offsetHeight;
                }
            }

            if (cachedHeight !== actualHeight) {
                cachedHeight = actualHeight;
                var evt = createEvent('autosize:resized');
                try {
                    ta.dispatchEvent(evt);
                } catch (err) {
                    // Firefox will throw an error on dispatchEvent for a detached element
                    // https://bugzilla.mozilla.org/show_bug.cgi?id=889376
                }
            }
        }

        var pageResize = function pageResize() {
            if (ta.clientWidth !== clientWidth) {
                update();
            }
        };

        var destroy = (function (style) {
            window.removeEventListener('resize', pageResize, false);
            ta.removeEventListener('input', update, false);
            ta.removeEventListener('keyup', update, false);
            ta.removeEventListener('autosize:destroy', destroy, false);
            ta.removeEventListener('autosize:update', update, false);

            Object.keys(style).forEach(function (key) {
                ta.style[key] = style[key];
            });

            map['delete'](ta);
        }).bind(ta, {
            height: ta.style.height,
            resize: ta.style.resize,
            overflowY: ta.style.overflowY,
            overflowX: ta.style.overflowX,
            wordWrap: ta.style.wordWrap
        });

        ta.addEventListener('autosize:destroy', destroy, false);

        // IE9 does not fire onpropertychange or oninput for deletions,
        // so binding to onkeyup to catch most of those events.
        // There is no way that I know of to detect something like 'cut' in IE9.
        if ('onpropertychange' in ta && 'oninput' in ta) {
            ta.addEventListener('keyup', update, false);
        }

        window.addEventListener('resize', pageResize, false);
        ta.addEventListener('input', update, false);
        ta.addEventListener('autosize:update', update, false);
        ta.style.overflowX = 'hidden';
        ta.style.wordWrap = 'break-word';

        map.set(ta, {
            destroy: destroy,
            update: update
        });

        init();
    }

    function destroy(ta) {
        var methods = map.get(ta);
        if (methods) {
            methods.destroy();
        }
    }

    function update(ta) {
        var methods = map.get(ta);
        if (methods) {
            methods.update();
        }
    }

    var autosize = null;

    // Do nothing in Node.js environment and IE8 (or lower)
    if (typeof window === 'undefined' || typeof window.getComputedStyle !== 'function') {
        autosize = function (el) {
            return el;
        };
        autosize.destroy = function (el) {
            return el;
        };
        autosize.update = function (el) {
            return el;
        };
    } else {
        autosize = function (el, options) {
            if (el) {
                Array.prototype.forEach.call(el.length ? el : [el], function (x) {
                    return assign(x, options);
                });
            }
            return el;
        };
        autosize.destroy = function (el) {
            if (el) {
                Array.prototype.forEach.call(el.length ? el : [el], destroy);
            }
            return el;
        };
        autosize.update = function (el) {
            if (el) {
                Array.prototype.forEach.call(el.length ? el : [el], update);
            }
            return el;
        };
    }
    module.exports = autosize;
});

//initial textarea autosize
$(document).ready(function(){
    autosize(document.querySelectorAll('.textarea'));
});