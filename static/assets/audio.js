(function ($) {
    $(function () {
        var equalizerLines = $(".js-equlizer_line");

        setInterval(function () {
            $.each(equalizerLines, function (index) {
                let x = document.getElementById('audio').paused
                if (!x) {
                    var rand = 0 - 0.5 + Math.random() * (100 - 0 + 1);
                    rand = Math.round(rand);
                    $(this).css({ height: rand + "%" });
                }else{
                    $(this).css({ height: "1%" });
                }
            });
        }, 50);
    });
})(jQuery);


var audio = document.getElementById('audio');
var playpause = document.getElementById("play");


function togglePlayPause() {
   if (audio.paused || audio.ended) {
      playpause.title = "Pause";
      audio.play();
   } else {
      playpause.title = "Play";
      audio.pause();
   }
}