window.onload=init;



function init()
{
    title = document.getElementsByClassName("title-link")
    for(var i=0;i<title.length;i++)
    {
        title[i].onmouseover=mouseover;
        title[i].onmouseout = mouseout;
    }
}

function mouseover()
{
    this.style.color="#007bff";
}
function mouseout()
{
    this.style.color="black";
}