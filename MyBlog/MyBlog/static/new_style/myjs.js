window.onload=init;



function init()
{


}

function mouseover()
{
    this.style.color="#007bff";
}
function mouseout()
{
    this.style.color="black";
}

function del_code_item()
{
    code_list = document.getElementsByTagName("code");
    alert(code_list.length);
    for(var i=0;i<code_list.length;i++)
    {
        parent = code_list[i].parentNode;
        parent.innerHTML =  code_list[i].text;
        parent.removeChild(code_list[i]);
    }

}