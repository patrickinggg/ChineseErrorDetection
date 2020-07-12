var canvas_background = new Image();
// var web_url = "http://80.85.84.44:5000/"
var web_url = "http://127.0.0.1:5000/"

canvas_background.src = web_url + "public/tianzige1.png"


window.onload = function(){

  var mycanvas = document.getElementById("mycanvas");
  var ctx = mycanvas.getContext("2d");
  var clic = false;
  var xCoord, yCoord = "";
  var canvaslist = [];
  var undo_list = [];
  var stroke_num = 0;
  var stroke_coords = [];
  var total_stroke_num = 0;
  var factor = 0;
  ctx.strokeStyle = "#000000";
  ctx.lineWidth = 20;
  ctx.lineCap = "round";
  ctx.fillStyle = "#fff";
  ctx.fillRect(0, 0, mycanvas.width, mycanvas.height);
  ctx.drawImage(canvas_background, 0, 0, 500, 500, 0, 0, 500, 500 );
  document.getElementById("feedback").innerHTML = "~ This box will display feedback/hint ~";



  // var img = new Image();
  // img.onload = function() {
  // ctx.drawImage(img, 0, 0);
  // }
  // img.src = "http://upload.wikimedia.org/wikipedia/commons/d/d2/Svg_example_square.svg";

  load_stroke_num()
  // alert(total_stroke_num)
  // create_canves(7);
  var initialImage = ctx.getImageData(0, 0, mycanvas.width, mycanvas.height);
  undo_list.push(initialImage);

  mycanvas.addEventListener('mousedown', function(canvas){
    ctx.globalAlpha = 1.0;
    console.log(xCoord)

    clic = true;
    ctx.save();
    xCoord = canvas.pageX - this.offsetLeft;
    yCoord = canvas.pageY - this.offsetTop;
  });

  mycanvas.addEventListener('mouseup', function(canvas){
    var imgData = ctx.getImageData(0, 0, mycanvas.width, mycanvas.height);
    undo_list.push(imgData);
    var stroke_img = draw_stroke(stroke_coords, stroke_num);
    send_stroke(stroke_img)
    stroke_coords = [];
    stroke_num++;
    clic = false;
  });

  mycanvas.addEventListener('click', function(canvas){
    console.log(xCoord);

    clic = false;
  });

  mycanvas.addEventListener('mousemove', function(canvas){
    if(clic == true){
        ctx.beginPath();
        ctx.moveTo(canvas.pageX - this.offsetLeft, canvas.pageY - this.offsetTop);
        stroke_coords.push({x: canvas.pageX - this.offsetLeft, y: canvas.pageY - this.offsetTop})
        //capture the trace by x and y
        ctx.lineTo(xCoord, yCoord);
        ctx.stroke();
        ctx.closePath();
        xCoord = canvas.pageX - this.offsetLeft;
        yCoord = canvas.pageY - this.offsetTop
    }
  });

  mycanvas.addEventListener('touchstart', function(event){
    console.log("touched")
    ctx.globalAlpha = 1.0;

    clic = true;
    ctx.save();
    if (event.touches.length == 1) { // Only deal with one finger
        var touch = event.touches[0]; // Get the information for finger #1
        xCoord=touch.pageX - this.offsetLeft;
        yCoord=touch.pageY - this.offsetTop;
    }


  });

  mycanvas.addEventListener('touchend', function(canvas){
    var imgData = ctx.getImageData(0, 0, mycanvas.width, mycanvas.height);
    undo_list.push(imgData);
    var stroke_img = draw_stroke(stroke_coords, stroke_num);
    send_stroke(stroke_img)
    stroke_coords = [];
    stroke_num++;
    clic = false;
  });


  mycanvas.addEventListener('touchmove', function(event){
    if(clic == true){
        console.log(event.touches.length)
        ctx.beginPath();
        ctx.moveTo(event.touches[0].pageX - this.offsetLeft, event.touches[0].pageY - this.offsetTop);
        stroke_coords.push({x: event.touches[0].pageX - this.offsetLeft, y: event.touches[0].pageY - this.offsetTop})
        //capture the trace by x and y
        ctx.lineTo(xCoord, yCoord);
        ctx.stroke();
        ctx.closePath();
        if (event.touches.length == 1) { // Only deal with one finger
            var touch = event.touches[0]; // Get the information for finger #1
            xCoord=touch.pageX - this.offsetLeft;
            yCoord=touch.pageY - this.offsetTop;
        }
        // xCoord = event.pageX - this.offsetLeft;
        // yCoord = event.pageY - this.offsetTop
        event.preventDefault();
    }
  });


  function load_stroke_num(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var myObj = JSON.parse(this.responseText);
        create_canves(myObj.total_stroke_num);
      }
    };
    xhttp.open("GET", web_url + "get_stroke_num", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
  }

  function loadDoc() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        alert(this.responseText);
      }
    };
    xhttp.open("GET", web_url , true);
    xhttp.send();
  }

  function openModal() {
          document.getElementById('modal').style.display = 'block';
          document.getElementById('fade').style.display = 'block';
  }

  function closeModal() {
      document.getElementById('modal').style.display = 'none';
      document.getElementById('fade').style.display = 'none';
  }

  function send_stroke(stroke_img) {
    openModal();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        closeModal();
        var myObj = JSON.parse(this.responseText);
        if (myObj.feedback == "0" ){
          document.getElementById("feedback").innerHTML = "Please correct the previous stroke.";
          undo_list.pop();
          var restore_state = undo_list[undo_list.length - 1];
          ctx.putImageData(restore_state, 0, 0);
          empty_canvas(stroke_num-1);
          stroke_num -= 1;

        } else {
          if (myObj.factor != 0){
            factor = myObj.factor;
          }
          if(stroke_num == 1 ){
            getAllHintFunction();

          }
          // alert(this.responseText);
          document.getElementById("feedback").innerHTML = myObj.feedback;
        }

        // alert();
      }
    };

    xhttp.open("POST", web_url + "sendstroke", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(stroke_img));
    console.log(JSON.stringify(stroke_img))
  }

  function create_canves(num){
    for (var i = 0; i < num; i++){
      var canv= document.createElement("canvas");
      canv.height = 500;
      canv.width = 500;
      canv.id = i;
      canvaslist.push(canv);
      document.body.appendChild(canv);
      document.getElementById(i).style.display = "none";

    }

  }

  function empty_canvas(canvas_id){
    console.log(canvas_id)
    var canvas = document.getElementById(canvas_id);
    console.log(canvas)
    var context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);

  }


  function draw_stroke(stroke_coords, canvas_id){
    var canvas = document.getElementById(canvas_id);

    var ctx = canvas.getContext("2d");
    var xCoord = stroke_coords[0].x;
    var yCoord = stroke_coords[0].y;
    ctx.strokeStyle = "#000000";
    if (stroke_num == 0){
      ctx.lineWidth = 20;
    } else {
      ctx.lineWidth = 20 + (10 * (factor - 1));
    }
    ctx.lineCap = "round";
    ctx.fillStyle = "#FFFFFF";
    ctx.fillRect(0, 0, mycanvas.width, mycanvas.height);

    for (var i = 1; i < stroke_coords.length; i++){
      ctx.beginPath();
      ctx.moveTo(xCoord, yCoord);
      ctx.lineTo(stroke_coords[i].x, stroke_coords[i].y);
      ctx.stroke();
      ctx.closePath();
      xCoord = stroke_coords[i].x;
      yCoord = stroke_coords[i].y;
    }

    var imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    var theimg = [];
    for (var i = 0; i < imgData.data.length; i += 4){
      theimg.push(imgData.data[i]);
    }
    // console.log(theimg);

    return theimg;
  }

  function savestate(){

  }

  document.getElementById("undo").onclick = function() {undoFunction()};
  function undoFunction() {

    if(undo_list.length == 1){
      document.getElementById("feedback").innerHTML = "Empty canvas, cannot undo";
    } else {
      undo_list.pop();
      var restore_state = undo_list[undo_list.length - 1];
      ctx.putImageData(restore_state, 0, 0);
      empty_canvas(stroke_num-1);
      stroke_num -= 1;
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("feedback").innerHTML = this.responseText;
        }
      };
      xhttp.open("GET", web_url + "undo", true);
      xhttp.setRequestHeader("Content-type", "application/json");
      xhttp.send();
    }


  }

  document.getElementById("clear").onclick = function() {clearFunction()};
  function clearFunction() {
    if (undo_list.length == 1){
      document.getElementById("feedback").innerHTML = "Empty canvas, nothing to clear";
    } else {
      var restore_state = undo_list[0];
      undo_list = [];
      undo_list.push(restore_state);
      ctx.putImageData(restore_state, 0, 0);
      for(var i = 0; i < canvaslist.length; i++){
        empty_canvas(i);
      }
      stroke_num = 0;

      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("feedback").innerHTML = this.responseText;
        }
      };
      xhttp.open("GET", web_url + "clear", true);
      xhttp.setRequestHeader("Content-type", "application/json");
      xhttp.send();
    }


  }

  document.getElementById("get_hint").onclick = function() {getHintFunction()};
  function getHintFunction() {

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var myObj = JSON.parse(this.responseText);

        // console.log(myObj.url)
        // console.log(myObj.dis_x )
        // console.log(myObj.dis_y )
        // console.log(myObj.factor)

        var dis_X = myObj.dis_x
        var dis_Y = myObj.dis_y
        var factor = myObj.factor * 500
        var base_image = new Image();
        base_image.src = myObj.url;
        var ga = 1.0;
        var timerId = 0;
        var current_canvas = ctx.getImageData(0, 0, mycanvas.width, mycanvas.height);

        timerId = setInterval(fadeOut, 200);
        ctx.clearRect(0,0, mycanvas.width,mycanvas.height);
        ctx.putImageData(current_canvas, 0, 0);
        // base_image.onload = function() {
        // ctx.drawImage(base_image, 0, 0, 500, 500, dis_X, dis_Y, factor, factor);
        // }
        // img.src = "http://upload.wikimedia.org/wikipedia/commons/d/d2/Svg_example_square.svg";
        // ctx.drawImage(base_image, 0, 0, 500, 500, dis_X, dis_Y, factor, factor );
        // ctx.fillStyle = "#FF0000";
        // ctx.fillRect(myObj.x1, myObj.y1,myObj.x2,myObj.y2)
        function fadeOut()
        {
            ctx.putImageData(current_canvas, 0, 0);
            ctx.globalAlpha = ga;
            var base_image = new Image();
            base_image.onload = function()
            {
                ctx.drawImage(base_image, 0, 0, 500, 500, dis_X, dis_Y, factor, factor);
            };
            base_image.src = myObj.url;

            ga = ga - 0.2;
            if (ga <=  0.0)
            {
              clearInterval(timerId);
              return 0;
            }
        }

      }
    };

    xhttp.open("GET", web_url + "get_hint", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
  }

  document.getElementById("get_all_hint").onclick = function() {getAllHintFunction()};
  function getAllHintFunction() {

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        // alert(this.responseText);
        var myObj = JSON.parse(this.responseText);

        var dis_X = myObj.dis_x;
        var dis_Y = myObj.dis_y;
        var factor = myObj.factor * 500;
        var url = myObj.url1;
        var ga = 1.0;
        var timerId = 0;
        var current_canvas = ctx.getImageData(0, 0, mycanvas.width, mycanvas.height);

        timerId = setInterval(fadeOut, 100);
        ctx.clearRect(0,0, mycanvas.width,mycanvas.height);
        ctx.putImageData(current_canvas, 0, 0);


        function fadeOut()
        {
            ctx.putImageData(current_canvas, 0, 0);
            ctx.globalAlpha = ga;

            var base_image = [];
            for (var i = 1; i <= canvaslist.length; i++){
              base_image[i] = new Image();
              base_image[i].onload = (function (j) {
                return (function () {
                  ctx.drawImage(base_image[j], 0, 0, 500, 500, dis_X, dis_Y, factor, factor);
                });
              }(i));
              base_image[i].src = myObj.url1 + i + ".png";
            }

            ga = ga - 0.2;
            if (ga <=  0.0)
            {
              clearInterval(timerId);
              return 0;
            }
        }

      }
    };

    xhttp.open("GET", web_url + "get_all_hint", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
  }

};
