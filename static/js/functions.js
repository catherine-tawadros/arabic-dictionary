function reverseDiv(toggle){
    if (document.getElementById(toggle).style.display == 'block') {
      document.getElementById(toggle).style.display = 'none';
    }
    else if (document.getElementById(toggle).style.display == 'none') {
      document.getElementById(toggle).style.display = 'block';
    }
  }

function showDiv(toggle){
    document.getElementById(toggle).style.display = 'block';
}
