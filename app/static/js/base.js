function toggleDetails(index){
  $("#details").toggle();
}
var upVoteNumber = 0;
function upVote(){
  upVoteNumber++;
  document.getElementById('#upVote').innerHTML = upVoteNumber;
}