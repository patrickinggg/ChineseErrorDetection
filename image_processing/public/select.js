window.onload = function(){
  // var web_url = "http://80.85.84.44:5000/"
  var web_url = "http://127.0.0.1:5000/"
  var logo_clicked = false;
  document.getElementById("logo").onclick = function(){definition()};
  function definition(){
    if (logo_clicked == false){
      document.getElementById('definition').style.display = 'block';
      logo_clicked = true;
    } else {
      document.getElementById('definition').style.display = 'none';
      logo_clicked = false;
    }
  }

  document.getElementById("submit").onclick = function() {submitFunction()};
  function submitFunction(){
    var inputVal = document.getElementById("fname").value;

    check_character_exist(inputVal, function(if_exist){
      if (!if_exist){
        alert("This character is not collected in the database so far.")
      } else {
        window.open(web_url + "public/writing.html","_self")
      }
    });
  }

  function check_character_exist(character_name, callback) {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        callback('1' == this.responseText);
      }
    };
    xhttp.open("POST", web_url + "check_exist", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(character_name));
  }


};
