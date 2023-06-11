function likeHeart() {
    let heart = document.getElementById("like");
    heart.style.color = "#ff0000";
}

let comment_section = document.getElementById("comment");
comment_section.style.maxHeight = "0px";
function comment() {
    if(comment_section.style.maxHeight == "0px"){
        comment_section.style.maxHeight = "55px";
    }
    else {
        comment_section.style.maxHeight = "0px";
    }
}
function postDone() {
    alert("Your COmment has been posted !!!")
}