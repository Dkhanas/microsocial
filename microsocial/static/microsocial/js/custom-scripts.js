$(document).ready(function(){

    // The functions that must be performed when page loads

    landingCentre();
    leftBarToggle();
    

     // The functions that must be performed when window resize

     $(window).resize(function(){
        landingCentre();
        leftBarToggle();
     })

	$('.open-overlay').magnificPopup({
		type: 'inline',
        closeBtnInside: true,
        preloader: false,
        removalDelay: 500, //delay removal by X to allow out-animation
        callbacks: {
            beforeOpen: function() {
                this.st.mainClass = this.st.el.attr('data-effect');

            },
            open: function(){

              if($("#croptarget").length>0){
                selectingImage ();
              }
            },
            beforeClose: function(){
              if($("#croptarget").length>0){
                destroySelecting();
              }
            }
        },
        midClick: true // allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source.
	});


    // landing content center

    function landingCentre(){
       var allHeight = $('.page').height();
       var contentHeight = $('.header_landing').height();
       var footerHeight = $('.footer-wrap_pos').height();
       var paddinContentTop = ((allHeight - contentHeight) / 2) - footerHeight;
       var footerPos = allHeight - footerHeight;
       if (contentHeight < $(window).height()) {
        $('.footer-wrap_pos').css({
            'position' : 'absolute',
            "top" : footerPos
        })
       };
       $('.header_landing').css({
        'paddingTop' : paddinContentTop
       })
    }

    // left bar toggle

    function leftBarToggle(){
      if ($(window).width() <= 767) {
        var topMargin = $('.header').height();
        $('.left-sidebar').css({
          'top' : topMargin + 15
        })
        $('.moveMenuBtn').css({
          'top' : topMargin + 15
        })
        var sidebar = $('.left-sidebar')
        var sidebarWidth = $(sidebar).width();
        $(sidebar).css({
          'marginLeft' : - sidebarWidth - 50
        })
        $('.moveMenuBtn').click(function(){
          if ($(sidebar).hasClass('open-side')) {
            $(sidebar).removeClass('open-side')
            $(sidebar).css({
              'marginLeft' : - sidebarWidth - 50
            }, 500)
            $(this).css({
              'marginLeft' : 0
            }, 500)
            $('.shadow').css({
              "visibility" : 'hidden'
            })
          } else {
            $(sidebar).addClass('open-side')
            $(sidebar).css({
              'marginLeft' : 0
            }, 500)
             $(this).css({
              'marginLeft' : sidebarWidth - 15
            }, 500)
            $('.shadow').css({
              "visibility" : 'visible'
            })
          }
        })
      };      
    }


    // Select2 styler initial

    $(".multimediaSelect").select2({});
    $('.open-select').click(function(){
      $(".multimediaSelect").select2('open');
    })

    // Month autocomplete

    var months = [
      { 
        id: 0, text: 'January' 
      }, 
      { 
        id: 1, text: 'February' 
      }, 
      { 
        id: 2, text: 'March' 
      }, 
      { 
        id: 3, text: 'April' 
      }, 
      { 
        id: 4, text: 'May' 
      }, 
      { 
        id: 5, text: 'June' 
      }, 
      { 
        id: 6, text: 'July' 
      }, 
      { 
        id: 7, text: 'August' 
      }, 
      { 
        id: 8, text: 'September' 
      }, 
      { 
        id: 9, text: 'October' 
      }, 
      { 
        id: 10, text: 'November' 
      }, 
      { 
        id: 11, text: 'December' 
      }];

    var days = [
      { 
        id: 0, text: '1' 
      }, 
      { 
        id: 1, text: '2' 
      }, 
      { 
        id: 2, text: '3' 
      }, 
      { 
        id: 3, text: '4' 
      }, 
      { 
        id: 4, text: '5' 
      }, 
      { 
        id: 5, text: '6' 
      }, 
      { 
        id: 6, text: '7' 
      }, 
      { 
        id: 7, text: '8' 
      }, 
      { 
        id: 8, text: '9' 
      }, 
      { 
        id: 9, text: '10' 
      }, 
      { 
        id: 10, text: '11' 
      }, 
      { 
        id: 11, text: '12' 
      },
      { 
        id: 12, text: '13' 
      },
      { 
        id: 13, text: '14' 
      },
      { 
        id: 14, text: '15' 
      },
      { 
        id: 15, text: '16' 
      },
      { 
        id: 16, text: '17' 
      },
      { 
        id: 17, text: '18' 
      },
      { 
        id: 18, text: '19' 
      },
      { 
        id: 19, text: '20' 
      },
      { 
        id: 20, text: '21' 
      },
      { 
        id: 21, text: '22' 
      },
      { 
        id: 22, text: '23' 
      },
      { 
        id: 23, text: '24' 
      },
      { 
        id: 24, text: '25' 
      },
      { 
        id: 25, text: '26' 
      },
      { 
        id: 26, text: '27' 
      },
      { 
        id: 27, text: '28' 
      },
      { 
        id: 28, text: '29' 
      },
      { 
        id: 29, text: '30' 
      },
      { 
        id: 30, text: '31' 
      }];

    $(".autocompleteMonth").select2({
      placeholder: "Month",
      allowClear: true,
      data: months
    });

    $(".autocompleteDay").select2({
      placeholder: "Day",
      allowClear: true,
      data: days
    });

    // Toggle form

    $('.show-toggle-form').click(function(){
      $(this).parent().prev().slideDown(500);
    })

    // Tooltips

    $('[data-toggle="tooltip"]').tooltip();

    // Year control
    
    $('.year-control').keyup(function(){
      
      if ($(this).val().length >= 4) {
        if ($(this).val() < 1900) {
          $(this).next().text('Please enter correct year') 
        };                 
      } else {
        $('.inform-block').empty()
      }
    })

    // Cover background at user profile page
    $('#coverButton').click(function(){
      if ($('.cover-image').hasClass('cover-image-edit')) {
        $(this).text('Edit cover');
        $('.cover-image').removeClass('cover-image-edit');
        $( "#cover-image" ).draggable('destroy');
      } else {
        $(this).text('Save cover');
        $('.cover-image').addClass('cover-image-edit'); 
        $( "#cover-image" ).draggable({ axis: "y" });   
      }
    });

      // Avatar image size
      var imageWidth = $('#preview').width();
    
      var imageHeight = $('#preview').height();

      function preview(img, selection) {
        var scaleX = 100 / (selection.width || 1);
        var scaleY = 100 / (selection.height || 1);
        
         $('#preview').css({
            width: Math.round(scaleX * imageWidth) + 'px',
            height: Math.round(scaleY * imageHeight) + 'px',
            marginLeft: '-' + Math.round(scaleX * selection.x1) + 'px',
            marginTop: '-' + Math.round(scaleY * selection.y1) + 'px'
          });
         $('#preview-2').css({
             width: Math.round(scaleX * imageWidth / 1.3) + 'px',
            height: Math.round(scaleY * imageHeight / 1.4) + 'px',
            marginLeft: '-' + Math.round(scaleX * selection.x1) + 'px',
            marginTop: '-' + Math.round(scaleY * selection.y1) + 'px'          
          });
          $('#preview-3').css({
            width: Math.round(scaleX * imageWidth / 1.4) + 'px',
            height: Math.round(scaleY * imageHeight / 1.6) + 'px',
            marginLeft: '-' + Math.round(scaleX * selection.x1) + 'px',
            marginTop: '-' + Math.round(scaleY * selection.y1) + 'px'         
          });

      }

      function selectingImage(){
        $('#croptarget').imgAreaSelect({
            aspectRatio: '1:1',
            onSelectChange: preview
        });
      }
      function destroySelecting(){
        $('#croptarget').imgAreaSelect({remove:true});
      }

      $('.close-overlay').click(function(){
        $.magnificPopup.close();
      })
       
      // Dropdown header right menu

      $('.dropdown-menu-control').click(function(){
        if ($(this).hasClass('drop-opened')) {
          $(this).removeClass('drop-opened');
          $('i', this).removeClass('fa-arrow-up');
          $('i', this).addClass('fa-arrow-down');
          $('.dropdown-user-menu').slideUp(500)
        } else{
          $('i', this).removeClass('fa-arrow-down')
          $(this).addClass('drop-opened');
          $('i', this).addClass('fa-arrow-up');
          $('.dropdown-user-menu').slideDown(500)
        }
        
      })

      $(document).click(function(event) {   // Event of click on document

        var event = event || window.event;      // Crossbrouser event target = window object
        var ET = event.target || event.srcElement;

        if ($(ET).closest(".dropdown-user-menu").length) return; // <-- click out of this element 
        if ($(ET).closest(".dropdown-menu-control").length) return; // <-- click out of this element 
        $('.dropdown-user-menu').slideUp(500);
        $('.dropdown-menu-control').removeClass('drop-opened');
        $('.dropdown-menu-control i').removeClass('fa-arrow-up');
        $('.dropdown-menu-control i').addClass('fa-arrow-down');       // what we do when we clicked ouf of element
        event.stopPropagation();
      });



})