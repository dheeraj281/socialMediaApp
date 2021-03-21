// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

// Get the header
var header = document.getElementById("headernav");

// Get the offset position of the navbar
var sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}


function enableEditor(){
    document.getElementById("postform").classList.remove("hide");
    $('#summernote').summernote({
            placeholder: "What's On Your Mind?",
            tabsize: 1,
            height: 150,
            focus: true,
            toolbar: [
              ['style', ['style']],
              ['font', ['bold', 'underline']],
              ['color', ['color']],
              ['para', ['ul', 'paragraph']],
              ['insert', ['link']],
              ['view', ['fullscreen','undo','redo', 'help']]
            ]
          });

}

function closeEditor(){
   document.getElementById("postform").classList.add("hide");
   $('#summernote').summernote('destroy');
   //$('#summernote').summernote('reset');
}

function deletePost(element){
    event.preventDefault();
    $.ajax({
      type: 'POST',
      url: "/deletepost",
      data: {
          id: $(element).attr('id')
      },
      dataType: "text",
      success: function(data){
                 console.log(data)
                 $(element).parent('div').parent('div').remove();
               },
      error: function(error) {
          console.log(error);
      }
    });
};