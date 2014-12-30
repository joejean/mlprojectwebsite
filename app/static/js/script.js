$(document).ready(function(){
  jobkey = $("#jobkey").data();

  var url = "http://ml2014.herokuapp.com/getresults/"+jobkey.name;
  var interval = setInterval( function() {
    $.ajax({
      type:'GET',
      url: url,
      dataType: 'json',
      success: function(data){
          console.log(data);
        if (data.error == "undefined"){

          $('#loading').hide();

          if (_.size(data) !== 0){

            $('#results').show();
            var out = "<ul>";
            $.each(data, function(cat, score){
              out += "<li>"+cat+"</li>";
            });
            out += "</ul>";
            $('#results').append(out);
            clearInterval(interval);
          }
          else{

            $('#noresults').show();
          }
        }
      },
      error: function(error){
        console.log(error);
      }

    });

    },10000);

})

