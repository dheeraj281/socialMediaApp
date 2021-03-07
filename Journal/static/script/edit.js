var intialState;

function formEditor(contetHeight){
    console.log(contentHeight);
    $('#summernote').summernote({
            height: contentHeight,
            focus: true,
            toolbar: [
              ['font', ['bold', 'underline']],
              ['color', ['color']],
              ['para', ['ul', 'paragraph']],
              ['insert', ['link']],
              ['view', ['fullscreen','undo','redo', 'help']]
            ]
          });

}

$('#updateform').submit(function(){
    var textareaValue = $('#summernote').summernote('code').replace(/<\/?[^>]+(>|$)/g, "");
    if (textareaValue == ""){
     alert('editor content is empty');
     return false;
    }
});




function cancel(){
   $('#summernote').summernote('destroy');
   $(".postcards")[0].innerHTML = intialState;
}

function updateform() {
  $(".post").css("height", "80%");
  $(".postcards").css("height", "65%");
  contentHeight= $(".postcards")[0].offsetHeight
  intialState = $(".postcards")[0].innerHTML
  content = $(".user_content")[0].innerHTML
  form= document.getElementById("updateform")
  form.classList.remove("hide");
  document.getElementsByClassName("card")[0].classList.add("hide");
  formEditor(contentHeight)
  $('#summernote').summernote('pasteHTML', content);
}

window.onload = function() {updateform()};

