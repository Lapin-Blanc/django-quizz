$(function() {
    var $container = $('#conteneur');
    var $selection = $('<div>').addClass('selection-box');
    var $image = $('#capture_image');
    var $pos = $container.position();
    
    
    $container.on('mousedown', function(e) {
        var click_y = e.pageY - $pos.top, click_x = e.pageX - $pos.left;
        $("#zoneimage_set-empty").prev().find("td.field-x>input").val(click_x)
        $("#zoneimage_set-empty").prev().find("td.field-y>input").val(click_y)
        $selection.css({
          'top':    click_y,
          'left':   click_x,
          'width':  0,
          'height': 0
        });
        $selection.appendTo($container);
        
        $container.on('mousemove', function(e) {            
                var move_x = e.pageX - $pos.left,
                    move_y = e.pageY - $pos.top,
                    width  = Math.abs(move_x - click_x),
                    height = Math.abs(move_y - click_y);
                $("#zoneimage_set-empty").prev().find("td.field-width>input").val(width)
                $("#zoneimage_set-empty").prev().find("td.field-height>input").val(height)
                $selection.css({
                    'width':  width,
                    'height': height
                });
                if (move_x < click_x) { //mouse moving left instead of right
                    $selection.css({
                        'left': click_x - width
                    });
                    $("#zoneimage_set-empty").prev().find("td.field-x>input").val(click_x - width)
                }
                if (move_y < click_y) { //mouse moving up instead of down
                    $selection.css({
                        'top': click_y - height
                    });
                    $("#zoneimage_set-empty").prev().find("td.field-y>input").val(click_y - height)
                }
        }).on('mouseup', function(e) {
            $container.off('mousemove');
            // $selection.remove();
        });
    });
    
    $image.load(function() {
        $image.parent().width($image.width())
        $image.parent().height($image.height())
    });
});

